import pandas as pd

def add_last_finish(df):
    '''
    Add column of recent race results

    Incoming dataframe from get_season_results() looks like
    index|DriverNumber|RoundNumber|Position
    '''
    df["last_finish"] = (
        df.groupby("DriverNumber")["Position"]
        .shift(1)
    )

    return df