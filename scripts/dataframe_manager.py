import pandas as pd
from scripts.logging_config import get_logger


logger = get_logger()


def row_count_validation(df1, df2):
    # Check counts
    df1_record_count = df1.shape[0]
    df2_record_count = df2.shape[0]

    logger.info(f"Source record count: {df1_record_count}")
    logger.info(f"Target record count: {df2_record_count}")

    if df1_record_count == df2_record_count:
        logger.info("Counts are the same")
    else:
        logger.warning("Counts are different")


def column_validation(df1, df2):
    df1_record_count = df1.columns
    df2_record_count = df2.columns

    # Check column counts
    logger.info(f"Source columns: {len(df1_record_count)}.")
    logger.info(f"Target columns: {len(df2_record_count)}.")
    if len(df1_record_count) == len(df2_record_count):
        logger.info("Column counts are the same.")
    else:
        logger.warning("Column counts are different.")

    # Check for missing columns in each DataFrame
    missing_df1_columns = set(df1_record_count) - set(df2_record_count)
    missing_df2_columns = set(df2_record_count) - set(df1_record_count)
    if missing_df1_columns:
        logger.warning(f"Columns missing in DataFrame 1: {missing_df1_columns}.")
    if missing_df2_columns:
        logger.warning(f"Columns missing in DataFrame 2: {missing_df2_columns}.")

    if not missing_df1_columns and not missing_df2_columns:
        logger.info("All column names match and there are no missing columns between the datasets.")


def column_level_validation(df1, df2):
    # Merge the two dataframes, indicator=True adds a column '_merge' that indicates where the merge matched
    merged_df = pd.merge(df1, df2, how='outer', indicator=True)

    # Rows that are only in source_df or only in target_df
    diff_df = merged_df[merged_df['_merge'] != 'both']
    if diff_df.empty:
        logger.info("There are no differences between the datasets.")
    else:
        logger.warning("There are differences between the datasets.")
        pd.DataFrame.to_html(diff_df, 'assets/outputs/diff.html')
