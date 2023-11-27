import pandas as pd
import numpy as np
import xgboost as xgb

from typing import Tuple, Union, List
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle
from sklearn.metrics import confusion_matrix, classification_report

from .utils import get_period_day, is_high_season, get_min_diff, get_TOP_10_FEATURES


class DelayModel:

    def __init__(
        self
    ):
        self._model = None # Model should be saved in this attribute.

    def preprocess(
        self,
        data: pd.DataFrame,
        target_column: str = None
    ) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
        """
        Prepare raw data for training or predict.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """
        data['period_day'] = data['Fecha-I'].apply(get_period_day)
        data['high_season'] = data['Fecha-I'].apply(is_high_season)
        data['min_diff'] = data.apply(get_min_diff, axis = 1)

        data_suffle_keys = ['OPERA', 'MES', 'TIPOVUELO', 'SIGLADES', 'DIANOM']
        if target_column is not None:
            threshold_in_minutes = 15
            data[target_column] = pd.DataFrame(
                {target_column: np.where(data['min_diff'] > threshold_in_minutes, 1, 0)}
            )
            data_suffle_keys.append(target_column)

        training_data = shuffle(data[data_suffle_keys], random_state = 111)
        features = pd.concat([
            pd.get_dummies(training_data['OPERA'], prefix = 'OPERA'),
            pd.get_dummies(training_data['TIPOVUELO'], prefix = 'TIPOVUELO'), 
            pd.get_dummies(training_data['MES'], prefix = 'MES')], 
            axis = 1
        )[get_TOP_10_FEATURES()]

        if target_column is not None:
            target = training_data[target_column]
            return features, target.to_frame()
        else:
            return features

    def fit(
        self,
        features: pd.DataFrame,
        target: pd.DataFrame
    ) -> None:
        """
        Fit model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        """
        x_train, _, y_train, _ = train_test_split(features, target.iloc[:,0] , test_size = 0.33, random_state = 42)

        # Data balance
        n_y0 = len(y_train[y_train == 0])
        n_y1 = len(y_train[y_train == 1])
        scale = n_y0/n_y1

        self._model = xgb.XGBClassifier(random_state=1, learning_rate=0.01, scale_pos_weight = scale)
        self._model.fit(x_train, y_train)

        return

    def predict(
        self,
        features: pd.DataFrame
    ) -> List[int]:
        """
        Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.
        
        Returns:
            (List[int]): predicted targets.
        """
        xgboost_y_preds = self._model.predict(features)
        return [1 if y_pred > 0.5 else 0 for y_pred in xgboost_y_preds]
