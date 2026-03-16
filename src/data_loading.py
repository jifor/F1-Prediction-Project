import fastf1 as ff1
import pandas as pd
import cache_path as cache # path to cache in cache_path.py; in .gitignore

def get_events_in_season(year):
    '''
    Get the number of events in a season
    '''
    ff1.Cache.enable_cache(cache.cache_path)

    schedule = ff1.get_event_schedule(year, include_testing=False) # doesn't seem to return races that were cancelled 

    return len(schedule.index) 

def get_loaded_session(season_year, round_num, session_type='R'):
    '''
    Return loaded session
    '''
    ff1.Cache.enable_cache(cache.cache_path)

    session = ff1.get_session(season_year, round_num, session_type)
    session.load()

    return session

def get_race_results(season_year=None, round_number=None, session=None):
    '''
    Returns DataFrame with results from a race session. Can take in either session information or a loaded session.

    DataFrame:
    DriverNumber|RoundNumber|TeamName|Position
    '''
    if session is None:
        if season_year is None or round_number is None:
            raise ValueError('Need either a loaded session or session information')
        session = get_loaded_session(season_year, round_number, session_type='R')

    result = session.results['ClassifiedPosition']
    team = session.results['TeamName']
    result.index = result.index.astype(int)
    # Replace 'R', 'D', 'W' with 20
    result = pd.to_numeric(result, errors="coerce").fillna(20) # temporary, need a way to fix DSQs

    race_df = pd.DataFrame({
        "DriverNumber": result.index,
        "RoundNumber": session.event['RoundNumber'],
        "TeamName": team,
        "Position": result.values
    })

    race_df = race_df.sort_values('DriverNumber')

    return race_df

def get_quali_results(season_year=None, round_number=None, session=None):
    '''
    Returns DataFrame with results from a qualifying session. Can take in either session information or a loaded session.

    DataFrame:
    DriverNumber|RoundNumber|QualiPosition 
    '''
    if session is None:
        if season_year is None or round_number is None:
            raise ValueError('Need either a loaded session or session information')
        session = get_loaded_session(season_year, round_number, session_type='Q')   

    result = session.results['Position']
    result.index = result.index.astype(int)
    # Fill missing values with 20 because no quali result means they would start at the end
    result = pd.to_numeric(result, errors="coerce").fillna(20)

    qual_df = pd.DataFrame({
        "DriverNumber": result.index,
        "RoundNumber": session.event['RoundNumber'],
        "QualiPosition": result.values
    })

    qual_df = qual_df.sort_values('DriverNumber')

    return qual_df

def get_quali_times(season_year=None, round_number=None, session=None):
    '''
    Get the fastest times for each driver in a qualifying session. Can take either session information or a loaded session.

    Returns
    DriverNumber|RoundNumber|FastestTime
    '''
    if session is None:
        if season_year is None or round_number is None:
            raise ValueError('Need either a loaded session or session information')
        session = get_loaded_session(season_year, round_number, session_type='Q')

    rows = []
    for driver in session.drivers:
        lap = session.laps.pick_drivers(int(driver)).pick_fastest()
        if lap is None:  # handle laps that return None
            continue 
        else:
            time = lap['LapTime']
            rows.append({
                'DriverNumber': int(driver),
                'RoundNumber': session.event['RoundNumber'],
                'FastestTime': time
            })

    qual_times = pd.DataFrame(rows)
    qual_times['FastestTime'] = qual_times['FastestTime'].dt.total_seconds()
    return qual_times

# def get_rain_in_race(season):
#     '''
#     Return the percentage of race laps that had rain for each race in a season

#     Returns
#     RoundNumber|Rain %
#     '''
#     events = get_events_in_season(season)
#     rounds = range(1,events+1)

#     event_type = 'R'

#     results = []

#     for round in rounds:
            
#         session = ff1.get_session(season, round, event_type)
#         session.load()

#         weather = session.laps.get_weather_data()
#         rain = weather['Rainfall'].astype(int).mean()

#         results.append({
#             'RoundNumber': int(round),
#             'Rain %': rain
#         })

#     season_rain = pd.DataFrame(results)

#     return season_rain

def get_data_for_season(season):
    '''
    Returns DataFrame with results for a whole season.

    DataFrame:
    DriverNumber|Season|RoundNumber|TeamName|Position|QualiPosition|FastestTime
    '''   
    events = get_events_in_season(season)
    rounds = range(1, events+1)

    all_results = []
    for round in rounds:
        race = get_loaded_session(season, round, 'R')
        quali = get_loaded_session(season, round, 'Q')
        race.load()
        quali.load()

        quali_res = get_quali_results(session=quali) # DriverNumber|RoundNumber|QualiPosition
        quali_times = get_quali_times(session=quali) # DriverNumber|RoundNumber|FastestTime
        race_res = get_race_results(session=race) # DriverNumber|RoundNumber|TeamName|Position

        res_df1 = pd.merge(race_res, quali_res, on=['DriverNumber', 'RoundNumber'], how='left')
        res_df2 = pd.merge(res_df1, quali_times, on=['DriverNumber', 'RoundNumber'], how='left')

        all_results.append(res_df2)

    results = pd.concat(all_results, ignore_index=True)

    return results

def make_data_dataframe(seasons: list):
    '''
    Make a dataframe of all the results I want for the model

    Output:
    DriverNumber|Season|RoundNumber|TeamName|Position|QualiPosition|FastestTime
    '''
    results = []
    for season in seasons:
        season_res = get_data_for_season(season)
        season_res = season_res.insert(1,'Season', season)

        results.append(season_res)

    df = pd.concat(results, ignore_index=True)

    return df