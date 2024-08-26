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
  return np.sqrt(np.mean((test_data - predictions)**2))
# Model training and forecasting functions
# def train_arima(train_data, test_data):
#     model = auto_arima(train_data)
#     predictions = model.predict(n_periods=len(test_data))
#     mse = RMSE(test_data, predictions)
#     return predictions, mse

# def train_theta(train_data, test_data):
#     theta_constant = np.mean(train_data)
#     theta_predictions = [theta_constant] * len(test_data)
#     mse = RMSE(test_data, theta_predictions)
#     return theta_predictions, mse
def default_model(data, predict_len):
    return train_score_predict_prophet(data, predict_len)



def train_score_predict_prophet(data, predict_len=3, model_parameters={}):
    data = data.reset_index().rename(columns={'Months': 'ds', 'Demand': 'y'})

    model = Prophet(**model_parameters)
    train_df = data[:-1*predict_len]
    test_data = data[predict_len:]
    model.fit(train_df)
    future = model.make_future_dataframe(periods=len(test_data), freq='MS')
    forecast = model.predict(future)
    test_predictions = forecast['yhat'][-len(test_data):].values
    rmse = RMSE(test_data['y'], test_predictions)

    model = Prophet(**model_parameters)
    model.fit(pd.concat([data[predict_len+1:]]))
    future = model.make_future_dataframe(periods=predict_len, freq='MS')
    forecast = model.predict(future)
    predictions = forecast['yhat'][-predict_len:].values
    return predictions, rmse


def export_model():
    pass


def train_model():
    pass
    # with open(MODEL_PATH, 'wb') as f:
    #     pickle.dump(model, f)
    # pass



def predict():

    # with open(MODEL_PATH, 'rb') as f:
    #     model = pickle.load(f)
    # model.predict()

    return {}
