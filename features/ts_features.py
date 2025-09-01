def ts_features(df:pd.DataFrame, underlying:str, max_timeshift:int = 3, min_timeshift:int = 3) --> pd.DataFrame:
  """ Generates tsfresh features """
  
  # Failsafe
  if underlying not in df.columns:
      raise ValueError(f"Column '{underlying}' not found in DataFrame.")
  
  features = pd.DataFrame({'date': df.index, f'{underlying}': df[underlying], 'id': 1}).reset_index(drop=True)
  roller = roll_time_series(features, column_id="id", column_sort="date", min_timeshift=min_timeshift, max_timeshift=max_timeshift, rolling_direction=1)
  roller = roller.fillna(0)
  logging.basicConfig(level=logging.INFO)
  extracted_features = extract_features(roller, column_id='id', column_sort='date', column_value=underlying, impute_function=impute, show_warnings=False, n_jobs=1) #n_jobs=1
  extracted_features.index = extracted_features.index.droplevel(0)
  extracted_features.index.name = 'date'
  
  return extracted_features

