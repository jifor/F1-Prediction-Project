import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib
from data_loading import (
    get_most_recent_event
)

def train_RFR_model(df):
    '''
    Returns trained RandomForestRegressor model

    Incoming DataFrame:
    DriverNumber|Season|RoundNumber|TeamName|Position|QualiPosition|FastestTime|LastFinish|RollingAverage3|RollingStd3|Delta
    '''
    # data = pd.read_csv('data/F1_model_data.csv')

    df_train = df[df['Season'] != 2025]
    df_test = df[df['Season'] == 2025]

    feature_cols = ['DriverNumber', 'TeamName', 'QualiPosition', 'LastFinish', 'RollingAverage3', 'RollingStd3', 'Delta']
    X_train_teamnames = df_train[feature_cols]
    X_test_teamnames = df_test[feature_cols]
    y_train = df_train['Position']
    y_test = df_test['Position']

    X_train = pd.get_dummies(X_train_teamnames, columns=['TeamName'])
    X_test = pd.get_dummies(X_test_teamnames, columns=['TeamName'])
    X_test = X_test.reindex(columns=X_train.columns, fill_value=0)

    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    error = mean_absolute_error(y_test, predictions)

    print(f'Model trained. Error of {error}')

    return model, X_test, y_test

def make_prediction_dataframe():

    # get the most recent event and load the quali results
    event = get_most_recent_event()
    quali = event.get_qualifying()
    quali.load(telemetry=False, weather=False)

    return 0

def predict_winner():

    df = make_prediction_dataframe()

    model = joblib.load('model.pkl')
    predictions = model.predict(df)

    winner = get_winner(predictions)

    return 0