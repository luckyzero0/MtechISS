import pickle
import pandas as pd
import numpy as np

from prophet import Prophet


def import_model():
    pass


def MAPE(test_data, predictions):
    test_data, predictions = np.array(test_data), np.array(predictions)
    return np.mean(np.abs((test_data - predictions) / test_data)) * 100


def RMSE(test_data, predictions):
    test_data, predictions = np.array(test_data), np.array(predictions)
    return np.sqrt(np.mean((test_data - predictions) ** 2))


# Model training and forecasting functions
def train_predict_arima(train_data, test_data, evaluate=True):
    from pmdarima.arima import auto_arima
    model = auto_arima(train_data)
    predictions = model.predict(n_periods=len(test_data))
    if evaluate == True:
        rmse = RMSE(test_data, predictions)
        return predictions, rmse
    else:
        return predictions, None


def train_predict_baseline(train_data, test_data, evaluate=True):
    mean_value = np.mean(train_data)
    predictions = [mean_value] * len(test_data)
    if evaluate == True:
        rmse = RMSE(test_data, predictions)
        return predictions, rmse
    else:
        return predictions, None


def train_predict_theta(train_data, test_data, evaluate=True):
    from statsmodels.tsa.forecasting.theta import ThetaModel
    model = ThetaModel(train_data, period=12)
    res = model.fit()
    predictions = res.forecast(len(test_data))
    if evaluate == True:
        rmse = RMSE(test_data, predictions)
        return predictions, rmse
    else:
        return predictions, None


def get_best_prediction(data, predict_len, config=None):
    if config is None:
        config = {'prophet': {'model_type': 'prophet'},
                  'theata': {'model_type': 'theata'},
                  'arima': {'model_type': 'arima'},
                  'baseline': {'model_type': 'baseline'}}
    output = config.copy()
    for k, v in output.items():
        v['predictions'], v['rmse'] = train_score_predict(data, predict_len, model_type=v.get('model_type', ''))
        print(f"Completed {k} Model: {v['rmse']}")
    best_model = min(output, key=lambda k: output[k]['rmse'])
    print(f"Best Model: {best_model}")
    print()
    return output[best_model]['predictions'], output[best_model]['rmse']

def train_score_predict(data, predict_len=3, model_parameters={}, model_type='prophet'):
    data = data.reset_index().rename(columns={'Months': 'ds', 'Demand': 'y'})
    train_data = data[:-1 * predict_len]
    test_data = data[-1 * predict_len:]
    train_data_second = data[predict_len + 1:]
    test_data_second = ['placeholder'] * predict_len

    # Model Training
    if model_type == 'prophet':
        model = Prophet(**model_parameters)
        model.fit(train_data)
        future = model.make_future_dataframe(periods=len(test_data), freq='MS')
        forecast = model.predict(future)
        test_predictions = forecast['yhat'][-len(test_data):].values
        rmse = RMSE(test_data['y'], test_predictions)
        model = Prophet(**model_parameters)
        model.fit(train_data_second)
        future = model.make_future_dataframe(periods=predict_len, freq='MS')
        forecast = model.predict(future)
        predictions = forecast['yhat'][-predict_len:].values


    elif model_type == 'arima':
        _, rmse = train_predict_arima(train_data['y'], test_data['y'], evaluate=True)
        predictions, _ = train_predict_arima(train_data_second['y'], test_data_second, evaluate=False)

    elif model_type == 'theata':
        _, rmse = train_predict_theta(train_data['y'], test_data['y'], evaluate=True)
        predictions, _ = train_predict_arima(train_data_second['y'], test_data_second, evaluate=False)

    elif model_type == 'baseline':
        _, rmse = train_predict_baseline(train_data['y'], test_data['y'], evaluate=True)
        predictions, _ = train_predict_arima(train_data_second['y'], test_data_second, evaluate=False)

    return predictions, rmse
