import pandas as pd
import numpy as np
import logging

# Define logging
# Create logger definition
logger = logging.getLogger('Comparison.log')
logger.setLevel(logging.DEBUG)

# Create file handler which logs messages in log file
fh = logging.FileHandler('Comparison.log')
fh.setLevel(logging.DEBUG)

# Create console handler with high level log messages in console
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Create formatter and add it to the handlers
formatter = logging.Formatter('%(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(ch)
# logger.addHandler(fh)


def df_diff(actual_file_path: str, expected_file_path: str, actual_file_name: str, expected_file_name: str,
            file_format: str, key_columns: list, ignore_columns: list):
    """
    This method is used to find the differences between two data frame
    :param actual_file_path: r'C://Desktop//Comparison//data//actual//'
    :param expected_file_path: r'C://Desktop//Comparison//data//baseline//'
    :param actual_file_name: compare_actual_file
    :param expected_file_name: compare_base_file
    :param file_format: 'psv' or 'csv'
    :param key_columns: unique key columns names as list ['Key_Column1', 'Key_Column2']
    :param ignore_columns: columns to ignore ['Ignore_Column1', 'Ignore_Column2']
    :return:
    """
    logger.info('****************************************************************************************************')
    logger.info('PandasUtil Data Frame Comparison - Cell by Cell comparison with detailed mismatch report')
    logger.info('****************************************************************************************************')
    logger.info('Step-01 : Based on file format create the df with delimiter(sep)')
    if file_format == 'psv':
        df1 = pd.read_csv(actual_file_path + actual_file_name + '.' + file_format, sep='|', dtype='str',
                          keep_default_na =False)
        df2 = pd.read_csv(expected_file_path + expected_file_name + '.' + file_format, sep='|', dtype='str',
                          keep_default_na =False)
    elif file_format == 'csv':
        df1 = pd.read_csv(actual_file_path + actual_file_name + '.' + file_format, dtype='str',
                          keep_default_na =False)
        df2 = pd.read_csv(expected_file_path + expected_file_name + '.' + file_format, dtype='str',
                          keep_default_na =False)

    logger.info('Step-02 : Create the summary df based on count of rows and identify the count diff')
    # Create the summary df
    summary_col = ['Actual', 'Expected', 'Mismatch']
    summary_df = pd.DataFrame(columns=summary_col)
    summary_df = summary_df.append({'Actual': round(len(df1)), 'Expected': round(len(df2)),
                                    'Mismatch': round(len(df1)) - round(len(df2))}, ignore_index=True)
    logger.debug(summary_df)

    logger.info('Step-03 : Remove the columns based on ignore columns list')
    # If ignore columns are specified, remove those columns from comparison
    if len(ignore_columns) > 0:
        df1.drop(columns=ignore_columns, inplace=True)
        df2.drop(columns=ignore_columns, inplace=True)

    logger.info('Step-04 : Sort the df1 and df2 based on key columns and reset the index')
    # Sort df1 and df2 based on key columns and reset the index
    df1.sort_values(by=key_columns, ascending=True, inplace=True)
    df2.sort_values(by=key_columns, ascending=True, inplace=True)
    df1.reset_index(inplace=True)
    df2.reset_index(inplace=True)

    # Set the index based on key columns in df1 and df2. Remove the default index column
    df1 = df1.set_index(key_columns, drop=True, append=False, inplace=False, verify_integrity=True)
    df2 = df2.set_index(key_columns, drop=True, append=False, inplace=False, verify_integrity=True)
    df1 = df1.drop('index', axis=1)
    df2 = df2.drop('index', axis=1)

    logger.info('Step-05 : Identify the rows matching based on key in both df1 and df2')
    # Identify the rows matching based on key in both df1 and df2
    merge_outer_df = pd.merge(df1, df2, how='outer', on=key_columns, indicator='source')
    key_matched_df = merge_outer_df.loc[merge_outer_df['source'] == 'both'].copy()
    key_mismatched_df = merge_outer_df.loc[merge_outer_df['source'] != 'both'].copy()

    # Update the source column left_only to actual and right_only to expected
    # key_mismatched_df.loc[key_mismatched_df['source'] == 'left_only', 'source'] = 'Actual'

    logger.info('Step-06 : Create the summary df based on key columns')
    # Create the summary df based on key columns
    summary_key_col = ['Key_Matched', 'Key_Mismatch', 'Actual', 'Expected']
    summary_key_df = pd.DataFrame(columns=summary_key_col)
    actual_key_mismatch = len(key_mismatched_df[key_mismatched_df.source == 'left_only'])
    expected_key_mismatch = len(key_mismatched_df[key_mismatched_df.source == 'right_only'])
    summary_key_df = summary_key_df.append({'Key_Matched': round(len(key_matched_df)),
                                            'Key_Mismatch': round(len(key_mismatched_df)),
                                            'Actual': actual_key_mismatch,
                                            'Expected': expected_key_mismatch}, ignore_index=True)
    logger.debug(summary_key_df)
    logger.debug(key_mismatched_df)

    logger.info('Step-07 : Remove the mismatched key values and proceed further in validation')
    df1.drop(key_mismatched_df.loc[key_mismatched_df['source'] == 'left_only'].index, inplace=True)
    df2.drop(key_mismatched_df.loc[key_mismatched_df['source'] == 'right_only'].index, inplace=True)

    logger.info('Step-08 : Started cell by cell comparison for key values that exist in both df1 and df2')
    # Verify if columns in both df1 and df2 are same
    assert (df1.columns == df2.columns).all(), logger.debug('Failed - Column mismatch determined')

    logger.info('Step-09 : Verify column data types in both the files, if not convert based on actual')
    if any(df1.dtypes != df2.dtypes):
        logger.debug('Data Types are different, trying to convert')
        df2 = df2.astype(df1.dtypes)

    logger.info('Step-10 : Verify cell by cell data in both the data frame and generate mismatch report')
    # df to hold cell by cell comparison results
    cell_comp_df = pd.DataFrame([])

    # Verify if all the cell data are identical
    if df1.equals(df2):
        logger.info('          Passed : Cell by Cell comparison')
    else:
        logger.info('          Failed : Cell by Cell comparison ..Started to extract mismatched column values')
        # create new data frame with mismatched columns
        diff_mask = (df1 != df2) & ~(df1.isnull() & df2.isnull())
        ne_stacked = diff_mask.stack()
        changed = ne_stacked[ne_stacked]
        key_columns.append('Mismatch_Column')
        changed.index.names = key_columns
        difference_locations = np.where(df1 != df2)
        changed_from = df1.values[difference_locations]
        changed_to = df2.values[difference_locations]
        cell_comp_df = pd.DataFrame({'Expected_Data': changed_from, 'Actual_Data': changed_to}, index=changed.index)
    logger.info('Step-11 : Comparison completed and generated info for reports(summary, keys mistmach, cell by cell')
    logger.info('****************************************************************************************************')
    return summary_df, summary_key_df, key_mismatched_df, cell_comp_df
