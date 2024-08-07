import pandas as pd
import numpy as np
import sys
from modules.logging_config import Logger
from modules.get_config import get_config


logger = Logger()


class DataFrameValidator:
    """
    A class to validate and compare two Pandas DataFrames.

    Attr:
        df1 (pd.DataFrame): The first DataFrame.
        df2 (pd.DataFrame): The second DataFrame.

    Methods:
        __init__(df1: pd.DataFrame, df2: pd.DataFrame): Initializes the DataFrameValidator with two DataFrames.
        validate(): Runs all validation checks on the DataFrames.
        row_count_validation(): Validates that both DataFrames have the same number of rows.
        column_validation(): Validates that both DataFrames have the same columns and column counts.
        data_validation(output_path: str = 'assets/outputs/diff.html'): Validates that the data in both DataFrames is the same and highlights differences.
        _create_diff_dataframe(differences: pd.DataFrame, rows_with_differences: pd.Series): Creates a DataFrame to show the differences side by side.
        _highlight_diffs(diff: pd.DataFrame, differences: pd.DataFrame, rows_with_differences: pd.Series): Applies highlighting to the differences in the DataFrame.
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
        self.numeric_column_extra_validations()
        self.date_column_extra_validations()

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

    def numeric_column_extra_validations(self) -> None:
        """
        Retrieves numeric-type columns based on the configuration settings, and triggers validation checks.

        If 'AUTO_NUMERIC_DISCOVER' is set to '1', it automatically discovers numeric-type columns.
        If 'AUTO_NUMERIC_DISCOVER' is set to '0', it retrieves numeric-type columns from the configuration.
        Logs an error if there is an issue with retrieving the numeric-type columns.
        """

        # Initialize 'numeric_columns' as an empty list
        numeric_columns = []

        try:
            # Retrieve the 'AUTO_NUMERIC_DISCOVER' configuration value
            auto_numeric_discover = get_config('COLUMN_TYPES', 'AUTO_NUMERIC_DISCOVER')

            if auto_numeric_discover == '1':
                numeric_columns = self.df1.select_dtypes(include=[np.number]).columns
            elif auto_numeric_discover == '0':
                numeric_columns = [item.strip() for item in get_config('COLUMN_TYPES', 'NUMERIC').split(',')]
            else:
                raise ValueError(f"Invalid value for 'AUTO_NUMERIC_DISCOVER' in 'config.ini' file: {auto_numeric_discover}")

            # Perform validation checks with the discovered numeric-type columns
            self.min_max_check(datatype='Numeric', columns=numeric_columns)
            self.median_check(datatype='Numeric', columns=numeric_columns)
            # self.mode_check(datatype='Numeric', columns=numeric_columns)
        except Exception as e:
            logger.error(f"Error while retrieving the numeric-type columns: {e}")

    def date_column_extra_validations(self) -> None:
        """
        Retrieves date-type columns based on the configuration settings, and triggers validation checks.

        If 'AUTO_DATE_DISCOVER' is set to '1', it automatically discovers date-type columns.
        If 'AUTO_DATE_DISCOVER' is set to '0', it retrieves date-type columns from the configuration.
        Logs an error if there is an issue with retrieving the date-type columns.
        """

        # Initialize 'date_columns' as an empty list
        date_columns = []

        try:
            # Retrieve the 'AUTO_DATE_DISCOVER' configuration value
            auto_date_discover = get_config('COLUMN_TYPES', 'AUTO_DATE_DISCOVER')

            # TODO: Enable the AUTO_DATE_DISCOVER feature
            if auto_date_discover == '1':
                date_columns = self.df1.select_dtypes(include=[np.number]).columns
            elif auto_date_discover == '0':
                date_columns = [item.strip() for item in get_config('COLUMN_TYPES', 'DATE').split(',')]
            else:
                raise ValueError(f"Invalid value for 'AUTO_DATE_DISCOVER' in 'config.ini' file: {auto_date_discover}")

            # Perform validation checks with the discovered date-type columns
            self.min_max_check(datatype='Date', columns=date_columns)
            # self.median_check(datatype='Date', columns=date_columns)
            # self.mode_check(datatype='Date', columns=date_columns)
        except Exception as e:
            logger.error(f"Error while retrieving the date-type columns: {e}")

    def min_max_check(self, datatype: str, columns: list[str]) -> None:
        """
        Checks the minimum and maximum values of specified columns in two DataFrames and logs any discrepancies.

        Args:
            datatype (str): The datatype of the columns being checked.
            columns (list): The list of columns to check for minimum and maximum values.
        """

        # Check for min and max values for each column
        logger.info(f"Checking the MIN and MAX values for these {datatype} columns: {list(columns)}")
        for col in columns:
            # Calculate the min and max values
            min1 = self.df1[col].min()
            max1 = self.df1[col].max()

            min2 = self.df2[col].min()
            max2 = self.df2[col].max()

            # Check if the min and max values match between the two DataFrames
            if min1 != min2 or max1 != max2:
                logger.warning(f"Value range mismatch in column {col}: "
                               f"Source: (min: {min1}, max: {max1}), "
                               f"Target: (min: {min2}, max: {max2})")
            else:
                logger.info(f"The min and max values match between both datasets for the columnn: {col}: "
                            f"Source: (min: {min1}, max: {max1}), "
                            f"Target: (min: {min2}, max: {max2})")

    def median_check(self, datatype: str, columns: list[str]) -> None:
        """
        Checks the median values for specified columns in two DataFrames and logs any discrepancies.

        Args:
            datatype (str): The datatype of the columns being checked.
            columns (list): The list of columns to check for the median value.
        """

        try:
            # Check for median values for each column
            logger.info(f"Checking the median values for these columns: {columns}")
            for col in columns:
                # Calculate the median value
                med1 = self.df1[col].median()
                med2 = self.df2[col].median()

                # Check if the median values match between the two DataFrames
                if med1 != med2:
                    logger.warning(f"Median mismatch in column {col}: "
                                   f"Dataset1 (median: {med1}), "
                                   f"Dataset2 (median: {med2})")
                else:
                    logger.info(f"The median values matched between both datasets for the column: {col}: "
                                f"Dataset1 (median: {med1}), "
                                f"Dataset2 (median: {med2})")
        except Exception as e:
            logger.error(f"Error during median check: {e}")
            sys.exit(1)

    # def mode_check(self, datatype: str, columns: list[str]) -> None:
    #     """
    #     Checks the mode values for specified columns in two DataFrames and logs any discrepancies.

    #     Args:
    #         datatype (str): The datatype of the columns being checked.
    #         columns (list): The list of columns to check for the mode value.
    #     """

    #     try:
    #         # Check for mode values for each column
    #         logger.info(f"Checking the mode values for these columns: {columns}")
    #         for col in columns:
    #             # Calculate the mode value
    #             mode1 = self.df1[col].mode()
    #             mode2 = self.df2[col].mode()

    #             # Check if the mode values match between the two DataFrames
    #             if mode1 != mode2:
    #                 logger.warning(f"Mode mismatch in column {col}: "
    #                                f"Dataset1 (mode: {mode1}), "
    #                                f"Dataset2 (mode: {mode2})")
    #             else:
    #                 logger.info(f"The mode values matched between both datasets for the column: {col}: "
    #                             f"Dataset1 (mode: {mode1}), "
    #                             f"Dataset2 (mode: {mode2})")
    #     except Exception as e:
    #         logger.error(f"Error during mode check: {e}")
    #         sys.exit(1)
