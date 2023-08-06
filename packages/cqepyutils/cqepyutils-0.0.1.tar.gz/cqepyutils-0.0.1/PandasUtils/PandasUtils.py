import pandas as pd
import numpy as np
import time
import logging


def df_diff(df1: pd.DataFrame, df2: pd.DataFrame, key_columns: list):
    """
    This method is used to find the differences between two data frame
    :param key_columns:
    :param df1: data frame 1
    :param df2: data frame 2
    :param key_columns: unique key columns names as list ['Key_Column1', 'Key_Column2']
    :return:
    """
    logging.info('****************************************************************************************************')
    logging.info('Identify difference between two data frames - Cell by Cell comparison with mismatch report')
    logging.info('****************************************************************************************************')
    logging.info('Step-1 : Verify columns in both the data frame')
    assert (df1.columns == df2.columns).all(), logging.info('Failed - Column mismatch determined')
    logging.info('Step-1 : Verify columns in both the data frame')
    logging.info('Step-2 : Verify column data types in both the data frame')
    if any(df1.dtypes != df2.dtypes):
        "Data Types are different, trying to convert"
        df2 = df2.astype(df1.dtypes)
    logging.info('Step-2 : Verify column data types in both the data frame')
    logging.info('Step-3 : Verify cell by cell data in both the data frame')
    if df1.equals(df2):
        logging.info('Passed : Cell by cell comparison passed')
        return None
    else:
        logging.info('Failed : Cell by cell comparison failed.. Started to extract mismatched column values')
        # create new data frame with mismatched columns
        diff_mask = (df1 != df2) & ~(df1.isnull() & df2.isnull())
        ne_stacked = diff_mask.stack()
        changed = ne_stacked[ne_stacked]
        key_columns.append('Mismatch_Column')
        changed.index.names = key_columns
        difference_locations = np.where(df1 != df2)
        changed_from = df1.values[difference_locations]
        changed_to = df2.values[difference_locations]
        logging.info('Failed : Extracted all mismatched column values')
        logging.info('************************************************************************************************')
        return pd.DataFrame({'Expected_Data': changed_from, 'Actual_Data': changed_to},
                            index=changed.index)
