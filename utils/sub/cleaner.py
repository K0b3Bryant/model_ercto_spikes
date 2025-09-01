import pandas as pd
import numpy as np
import re

def cleaner(df: pd.DataFrame, handle_outliers: bool = True, fill_method: str = "ffill") -> pd.DataFrame:
    """ Cleans DataFrame. """
    
    df = df.copy()
    
    # --- Standardize column names ---
    def to_snake_case(s):
        return re.sub(r'[^0-9a-zA-Z]+', '_', s).strip('_').lower()
    
    df.columns = [to_snake_case(col) for col in df.columns]

     # --- Strip whitespace in string columns ---
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()
        
    # --- Remove duplicates ---
    def choose_row(group):
        # Keep first row that is not fully empty
        non_empty = group.dropna(how='all')
        if not non_empty.empty:
            return non_empty.iloc[0]
        else:
            return group.iloc[0]  # all empty, keep first

    df = df.groupby(df.index, group_keys=False).apply(choose_row)
    
    # --- Handle outliers ---
    if handle_outliers:
        for col in df.select_dtypes(include=[np.number]).columns:
            lower, upper = df[col].quantile([0.01, 0.99])
            df[col] = df[col].clip(lower, upper)
    
    # --- Handle missing values ---
    if fill_method in ["ffill", "bfill"]:
        df = df.fillna(method=fill_method)
        
    # --- Convert datetime-like columns ---
    for col in df.columns:
        if df[col].dtype == object:
            try:
                df[col] = pd.to_datetime(df[col], errors="ignore")
            except Exception:
                pass
    
    return df
