import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

def train_RFR_model(df):
    '''
    Returns trained RandomForestRegressor model

    Incoming DataFrame:
    DriverNumber|Season|RoundNumber|TeamName|Position|QualiPosition|FastestTime|LastFinish|RollingAverage3|RollingStd3|Delta
    '''
    # data = pd.read_csv('data/F1_model_data.csv')

    X_teamnames = df[['DriverNumber', 'TeamName', 'QualiPosition', 'LastFinish', 'RollingAverage3', 'RollingStd3', 'Delta']]
    y = df['Position']

    X = pd.get_dummies(X_teamnames, columns=['TeamName'])

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    error = mean_absolute_error(y_test, predictions)

    print(f'Model trained. Error of {error}')

    return model, X_test, y_test