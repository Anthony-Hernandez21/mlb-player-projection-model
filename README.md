# MLB Player Projection Model

This project builds a basic MLB pitcher strikeout projection board.

## Current Version

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

## Current Workflow

1. Open the notebook in `notebooks/data_exploration.ipynb`
2. Update the daily input section
3. Run the notebook cells
4. Review the daily pitcher board
5. Save the output CSV



## How to Run the Daily Board

Update the slate settings file:

`data/slate_config.csv`

Example:

```csv
slate_date,season
2026-06-16,2026
```

Update the sportsbook lines file:

`data/daily_lines.csv`

Example:

```csv
pitcher,opponent,home_away,line
Tarik Skubal,CLE,Home,7.5
Zack Wheeler,ATL,Away,6.5
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