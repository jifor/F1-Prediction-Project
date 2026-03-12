import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

def train_RFR_model():
    '''
    Train RandomForestRegressor model

    Returns model, array of predictions from the model, and error of the predictions to test data
    '''
    data = pd.read_csv('data/F1_model_data.csv')

    X = data[['DriverNumber', 'QualiPosition', 'LastFinish', 'RollingAverage3', 'RollingStd3', 'Delta']]
    y = data['Position']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    error = mean_absolute_error(y_test, predictions)

    return model, predictions, error