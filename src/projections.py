"""
Projection helper functions for the MLB pitcher strikeout model.
"""

import numpy as np
import pandas as pd

from pybaseball import playerid_lookup, statcast_pitcher


def split_pitcher_name(full_name):
    name_parts = full_name.strip().split()

    first_name = name_parts[0].lower()
    last_name = name_parts[-1].lower()

    return first_name, last_name


def label_edge(difference):
    abs_difference = abs(difference)

    if abs_difference >= 1.5:
        return 'Strong Edge'
    elif abs_difference >= 1.0:
        return 'Medium Edge'
    elif abs_difference >= 0.5:
        return 'Small Edge'
    else:
        return 'No Bet'


def final_action(row):
    if (
        row['sample_size'] == 'Good Sample'
        and row['edge_strength'] in ['Medium Edge', 'Strong Edge']
        and row['recommendation'] == 'Over'
    ):
        return 'Bet Over'

    elif (
        row['sample_size'] == 'Good Sample'
        and row['edge_strength'] in ['Medium Edge', 'Strong Edge']
        and row['recommendation'] == 'Under'
    ):
        return 'Bet Under'

    else:
        return 'Pass'


def add_status(row):
    if row['recommendation'] == 'No Data':
        return 'No Data'

    if row['final_action'] in ['Bet Over', 'Bet Under']:
        return 'Playable'

    if row['sample_size'] == 'Small Sample':
        return 'Pass - Small Sample'

    if row['edge_strength'] == 'Small Edge' or row['edge_strength'] == 'No Bet':
        return 'Pass - Small Edge'

    return 'Pass'



def project_pitcher_k(last_name, first_name, season, regular_season_start):
    player_ids = playerid_lookup(last_name, first_name)
    mlbam_id = int(player_ids.iloc[0]['key_mlbam'])

    start_date = regular_season_start
    end_date = f'{season}-10-01'

    data = statcast_pitcher(start_date, end_date, mlbam_id)

    games = (
        data.groupby('game_date')
        .agg(
            strikeouts=('events', lambda x: (x == 'strikeout').sum()),
            pitches=('pitch_type', 'count'),
            avg_velocity=('release_speed', 'mean')
        )
        .reset_index()
        .sort_values('game_date')
    )

    games['last_3_avg_k'] = games['strikeouts'].rolling(3).mean()
    games['last_5_avg_k'] = games['strikeouts'].rolling(5).mean()
    games['season_avg_k'] = games['strikeouts'].expanding().mean()
    games['season_avg_pitches'] = games['pitches'].expanding().mean()

    latest = games.iloc[-1]

    projected_k = (
        latest['last_3_avg_k'] * 0.4 +
        latest['last_5_avg_k'] * 0.4 +
        latest['season_avg_k'] * 0.2
    )

    return {
        'pitcher': f'{first_name.title()} {last_name.title()}',
        'mlbam_id': mlbam_id,
        'season': season,
        'regular_season_start': regular_season_start,
        'projected_k': projected_k,
        'last_3_avg_k': latest['last_3_avg_k'],
        'last_5_avg_k': latest['last_5_avg_k'],
        'season_avg_k': latest['season_avg_k'],
        'season_avg_pitches': latest['season_avg_pitches'],
        'games_used': len(games),
        'games': games
    }


def compare_to_line(result, sportsbook_line):
    projected_k = round(result['projected_k'], 2)
    difference = round(projected_k - sportsbook_line, 2)

    if difference >= 0.5:
        recommendation = 'Over'
    elif difference <= -0.5:
        recommendation = 'Under'
    else:
        recommendation = 'No Bet'

    if result['games_used'] >= 10:
        sample_size = 'Good Sample'
    else:
        sample_size = 'Small Sample'

    summary = pd.DataFrame([{
        'pitcher': result['pitcher'],
        'games_used': result['games_used'],
        'last_3_avg_k': round(result['last_3_avg_k'], 2),
        'last_5_avg_k': round(result['last_5_avg_k'], 2),
        'season_avg_k': round(result['season_avg_k'], 2),
        'season_avg_pitches': round(result['season_avg_pitches'], 2),
        'projected_k': projected_k,
        'sportsbook_line': sportsbook_line,
        'difference': difference,
        'recommendation': recommendation,
        'sample_size': sample_size
    }])

    return summary


def build_pitcher_board(pitchers, season, regular_season_start):
    all_summaries = []

    for pitcher in pitchers:
        try:
            first_name, last_name = split_pitcher_name(pitcher['pitcher'])

            result = project_pitcher_k(
                last_name,
                first_name,
                season,
                regular_season_start
            )

            summary = compare_to_line(result, pitcher['line'])
            summary['opponent'] = pitcher['opponent']
            summary['home_away'] = pitcher['home_away']

            all_summaries.append(summary)

        except Exception as e:
            missing_summary = pd.DataFrame([{
                'pitcher': pitcher['pitcher'],
                'opponent': pitcher['opponent'],
                'home_away': pitcher['home_away'],
                'games_used': 0,
                'last_3_avg_k': np.nan,
                'last_5_avg_k': np.nan,
                'season_avg_k': np.nan,
                'season_avg_pitches': np.nan,
                'projected_k': np.nan,
                'sportsbook_line': pitcher['line'],
                'difference': np.nan,
                'recommendation': 'No Data',
                'sample_size': 'No Data',
                'error_message': str(e)
            }])

            all_summaries.append(missing_summary)

    board = pd.concat(all_summaries, ignore_index=True)

    board['edge_strength'] = board['difference'].apply(
        lambda x: 'No Data' if pd.isna(x) else label_edge(x)
    )

    board['final_action'] = board.apply(
        lambda row: 'Pass' if row['recommendation'] == 'No Data' else final_action(row),
        axis=1
    )

    board['status'] = board.apply(add_status, axis=1)

    board['abs_difference'] = board['difference'].abs()
    board = board.sort_values('abs_difference', ascending=False, na_position='last')
    board = board.drop(columns=['abs_difference'])

    columns = [
        'pitcher',
        'opponent',
        'home_away',
        'games_used',
        'last_3_avg_k',
        'last_5_avg_k',
        'season_avg_k',
        'season_avg_pitches',
        'projected_k',
        'sportsbook_line',
        'difference',
        'recommendation',
        'sample_size',
        'edge_strength',
        'final_action',
        'status'
    ]

    return board[columns]