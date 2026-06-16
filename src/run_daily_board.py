import pandas as pd

from projections import build_pitcher_board


regular_season_start_dates = {
    2025: '2025-03-27',
    2026: '2026-03-25'
}

slate_config = pd.read_csv('data/slate_config.csv')

slate_date = slate_config.loc[0, 'slate_date']
season = int(slate_config.loc[0, 'season'])
regular_season_start = regular_season_start_dates[season]

daily_lines = pd.read_csv('data/daily_lines.csv').to_dict('records')

daily_pitcher_board = build_pitcher_board(
    daily_lines,
    season,
    regular_season_start
)

daily_pitcher_board['slate_date'] = slate_date

columns = [
    'slate_date',
    'pitcher',
    'opponent',
    'home_away',
    'sportsbook_line',
    'projected_k',
    'difference',
    'final_action',
    'status',
    'recommendation',
    'edge_strength',
    'sample_size',
    'games_used',
    'last_3_avg_k',
    'last_5_avg_k',
    'season_avg_k',
    'season_avg_pitches'
]

daily_pitcher_board = daily_pitcher_board[columns]

output_path = f'data/daily_pitcher_board_{slate_date}.csv'
daily_pitcher_board.to_csv(output_path, index=False)

print(daily_pitcher_board)
print(f'Saved board to {output_path}')
