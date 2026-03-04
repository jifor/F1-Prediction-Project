'''
File that will get previous race results, put them into a dataframe, and return the dataframe of results.

Things to consider:
    - Want this to work automatically in the future so it should do something like get the event schedule and pull all the results from that season
    - drivers change during a season so I need a way to handle driver changes; probably just remove the driver if they aren't in the current season
    - also need a way to handle dsqs and retires. dsq is difficult because in recent seasons dsqs did very well in the race
        - Ferrari in China 2025, Russell in Belgium 2024, Mclaren in 2025 in Las Vegas
    - Problem: Doohan only got six races so there is no franco in the results frame
Base this on First_Attempt.ipynb 
'''

import fastf1 as ff1
import pandas as pd
import cache_path as cache # cache path in python file in .gitignore. Need to make one of macbook

def get_season_results(season):
    ff1.Cache.enable_cache(cache.cache_path)

    session_type = 'R'

    rounds = range(6,8)
    # results = pd.DataFrame(columns=rounds)

    # for round in rounds:
    #     session = ff1.get_session(season, round, session_type)
    #     session.load()
    #     result = pd.Series(session.results.loc[:, 'ClassifiedPosition'])
    #     # Re-sort the results by ascending driver number
    #     result.index = result.index.astype(int)
    #     result = result.sort_index()
    #     # Handle retires and dsqs
    #     # result = result.replace(['R', 'D'], 20)
    #     # result = result.fillna(20) # on hold for now
    #     result = pd.to_numeric(result, errors='coerce')
    #     result = result.fillna(20)
    #     results[round] = result

    # return results

    all_rounds = []

    for round in rounds:
        session = ff1.get_session(season, round, session_type)
        session.load()

        result = session.results['ClassifiedPosition']
        # Re-sort by ascending driver number
        result.index = result.index.astype(int)
        result = result.sort_index()

        result = pd.to_numeric(result, errors='coerce')

        all_rounds.append(result.rename(round))

    results = pd.concat(all_rounds, axis=1)
    results = results.fillna(20)

    return results

r = get_season_results(2025)
print(r)