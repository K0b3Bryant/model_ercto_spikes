def feature_importance(self, X):
  """ Displays features importance. """
  
  importance_data = []

  ### NEEDS ADJUSTMENTS HERE
  for model_name, model in self.models.items():
    if hasattr(model.model, 'feature_importances_'):
        importances = model.model.feature_importances_
        features = X.columns
        sorted_indices = importances.argsort()[::-1][:5]
        for idx in sorted_indices:
            importance_data.append({
                'Model': model_name,
                'Feature': features[idx],
                'Importance': importances[idx]
            })
    elif hasattr(model.model, 'coef_'):
        importances = np.abs(model.model.coef_).ravel()
        features = X.columns
        sorted_indices = importances.argsort()[::-1][:5]
        for idx in sorted_indices:
            importance_data.append({
                'Model': model_name,
                'Feature': features[idx],
                'Importance': importances[idx]
            })
    else:
        print(f"{model_name} does not support feature importance.")
