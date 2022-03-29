"""KNN Prediction Model"""
__docformat__ = "numpy"

import logging
from typing import Any, Tuple, Union

import numpy as np
import pandas as pd
from sklearn import neighbors

from openbb_terminal.common.prediction_techniques.pred_helper import (
    prepare_scale_train_valid_test,
)
from openbb_terminal.decorators import log_start_end
from openbb_terminal.helper_funcs import get_next_stock_market_days
from openbb_terminal.rich_config import console

logger = logging.getLogger(__name__)


@log_start_end(log=logger)
def get_knn_model_data(
    data: Union[pd.Series, pd.DataFrame],
    n_input_days: int,
    n_predict_days: int,
    n_neighbors: int,
    test_size: float,
    end_date: str,
    no_shuffle: bool,
) -> Tuple[pd.DataFrame, np.ndarray, np.ndarray, np.ndarray, Any]:
    """Perform knn model fitting and predicting on data

    Parameters
    ----------
    data : Union[pd.Series, pd.DataFrame]
        Data to fit
    n_input_days : int
        Length of input series
    n_predict_days : int
        Number of days to predict
    n_neighbors : int
        Number of neighbors for nn
    test_size : float
        Fraction of data for testing
    end_date : str
        End date for backtesting
    no_shuffle : bool
        Flag to not shuffle train/test data

    Returns
    -------
    pd.DataFrame:
        Dataframe of preditions
    np.array:
        Array of validation predictions
    np.array:
        Array of validation data
    np.array:
        Array of validation dates
    Any:
        Scaler for processing data
    """
    (
        X_train,
        X_valid,
        y_train,
        y_valid,
        _,
        _,
        _,
        y_dates_valid,
        forecast_data_input,
        dates_forecast_input,
        scaler,
        is_error,
    ) = prepare_scale_train_valid_test(
        data, n_input_days, n_predict_days, test_size, end_date, no_shuffle
    )
    if is_error:
        return pd.DataFrame(), np.array(0), np.array(0), np.array(0), None

    future_dates = get_next_stock_market_days(
        dates_forecast_input[-1], n_next_days=n_predict_days
    )
    console.print(
        f"Training on {X_train.shape[0]} sequences of length {X_train.shape[1]}.  Using {X_valid.shape[0]} sequences "
        f" of length {X_valid.shape[1]} for validation"
    )
    # Machine Learning model
    knn = neighbors.KNeighborsRegressor(n_neighbors=n_neighbors)
    knn.fit(
        X_train.reshape(X_train.shape[0], X_train.shape[1]),
        y_train.reshape(y_train.shape[0], y_train.shape[1]),
    )

    preds = knn.predict(X_valid.reshape(X_valid.shape[0], X_valid.shape[1]))
    forecast_data = knn.predict(forecast_data_input.reshape(1, -1))
    forecast_data = scaler.inverse_transform(forecast_data.reshape(1, -1))
    forecast_data_df = pd.DataFrame(list(forecast_data.T), index=future_dates)

    return forecast_data_df, preds, y_valid, y_dates_valid, scaler
