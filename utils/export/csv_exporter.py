def export_csv(df: pd.DataFrame, filename: str):
    """ Exports csv. """
    df.to_csv(f"{filename}.csv", index=False)
