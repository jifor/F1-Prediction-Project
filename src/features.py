import pandas as pd

def add_last_finish(df):
    '''
    Add column of recent race results

    Has NaN for first race; for now will use imputer but I could use the previous season's results

    Incoming dataframe from get_season_results() looks like
    index|DriverNumber|RoundNumber|Position
    '''
    df["LastFinish"] = (
        df.groupby("DriverNumber")["Position"]
        .shift(1)
    )

    return df

def add_rolling_3_avg(df):
    '''
    Add a column with a rolling 3 race position average to dataframe

    Incoming dataframe looks like
    index|DriverNumber|RoundNumber|Position|...
    '''

    df = df.sort_values(["DriverNumber", "RoundNumber"])

    # Compute the rolling average of last 3 finish positions. This is from ChatGPT lol :p
    # .fillna(df['Position'] fill the NaN from the first race of each season with current position. Not the best method but works okay
    df['RollingAverage3'] = df.groupby('DriverNumber')['Position'].transform(lambda x: x.shift(1).rolling(3, min_periods=1).mean()).fillna(df['Position'])

    return df

def add_3_race_consistency(df):
    '''
    Add a column with a rolling 3 race standard deviation of Position

    Incoming dataframe looks like
    index|DriverNumber|RoundNumber|Position|...
    '''

    df = df.sort_values(['DriverNumber', 'RoundNumber'])

    df['RollingStd3'] = df.groupby('DriverNumber')['Position'].transform(lambda x: x.shift(1).rolling(3, min_periods=2).std()).fillna(0)
    
    return df

def add_rolling_5_avg(df):
    return 0

def add_results_features(df):


    return df