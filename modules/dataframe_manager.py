import pandas as pd
import sys
from modules.logging_config import Logger


logger = Logger()


class DataFrameValidator:
    """
    A class to validate and compare two Pandas DataFrames.

    Attr:
        df1 (pd.DataFrame): The first DataFrame.
        df2 (pd.DataFrame): The second DataFrame.
    """

    def __init__(self, df1: pd.DataFrame, df2: pd.DataFrame) -> None:
        """
        Initializes the DataFrameValidator class with two DataFrames.

        Args:
            df1 (pd.DataFrame): The first DataFrame.
            df2 (pd.DataFrame): The second DataFrame.
        """

        self.df1 = df1
        self.df2 = df2

    def validate(self) -> None:
        """Runs all validation checks on the DataFrames."""

        self.row_count_validation()
        self.column_validation()
        self.data_validation()

    def row_count_validation(self):
        """Validates that both DataFrames have the same number of rows."""

        # Get the number of rows for each DataFrame
        df1_record_count = self.df1.shape[0]
        df2_record_count = self.df2.shape[0]

        logger.info(f"Source record count: {df1_record_count}")
        logger.info(f"Target record count: {df2_record_count}")

        if df1_record_count == df2_record_count:
            logger.info("Row counts are the same.")
        else:
            logger.error("Row counts are different.")
            sys.exit(1)

    def column_validation(self) -> None:
        """Validates that both DataFrames have the same columns and column counts."""

        # Get the column labels
        df1_columns = self.df1.columns
        df2_columns = self.df2.columns

        # Get the column lengths
        df1_column_count = self.df1.shape[1]
        df2_column_count = self.df2.shape[1]

        logger.info(f"Source columns: {df1_column_count}.")
        logger.info(f"Target columns: {df2_column_count}.")

        if df1_column_count == df2_column_count:
            logger.info("Column counts are the same.")
        else:
            logger.error("Column counts are different.")

        # Obtain any missing columns
        missing_df1_columns = set(df1_columns) - set(df2_columns)
        missing_df2_columns = set(df2_columns) - set(df1_columns)

        if missing_df1_columns:
            logger.error(f"columns missing in Dataframe 1: {missing_df1_columns}.")
            sys.exit(1)
        if missing_df2_columns:
            logger.error(f"Columns missing in Dataframe 2: {missing_df2_columns}.")
            sys.exit(1)

        if not missing_df1_columns and not missing_df2_columns:
            logger.info("All column names match and there are no missing columns.")

    def data_validation(self, output_path: str = 'assets/outputs/diff.html') -> None:
        """
        Validate that the data in both DataFrames is the same and highlight differences.
        Save the differences to an HTML file.

        Args:
            output_path (str): The path to save the HTML file with differences.
        """

        # Check if the columns in both DataFrames are the same, exit if not
        if set(self.df1.columns) != set(self.df2.columns):
            logger.warning("DataFrames do not have the same columns.")
            return

        # Align df1 with df2 columns
        self.df1 = self.df1.reindex_like(self.df2)

        # Compute the differences between the DataFrames
        differences = self.df1 != self.df2

        # Identify rows with any differences
        rows_with_differences = differences.any(axis=1)

        # Log if there are any differences, exit the script if none
        if not rows_with_differences.any():
            logger.info("There are no differences between the datasets.")
            return
        else:
            logger.warning("There are differences between the datasets.")

        # Create a DataFrame to show the differences side-by-side
        diff = self._create_diff_dataframe(differences, rows_with_differences)

        # Apply highlighting to the differences
        styled_diff = self._highlight_diffs(diff, differences, rows_with_differences)

        # Save the styled DataFrame with differences to an HTML file
        styled_diff.to_html(output_path)
        logger.info(f"Differences highlighted and saved to {output_path}")

    def _create_diff_dataframe(self, differences: pd.DataFrame, rows_with_differences: pd.Series) -> pd.DataFrame:
        """
        Create a DataFrame to show the differences side by side.

        Args:
            differences (pd.DataFrame): DataFrame of boolean values indicating differences.
            rows_with_differences (pd.Series): Series indicating rows with differences.

        Returns:
            pd.DataFrame: DataFrame with differences side-by-side.
        """

        # Initialize an empty DataFrame with the index of rows with differences
        diff = pd.DataFrame(index=self.df1.index[rows_with_differences])

        # Populate the DataFrame with the source and target values for each column
        for col in self.df1.columns:
            diff[f'{col}_source'] = self.df1.loc[rows_with_differences, col]
            diff[f'{col}_target'] = self.df2.loc[rows_with_differences, col]
        return diff

    def _highlight_diffs(self, diff: pd.DataFrame, differences: pd.DataFrame, rows_with_differences: pd.Series):
        """
        Apply highlighting to the differences in the DataFrame.

        Args:
            diff (pd.DataFrame): DataFrame with differences.
            differences (pd.DataFrame): DataFrame of boolean values indicating differences.
            rows_with_differences (pd.Series): Series indicating rows with differences.

        Returns:
            pd.io.formats.style.Styler: Styler object with highlighted differences.
        """

        def highlight_diffs(data: pd.DataFrame) -> pd.DataFrame:
            # Define the highlight color
            color = 'background-color: yellow'

            # Create a Styler DataFrame initialized with empty strings
            df_styler = pd.DataFrame('', index=data.index, columns=data.columns)

            # Apply the highlight color to the cells with differences
            for col in self.df1.columns:
                df_styler.loc[differences[col] & rows_with_differences, f'{col}_source'] = color
                df_styler.loc[differences[col] & rows_with_differences, f'{col}_target'] = color
            return df_styler

        # Apply the highlighting function to the DataFrame
        return diff.style.apply(highlight_diffs, axis=None)
