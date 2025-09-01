import pandas as pd
import numpy as np
import re

def cleaner(df: pd.DataFrame, handle_outliers: bool = True, fill_method: str = None) -> pd.DataFrame:
    """
    Cleans and prepares a pandas DataFrame for analysis.
    
    Steps:
        - Standardizes column names (snake_case).
        - Removes duplicate rows.
        - Strips whitespace from string/object columns.
        - Fills missing values (numeric → median, categorical → mode) or forward/backward fill.
        - Optionally handles outliers (clipping to 1st and 99th percentile).
        - Converts date-like columns to datetime.
    
    Parameters
    ----------
    df : pd.DataFrame
        Input DataFrame to clean.
    handle_outliers : bool, optional
        If True, numeric columns are clipped to [1st, 99th] percentile.
    fill_method : str, optional
        If 'ffill', missing values are forward-filled.
        If 'bfill', missing values are backward-filled.
        If None, numeric → median, categorical → mode.
    
    Returns
    -------
    pd.DataFrame
        Cleaned DataFrame.
    """
    
    df = df.copy()
    
    # --- Standardize column names ---
    def to_snake_case(s):
        return re.sub(r'[^0-9a-zA-Z]+', '_', s).strip('_').lower()
    
    df.columns = [to_snake_case(col) for col in df.columns]
    
    # --- Remove duplicates ---
    df = df.drop_duplicates()
    
    # --- Strip whitespace in string columns ---
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()
    
    # --- Handle missing values ---
    if fill_method in ["ffill", "bfill"]:
        df = df.fillna(method=fill_method)
    else:
        for col in df.columns:
            if df[col].dtype in [np.float64, np.int64]:
                df[col] = df[col].fillna(df[col].median())
            else:
                mode = df[col].mode()
                if not mode.empty:
                    df[col] = df[col].fillna(mode[0])
    
    # --- Handle outliers ---
    if handle_outliers:
        for col in df.select_dtypes(include=[np.number]).columns:
            lower, upper = df[col].quantile([0.01, 0.99])
            df[col] = df[col].clip(lower, upper)
    
    # --- Convert datetime-like columns ---
    for col in df.columns:
        if df[col].dtype == object:
            try:
                df[col] = pd.to_datetime(df[col], errors="ignore")
            except Exception:
                pass
    
    return df
