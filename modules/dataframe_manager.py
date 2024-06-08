import pandas as pd
import sys
from modules.logging_config import Logger


logger = Logger()


class DataFrameValidator:
    def __init__(self, df1, df2):
        self.df1 = df1
        self.df2 = df2

    def validate(self):
        self.row_count_validation()
        self.column_validation()
        self.data_validation()

    def row_count_validation(self):
        df1_record_count = self.df1.shape[0]
        df2_record_count = self.df2.shape[0]

        logger.info(f"Source record count: {df1_record_count}")
        logger.info(f"Target record count: {df2_record_count}")

        if df1_record_count == df2_record_count:
            logger.info("Row counts are the same.")
        else:
            logger.error("Row counts are different.")
            sys.exit(1)

    def column_validation(self):
        df1_columns = self.df1.columns
        df2_columns = self.df2.columns

        logger.info(f"Source columns: {len(df1_columns)}.")
        logger.info(f"Target columns: {len(df2_columns)}.")

        if len(df1_columns) == len(df2_columns):
            logger.info("Column counts are the same.")
        else:
            logger.error("Column counts are different.")

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

    def data_validation(self, output_path='assets/outputs/diff.html'):
        """
        Validate that the data in both DataFrames is the same and highlight differences.
        Save the differences to an HTML file.
        """
        if set(self.df1.columns) != set(self.df2.columns):
            logger.warning("DataFrames do not have the same columns.")
            return

        self.df1 = self.df1.reindex_like(self.df2)

        differences = self.df1 != self.df2
        rows_with_differences = differences.any(axis=1)

        if not rows_with_differences.any():
            logger.info("There are no differences between the datasets.")
            return
        else:
            logger.warning("There are differences between the datasets.")

        diff = self._create_diff_dataframe(differences, rows_with_differences)
        styled_diff = self._highlight_diffs(diff, differences, rows_with_differences)
        styled_diff.to_html(output_path)
        logger.info(f"Differences highlighted and saved to {output_path}")

    def _create_diff_dataframe(self, differences, rows_with_differences):
        """
        Create a DataFrame to show the differences side by side.
        """
        diff = pd.DataFrame(index=self.df1.index[rows_with_differences])
        for col in self.df1.columns:
            diff[f'{col}_source'] = self.df1.loc[rows_with_differences, col]
            diff[f'{col}_target'] = self.df2.loc[rows_with_differences, col]
        return diff

    def _highlight_diffs(self, diff, differences, rows_with_differences):
        """
        Apply highlighting to the differences in the DataFrame.
        """
        def highlight_diffs(data):
            color = 'background-color: yellow'
            df_styler = pd.DataFrame('', index=data.index, columns=data.columns)
            for col in self.df1.columns:
                df_styler.loc[differences[col] & rows_with_differences, f'{col}_source'] = color
                df_styler.loc[differences[col] & rows_with_differences, f'{col}_target'] = color
            return df_styler

        return diff.style.apply(highlight_diffs, axis=None)
