""" Neural Networks View"""
__docformat__ = "numpy"

import logging
from typing import Union

import numpy as np
import pandas as pd

from openbb_terminal.common.prediction_techniques import neural_networks_model
from openbb_terminal.common.prediction_techniques.pred_helper import (
    plot_data_predictions,
    print_pretty_prediction,
)
from openbb_terminal.decorators import log_start_end
from openbb_terminal.rich_config import console

# pylint:disable=too-many-arguments


logger = logging.getLogger(__name__)


@log_start_end(log=logger)
def display_mlp(
    dataset: str,
    data: Union[pd.Series, pd.DataFrame],
    n_input_days: int,
    n_predict_days: int,
    learning_rate: float,
    epochs: int,
    batch_size: int,
    test_size: float,
    n_loops: int,
    no_shuffle: bool,
    time_res: str = "",
):
    """Display trained MLP model

    Parameters
    ----------
    dataset : str
        Dataset for model
    data : Union[pd.Series, pd.DataFrame]
        Data to feed to model
    n_input_days : int
        Number of inputs to train
    n_predict_days : int
        Number of outputs to predict
    learning_rate : float
        MLP learning rate
    epochs : int
        Number of training epochs
    batch_size : int
        Training batch size
    test_size : float
        Size of test set
    n_loops : int
        Number of loops to perform for model
    no_shuffle : bool
        Flag to not randomly shuffle data
    time_res : str
        Resolution for data, allowing for predicting outside of standard market days
    """
    (
        forecast_data_df,
        preds,
        y_valid,
        y_dates_valid,
        scaler,
    ) = neural_networks_model.mlp_model(
        data,
        n_input_days,
        n_predict_days,
        learning_rate,
        epochs,
        batch_size,
        test_size,
        n_loops,
        no_shuffle,
    )

    if time_res:
        forecast_data_df.index = pd.date_range(
            data.index[-1], periods=n_predict_days + 1, freq=time_res
        )[1:]

    if n_loops > 1:
        forecast_data_df["Median"] = forecast_data_df.median(axis=1)
        print_pretty_prediction(forecast_data_df["Median"], data.values[-1])
    else:
        print_pretty_prediction(forecast_data_df[0], data.values[-1])
    plot_data_predictions(
        data,
        np.median(preds, axis=0),
        y_valid,
        y_dates_valid,
        scaler,
        f"MLP Model on {dataset}",
        forecast_data_df,
        n_loops,
        time_res,
    )
    console.print("")


@log_start_end(log=logger)
def display_rnn(
    dataset: str,
    data: Union[pd.Series, pd.DataFrame],
    n_input_days: int,
    n_predict_days: int,
    learning_rate: float,
    epochs: int,
    batch_size: int,
    test_size: float,
    n_loops: int,
    no_shuffle: bool,
    time_res: str = "",
):
    """Display trained RNN model

    Parameters
    ----------
    dataset : str
        Dataset for model
    data : Union[pd.Series, pd.DataFrame]
        Data to feed to model
    n_input_days : int
        Number of inputs to train
    n_predict_days : int
        Number of outputs to predict
    learning_rate : float
        MLP learning rate
    epochs : int
        Number of training epochs
    batch_size : int
        Training batch size
    test_size : float
        Size of test set
    n_loops : int
        Number of loops to perform for model
    no_shuffle : bool
        Flag to not randomly shuffle data
    time_res : str
        Resolution for data, allowing for predicting outside of standard market days
    """

    (
        forecast_data_df,
        preds,
        y_valid,
        y_dates_valid,
        scaler,
    ) = neural_networks_model.rnn_model(
        data,
        n_input_days,
        n_predict_days,
        learning_rate,
        epochs,
        batch_size,
        test_size,
        n_loops,
        no_shuffle,
    )
    if time_res:
        forecast_data_df.index = pd.date_range(
            data.index[-1], periods=n_predict_days + 1, freq=time_res
        )[1:]
    if n_loops > 1:
        forecast_data_df["Median"] = forecast_data_df.median(axis=1)
        print_pretty_prediction(forecast_data_df["Median"], data.values[-1])
    else:
        print_pretty_prediction(forecast_data_df[0], data.values[-1])
    plot_data_predictions(
        data,
        np.median(preds, axis=0),
        y_valid,
        y_dates_valid,
        scaler,
        f"RNN Model on {dataset}",
        forecast_data_df,
        n_loops,
        time_res,
    )
    console.print("")


