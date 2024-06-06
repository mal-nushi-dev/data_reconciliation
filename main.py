import pandas as pd
from scripts.get_config import get_config
from scripts.dataframe_manager import row_count_validation, column_validation, data_validation


def main():
    # Initialize files
    source_file = get_config('INPUTS', 'SOURCE_FILE')
    target_file = get_config('INPUTS', 'TARGET_FILE')

    # Create dataframes
    source_df = pd.read_csv(source_file)
    target_df = pd.read_csv(target_file)

    # Check counts
    row_count_validation(source_df, target_df)

    # Check columns
    column_validation(source_df, target_df)
    data_validation(source_df, target_df)


if __name__ == ("__main__"):
    main()
