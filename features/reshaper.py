def reshape_for_lstm(X, sequence_length):
  """ Reshapes for LSTM """
  X_lstm = []
  for i in range(sequence_length, len(X)):
      X_lstm.append(X[i-sequence_length:i].values)
  return np.array(X_lstm)