@log_start_end(log=logger)
def display_lstm(
    dataset: str,
    data: Union[pd.Series, pd.DataFrame],
    n_input_days: int,
    n_predict_days: int,
    learning_rate: float,
    epochs: int,
    batch_size: int,
    test_size: float,
    n_loops: int,
    no_shuffle: bool,
    time_res: str = "",
):
    """Display trained LSTM model

    Parameters
    ----------
    dataset : str
        Dataset for model
    data : Union[pd.Series, pd.DataFrame]
        Data to feed to model
    n_input_days : int
        Number of inputs to train
    n_predict_days : int
        Number of outputs to predict
    learning_rate : float
        MLP learning rate
    epochs : int
        Number of training epochs
    batch_size : int
        Training batch size
    test_size : float
        Size of test set
    n_loops : int
        Number of loops to perform for model
    no_shuffle : bool
        Flag to not randomly shuffle data
    time_res : str
        Resolution for data, allowing for predicting outside of standard market days
    """

    (
        forecast_data_df,
        preds,
        y_valid,
        y_dates_valid,
        scaler,
    ) = neural_networks_model.lstm_model(
        data,
        n_input_days,
        n_predict_days,
        learning_rate,
        epochs,
        batch_size,
        test_size,
        n_loops,
        no_shuffle,
    )
    if time_res:
        forecast_data_df.index = pd.date_range(
            data.index[-1], periods=n_predict_days + 1, freq=time_res
        )[1:]
    if n_loops > 1:
        forecast_data_df["Median"] = forecast_data_df.median(axis=1)
        print_pretty_prediction(forecast_data_df["Median"], data.values[-1])
    else:
        print_pretty_prediction(forecast_data_df[0], data.values[-1])
    plot_data_predictions(
        data,
        np.median(preds, axis=0),
        y_valid,
        y_dates_valid,
        scaler,
        f"LSTM Model on {dataset}",
        forecast_data_df,
        n_loops,
        time_res,
    )
    console.print("")


@log_start_end(log=logger)
def display_conv1d(
    dataset: str,
    data: Union[pd.Series, pd.DataFrame],
    n_input_days: int,
    n_predict_days: int,
    learning_rate: float,
    epochs: int,
    batch_size: int,
    test_size: float,
    n_loops: int,
    no_shuffle: bool,
    time_res: str = "",
):
    """Display trained Conv1D model

    Parameters
    ----------
    dataset : str
        Dataset for model
    data : Union[pd.Series, pd.DataFrame]
        Data to feed to model
    n_input_days : int
        Number of inputs to train
    n_predict_days : int
        Number of outputs to predict
    learning_rate : float
        MLP learning rate
    epochs : int
        Number of training epochs
    batch_size : int
        Training batch size
    test_size : float
        Size of test set
    n_loops : int
        Number of loops to perform for model
    no_shuffle : bool
        Flag to not randomly shuffle data
    time_res : str
        Resolution for data, allowing for predicting outside of standard market days
    """

    (
        forecast_data_df,
        preds,
        y_valid,
        y_dates_valid,
        scaler,
    ) = neural_networks_model.conv1d_model(
        data,
        n_input_days,
        n_predict_days,
        learning_rate,
        epochs,
        batch_size,
        test_size,
        n_loops,
        no_shuffle,
    )
    if time_res:
        forecast_data_df.index = pd.date_range(
            data.index[-1], periods=n_predict_days + 1, freq=time_res
        )[1:]
    if n_loops > 1:
        forecast_data_df["Median"] = forecast_data_df.median(axis=1)
        print_pretty_prediction(forecast_data_df["Median"], data.values[-1])
    else:
        print_pretty_prediction(forecast_data_df[0], data.values[-1])
    plot_data_predictions(
        data,
        np.median(preds, axis=0),
        y_valid,
        y_dates_valid,
        scaler,
        f"Conv1D Model on {dataset}",
        forecast_data_df,
        n_loops,
        time_res,
    )
    console.print("")
