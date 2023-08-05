import math

import numpy as np

import pandas as pd
from pandas import DataFrame

from pytchout.misc import get_pitch_types

from datetime import datetime


def combine_dataframes(df1, df2):
    pass


def get_statcast_request_url(
    season="",
    player_type="pitcher",
    pitcher_throws="",
    batter_stands="",
    game_date_gt="",
    game_date_lt="",
    batter_id="",
    pitcher_id="",
):

    # support lists?
    if batter_id:
        batters_lookup = f"batters_lookup%5B%5D={str(batter_id)}&"
    else:
        batters_lookup = ""

    if pitcher_id:
        pitchers_lookup = f"pitchers_lookup%5B%5D={str(pitcher_id)}&"
    else:
        pitchers_lookup = ""

    url = f"https://baseballsavant.mlb.com/statcast_search/csv?all=true&hfPT=&hfAB=&hfBBT=&hfPR=&hfZ=&stadium=&hfBBL=&hfNewZones=&hfGT=R%7C&hfC=&hfSea={str(season)}%7C&hfSit=&player_type={str(player_type)}&hfOuts=&opponent=&pitcher_throws={str(pitcher_throws)}&batter_stands={str(batter_stands)}&hfSA=&game_date_gt={str(game_date_gt)}&game_date_lt={str(game_date_lt)}&hfInfield=&team=&position=&hfOutfield=&hfRO=&home_road=&{batters_lookup}hfFlag=&hfPull=&{pitchers_lookup}metric_1=&hfInn=&min_pitches=0&min_results=0&group_by=name&sort_col=pitches&player_event_sort=h_launch_speed&sort_order=desc&min_pas=0&type=details&"

    return url


def validate_datestring(datestring, date_format="%Y-%m-%d"):
    try:
        return datetime.strptime(datestring, date_format)
    except ValueError:
        raise ValueError("Incorrect date format. Use YYYY-MM-DD.")


def df_mean(df, column):
    return df[column].dropna().mean()


def decimal_time_to_clock_time(decimal_time, minutes_round=1):
    if math.isnan(decimal_time):
        return ""

    if minutes_round == 0:
        raise ValueError("minutes_round cannot be 0")

    MINUTES_ROUND = minutes_round

    hours = int(decimal_time)
    minutes = MINUTES_ROUND * round(int(decimal_time * 60 % 60) / MINUTES_ROUND)

    if minutes == 60:
        hours += 1
        minutes = 0

    hours %= 12

    return f"{hours}:{minutes:02d}"


def decimal_time_to_spin_direction(decimal_time):
    time = decimal_time_to_clock_time(decimal_time)
    return tilt_to_spin_direction(time)


def tilt_to_spin_direction(tilt):
    if not tilt:
        return np.nan

    time_components = tilt.split(":")

    hours = int(time_components[0])
    minutes = int(time_components[1])

    return ((hours * 30) + (minutes / 2) + 180) % 360


def spin_direction_to_tilt(spin_direction):
    pass


if __name__ == "__main__":
    print(decimal_time_to_spin_direction(3.90))
