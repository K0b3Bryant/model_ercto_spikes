def separator(df:pd.DataFrame, col: str):
  """ Separates data into sets depending on unique values of a specified column. """

  sets = {}
  
  for value in df[col].unique():
      sets[value] = df[df[col] == value].copy()
      
  return sets
