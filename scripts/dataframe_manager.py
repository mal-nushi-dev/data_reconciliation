import pandas as pd
import sys
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
        logger.warning(f"Columns missing in DataFrame 1: {
                       missing_df1_columns}.")
        sys.exit()
    if missing_df2_columns:
        logger.warning(f"Columns missing in DataFrame 2: {
                       missing_df2_columns}.")
        sys.exit()

    if not missing_df1_columns and not missing_df2_columns:
        logger.info(
            "All column names match and there are no missing columns between the datasets.")


def data_validation(df1, df2, output_path='assets/outputs/diff.html'):
    # Check if DataFrames have the same columns
    if set(df1.columns) != set(df2.columns):
        logger.warning("DataFrames do not have the same columns.")
        return

    # Reindex DataFrames to ensure alignment
    df1 = df1.reindex_like(df2)

    # Identify rows with any differences
    differences = df1 != df2
    rows_with_differences = differences.any(axis=1)

    if not rows_with_differences.any():
        logger.info("There are no differences between the datasets.")
        return
    else:
        logger.warning("There are differences between the datasets.")

    # Create a new DataFrame to hold the differences side by side for the rows with differences
    diff = pd.DataFrame(index=df1.index[rows_with_differences])
    for col in df1.columns:
        diff[f'{col}_source'] = df1.loc[rows_with_differences, col]
        diff[f'{col}_target'] = df2.loc[rows_with_differences, col]

    # Highlight differences using Styler
    def highlight_diffs(data):
        color = 'background-color: yellow'
        df_styler = pd.DataFrame('', index=data.index, columns=data.columns)
        for col in df1.columns:
            df_styler.loc[differences[col] &
                          rows_with_differences, f'{col}_source'] = color
            df_styler.loc[differences[col] &
                          rows_with_differences, f'{col}_target'] = color
        return df_styler

    # Style the DataFrame
    styled_diff = diff.style.apply(highlight_diffs, axis=None)

    # Save the styled DataFrame to an HTML file
    styled_diff.to_html(output_path)
    logger.info(f"Differences highlighted and saved to {output_path}")
