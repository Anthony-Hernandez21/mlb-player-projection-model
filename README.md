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

Update the slate settings:

`data/slate_config.csv`

Example:

```csv
slate_date,season
2026-06-16,2026


Update the sportsbook lines:

`data/slate_config.csv`

Example: