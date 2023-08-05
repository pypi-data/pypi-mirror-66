import pandas as pd
from requests import get
from bs4 import BeautifulSoup


def get_team_game_logs(team, season_end_year):
    url = 'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=%2Fteams%2F'+team+'%2F'+season_end_year+'%2Fgamelog%2F&div=div_tgl_basic'
    r = get(url)
    df = None
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        df = pd.read_html(str(table))[0]
        game = df['Unnamed: 1_level_0', 'G']
        df = df[~game.str.contains("G", na=True)]
        df.columns = [' '.join(col).strip() for col in df.columns.values]
        df.rename(columns={
            'Unnamed: 1_level_0 G': 'Game #',
            'Unnamed: 2_level_0 Date': 'Date',
            'Unnamed: 3_level_0 Unnamed: 3_level_1': 'H/A',
            'Unnamed: 4_level_0 Opp': 'Opponent',
            'Unnamed: 5_level_0 W/L': 'W/L',
            'Unnamed: 6_level_0 Tm': 'Team PTS',
            'Unnamed: 7_level_0 Opp': 'Opponent PTS'}, inplace=True)
        df = df.drop(columns=[
            'Unnamed: 0_level_0 Rk',
            'Unnamed: 24_level_0 Unnamed: 24_level_1'])
        df['H/A'] = df['H/A'].fillna(value='H')
        df['H/A'] = df['H/A'].replace('@', 'A')
        df = df.astype(
            {
                'Team PTS': 'float64', 'Opponent PTS': 'float64',
                'Team FG': 'float64', 'Team FGA': 'float64',
                'Team FG%': 'float64', 'Team 3P': 'float64',
                'Team 3PA': 'float64', 'Team 3P%': 'float64',
                'Team FT': 'float64', 'Team FTA': 'float64',
                'Team FT%': 'float64', 'Team ORB': 'float64',
                'Team TRB': 'float64', 'Team AST': 'float64',
                'Team STL': 'float64', 'Team BLK': 'float64',
                'Team TOV': 'float64', 'Team PF': 'float64',
                'Opponent FG': 'float64', 'Opponent 3P%': 'float64',
                'Opponent FT': 'float64', 'Opponent FTA': 'float64',
                'Opponent FT%': 'float64', 'Opponent FGA': 'float64',
                'Opponent FG%': 'float64', 'Opponent 3P': 'float64',
                'Opponent 3PA': 'float64', 'Opponent ORB': 'float64',
                'Opponent TRB': 'float64', 'Opponent AST': 'float64',
                'Opponent STL': 'float64', 'Opponent BLK': 'float64',
                'Opponent TOV': 'float64', 'Opponent PF': 'float64'})
    return df


def get_team_game_logs_adv(team, season_end_year):
    url = 'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=%2Fteams%2F' + team + '%2F' + season_end_year + '%2Fgamelog-advanced%2F&div=div_tgl_advanced'
    r = get(url)
    df = None
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find('table')
        df = pd.read_html(str(table))[0]
        game = df['Unnamed: 1_level_0', 'G']
        df = df[~game.str.contains("G", na=True)]
        df.columns = [' '.join(col).strip() for col in df.columns.values]
        df.rename(columns={
            'Unnamed: 1_level_0 G': 'Game #',
            'Unnamed: 2_level_0 Date': 'Date',
            'Unnamed: 3_level_0 Unnamed: 3_level_1': 'H/A',
            'Unnamed: 4_level_0 Opp': 'Opponent',
            'Unnamed: 5_level_0 W/L': 'W/L',
            'Unnamed: 6_level_0 Tm': 'Team PTS',
            'Unnamed: 7_level_0 Opp':
            'Opponent PTS'}, inplace=True)
        df = df.drop(columns=[
            'Unnamed: 0_level_0 Rk', 'Unnamed: 18_level_0 Unnamed: 18_level_1',
            'Unnamed: 23_level_0 Unnamed: 23_level_1'])
        df.columns = df.columns.str.replace(r'Advanced ', '')
        df.columns = df.columns.str.replace(r'Four Factors ', '')
        df['H/A'] = df['H/A'].fillna(value='H')
        df['H/A'] = df['H/A'].replace('@', 'A')
        df = df.astype(
            {
                'Team PTS': 'float64', 'Opponent PTS': 'float64',
                'ORtg': 'float64', 'DRtg': 'float64', 'Pace': 'float64',
                'FTr': 'float64', '3PAr': 'float64', 'TS%': 'float64',
                'TRB%': 'float64', 'AST%': 'float64', 'STL%': 'float64',
                'BLK%': 'float64', 'Offensive eFG%': 'float64',
                'Offensive TOV%': 'float64', 'Offensive ORB%': 'float64',
                'Offensive FT/FGA': 'float64', 'Defensive eFG%': 'float64',
                'Defensive TOV%': 'float64', 'Defensive DRB%': 'float64',
                'Defensive FT/FGA': 'float64'})
    return df
