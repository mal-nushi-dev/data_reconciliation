import pandas as pd
from modules.get_config import get_config
from modules.dataframe_manager import DataFrameValidator


def main():
    # Initialize files
    source_file = get_config('INPUTS', 'SOURCE_FILE')
    target_file = get_config('INPUTS', 'TARGET_FILE')

    # Create dataframes
    source_df = pd.read_csv(source_file)
    target_df = pd.read_csv(target_file)

    validator = DataFrameValidator(source_df, target_df)
    validator.validate()


if __name__ == ("__main__"):
    main()
