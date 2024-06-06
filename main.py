import pandas as pd
from scripts.logging_config import get_logger
from scripts.get_config import get_config

logger = get_logger()

source_file = get_config('INPUTS', 'SOURCE_FILE')
target_file = get_config('INPUTS', 'TARGET_FILE')

source_df = pd.read_csv(source_file)
target_df = pd.read_csv(target_file)

# Check counts
source_record_count = source_df.shape[0]
target_record_count = target_df.shape[0]
logger.info(f'Source record count: {source_record_count}')
logger.info(f'Target record count: {target_record_count}')
if source_record_count == target_record_count:
    logger.info('Counts are the same')
else:
    logger.warning('Counts are different')

# Check columns
source_col_count = source_df.columns
target_col_count = target_df.columns
logger.info(f'Source columns: {len(source_col_count)}')
logger.info(f'Target columns: {len(target_col_count)}')
if len(source_col_count) == len(target_col_count):
    logger.info('Column counts are the same.')
else:
    logger.warning('Column counts are different.')

missing_source_cols = set(source_col_count) - set(target_col_count)
missing_target_cols = set(target_col_count) - set(source_col_count)

if missing_source_cols:
    logger.warning(f"Columns missing in DataFrame 1: {missing_source_cols}")
if missing_target_cols:
    logger.warning(f"Columns missing in DataFrame 2: {missing_target_cols}")

if not missing_source_cols and not missing_target_cols:
    logger.info("All columns match")

# Merge the two dataframes, indicator=True adds a column '_merge' that indicates where the merge matched
merged_df = pd.merge(source_df, target_df, how='outer', indicator=True)

# Rows that are only in source_df or only in target_df
diff_df = merged_df[merged_df['_merge'] != 'both']

pd.DataFrame.to_html(diff_df, 'assets/outputs/diff.html')
