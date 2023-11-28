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


### Part II

- The model was saved in a file in `./challenge/xgb_model.joblib`

- The `predict` endpoint was completed, as well as classes for validation of the input data and auxiliary functions for data management.

- Requirements: 
Running the tests the following error was found
`AttributeError: module 'anyio' has no attribute 'start_blocking_portal'`
The error was within the startlette module version 0.20.4, to update it the fastapi version had to be updated since the current 0.86.0 depended on it.
The latest version of fastapi (0.104.1) was installed. As well as the latest version of httpx (0.25.2) which emerged as a new requirement due to the upgrade.

- The tests were executed successfully 




### Part III

- Dockerfile was created and built locally

- Docker container was started locally

- Requirements modifications:
locust 1.6 requires Flask 1.1.2, and this old version of flask is causing the following problem
#ImportError: cannot import name 'escape' from 'jinja2'
Locust was updated to 2.19.1, with that Flask was updated
Which led to the following error, ImportError: cannot import name 'url_quote' from 'werkzeug.urls'
Which was fixed by downgrading the Werkzeug library to 2.2.2

- The url of the local container was entered and `make stress-test` was executed successfully.

- The GCP configuration was not completed, nor the deployment of the API in the cloud
