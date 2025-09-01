from functools import reduce
import pandas as pd

def merger(dfs: list[pd.DataFrame], on_cols: list[dict], how: str = "inner") -> pd.DataFrame:
    """ Merge multiple DataFrames. """

    # Failsafe
    if len(dfs) - 1 != len(on_cols):
        raise ValueError("Length of on_cols must be len(dfs) - 1")

    # Merge
    merged_df = dfs[0]
    
    for i in range(1, len(dfs)):
        left_col = on_cols[i-1]['left']
        right_col = on_cols[i-1]['right']
        merged_df = pd.merge(merged_df, dfs[i], left_on=left_col, right_on=right_col, how=how)
    
    return merged_df
    
    
