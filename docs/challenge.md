### Part I

## Jupyter notebook

- Fixed syntax errors in the `sns.barplot` function that now receives X and Y as parameters instead of two positional arguments

- Changed from `data` to `training_data` in the creation (`suffle`) of the features and targets, to be able to take samples for training and testing randomly

- All notebook was executed successfully

- Although the models give very similar results, it was chosen to use an XGBoost classifier since logistic regression assumes a linear relationship between the characteristics and the logarithmic probabilities of the target variable. If the relationship is very nonlinear, the logistic regression may not capture it effectively and in this case the probability of a delayed flight does not assume a priori a linear relationship. Instead, XGBoost is an ensemble learning method that can capture complex nonlinear relationships between features and the target. It can handle interactions between functions more effectively, making it much more suitable for this example.

## Tests

- The csv path to load `data` was corrected
- The `test_model_predict` test fails with the error `AttributeError: 'NoneType' object has no attribute 'predict'` since the model is not being trained before predicting, so internally the model does not yet exist and is `None`
- Regarding the choice of the test, it was also tested with a logistic regression and within the test `test_model_fit` the expected parameters were not reached.
