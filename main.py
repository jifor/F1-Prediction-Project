import typer 
import fastf1 as ff1

app = typer.Typer()

ff1.Cache.enable_cache('C:\\Users\\jifor\\Python\\F1 Prediction Project\\FF1 Cache')

'''
Make a function that will take a race (year and name) as the input and return the winner
'''
@app.command()
def race_winner(name: str, year: int):
    session = ff1.get_session(year, name, 'R')

    session.load()

    winner_first_name = session.results.iloc[0]['FirstName']
    winner_last_name = session.results.iloc[0]['LastName']

    print(f'The winner of the {year} {session.event['EventName']} was {winner_first_name} {winner_last_name}!')

if __name__ == '__main__':
    app()