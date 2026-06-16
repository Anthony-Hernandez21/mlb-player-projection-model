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