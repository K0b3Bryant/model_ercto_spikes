def lagger(self, df: pd.DataFrame, lags: list = [2]):
  """ Lags df multiple times. """
  
  features = []
  for lag in lags:
      df_lag = df.shift(lag)
      df_lag.columns = [f"{col}_l({lag})" for col in df.columns]
      features.append(df_lag)
  return pd.concat(features, axis=1)
