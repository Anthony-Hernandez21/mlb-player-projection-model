# MLB Player Projection Model

This project builds a basic MLB pitcher strikeout projection board.

## What It Does

The current notebook:

- pulls pitcher Statcast data with pybaseball
- converts pitch-level data into game-level strikeout logs
- calculates last 3, last 5, and season strikeout averages
- creates a projected strikeout number
- compares the projection to a manually entered sportsbook strikeout line
- labels each row as Over, Under, No Bet, or No Data
- adds basic game context like opponent and home/away
- saves a daily pitcher board to CSV

## Tools

- Python
- pandas
- numpy
- pybaseball
- Jupyter Notebook

## Example Output

| slate_date | pitcher | opponent | home_away | sportsbook_line | projected_k | difference | final_action | status |
|---|---|---|---|---:|---:|---:|---|---|
| 2026-06-16 | Dylan Cease | BOS | Away | 6.5 | 9.19 | 2.69 | Bet Over | Playable |
| 2026-06-16 | Jesús Luzardo | MIA | Home | 6.5 | 5.55 | -0.95 | Pass | Pass - Small Edge |


## How to Run the Daily Board

Launch Project from Terminal:

`cd ~/mlb-player-projection-model`

Update the slate settings file:

`nano data/slate_config.csv`

Example:

```csv
slate_date,season
2026-06-16,2026
```

Update the sportsbook lines file:

`nano data/daily_lines.csv`

Example:

```csv
pitcher,opponent,home_away,line
Dylan Cease,BOS,Away,6.5
Jesús Luzardo,MIA,Home,6.5
```

Run the daily board from Terminal:

```bash
source venv312/bin/activate
python src/run_daily_board.py
```

The script saves the output to:

```text
data/daily_pitcher_board_YYYY-MM-DD.csv
```

## Project Structure

data/
  daily_lines.csv
  slate_config.csv
  daily_pitcher_board_YYYY-MM-DD.csv

notebooks/
  data_exploration.ipynb

src/
  projections.py
  run_daily_board.py

  ## Current Limitations

Sportsbook lines are entered manually.
The model is a simple baseline, not a validated betting system.
No opponent strikeout-rate adjustment yet.
No backtesting yet.

## Next Steps

Backtest past projections.
Add opponent strikeout tendencies.
Improve player lookup for accented names.
Add probable pitchers automatically.
