import fastf1 as ff1
import pandas as pd
import cache_path as cache # path to cache in cache_path.py; in .gitignore

def get_events_in_season(year):
    '''
    Get the number of events in a season
    '''
    ff1.Cache.enable_cache(cache.cache_path)

    schedule = ff1.get_event_schedule(year)

    return len(schedule.index) # want this much more fleshed out in the future


def get_season_results(season):
    '''
    Function that will get previous race results, put them into a dataframe, and return the dataframe of results.

    Returns dataframe:
    index|DriverNumber|RoundNumber|Position

    Things to consider:
        - Want this to work automatically in the future so it should do something like get the event schedule and pull all the results from that season
        - also need a way to handle dsqs and retires. dsq is difficult because in recent seasons dsqs did very well in the race
            - Ferrari in China 2025, Russell in Belgium 2024, Mclaren in 2025 in Las Vegas
    '''
    ff1.Cache.enable_cache(cache.cache_path) # these can be removed once I have a working main.py

    session_type = 'R'

    # get the number of events in a season that results can be pulled for
    no_events = get_events_in_season(season)
    rounds = range(1, no_events)
    # rounds = range(1,5)
    all_results = []

    for round in rounds:
        session = ff1.get_session(season, round, session_type)
        session.load()

        result = session.results['ClassifiedPosition']
        result.index = result.index.astype(int)
        # Replace 'R', 'D', 'W' with 20
        result = pd.to_numeric(result, errors="coerce").fillna(20)

        race_df = pd.DataFrame({
            "DriverNumber": result.index,
            "RoundNumber": round,
            "Position": result.values
        })

        race_df = race_df.sort_values('DriverNumber')

        all_results.append(race_df)

    results = pd.concat(all_results, ignore_index=True)
    return results

def get_season_qual_results(season):
    '''
    Gets qualifying results for a season and returns them in a dataframe with Driver Number and Round Number
    '''
    ff1.Cache.enable_cache(cache.cache_path)

    session_type = 'Q'

    no_events = get_events_in_season(season)
    rounds = range(1, no_events)
    
    all_results = []

    for round in rounds:
        session = ff1.get_session(season, round, session_type)
        session.load()

        result = session.results['Position']
        result.index = result.index.astype(int)
        # Fill missing values with 20
        result = pd.to_numeric(result, errors="coerce").fillna(20)

        qual_df = pd.DataFrame({
            "DriverNumber": result.index,
            "RoundNumber": round,
            "Position": result.values
        })

        qual_df = qual_df.sort_values('DriverNumber')

        all_results.append(qual_df)

    results = pd.concat(all_results, ignore_index=True)

    return results

def get_event_qual_times(session_year, round_number):
    '''
    Get the fastest times for each driver in a qualifying session

    Returns
    DriverNumber|RoundNumber|FastestTime
    '''
    ff1.Cache.enable_cache(cache.cache_path)

    session = ff1.get_session(session_year, round_number, 'Q')
    session.load()

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
    return qual_times

def get_season_qual_times(season):
    '''
    Get the fastest time for each driver for every qualifying session in a season

    Returns df like
    DriverNumber|RoundNumber|FastestTime
    '''

    # Cache is enabled by get_event_qual_times()

    no_events = get_events_in_season(season)
    rounds = range(1, no_events)

    all_results = []
    for round in rounds:
        times = get_event_qual_times(season, round)
        times = times.sort_values('DriverNumber')
        all_results.append(times)

    results = pd.concat(all_results, ignore_index=True)
    return results 