import pandas as pd
from pandas import DataFrame

import requests
import io
import math

from contextlib import closing

from urllib3.exceptions import NewConnectionError

from datetime import datetime

from pytchout.tools.nathan import nathan_calculations
from pytchout.misc import get_pitch_types
from pytchout.misc import get_column_counts
from pytchout.utils import get_statcast_request_url
from pytchout.utils import validate_datestring
from pytchout.analysis.arsenal import get_pitcher_arsenal
from pytchout.analysis.arsenal import determine_primary_fb
from pytchout.retrosheet import retrosheet_game_logs


def split_data(data, by):
    if by != "pitch_type":
        raise ValueError("Splitting is only supported for pitch_type.")

    split_data = {}

    if by == "pitch_type":
        pitch_types = get_pitch_types(data)

        for pitch in pitch_types:
            split_data[pitch] = data.query("pitch_type == @pitch")

    if by == "opponent":
        pass

    if by == "batter_handedness":
        pass

    return split_data


def statcast(start_date, end_date=None, team=None, nathan=True, split_by=None):
    if not start_date:
        raise ValueError("No start date provided.")

    PITCHES_PER_GAME = 325
    ROW_LIMIT = 35000
    GAMES_ALLOWED = int(ROW_LIMIT / PITCHES_PER_GAME)

    # If not end date provided, assume same day as start date? Or assume up until today?
    start_date = validate_datestring(start_date)
    end_date = validate_datestring(end_date) if end_date else start_date

    # TODO: Move this stuff to own method
    if start_date > end_date:
        raise ValueError(
            "The start date for this request is after the end date. Please try again with valid dates."
        )

    start_year = start_date.year
    end_year = end_date.year

    if start_year != end_year:
        raise ValueError(
            "This request spans multiple years. Please split up your request and use the combine_dataframes method to combine your data."
        )

    # TODO: Fix up this gross code
    gamelogs = retrosheet_game_logs(start_year)

    in_range = gamelogs.query("date >= @start_date and date <= @end_date")

    date_counts = get_column_counts(in_range, column="date")

    dates = sorted(date_counts.keys())

    game_count = 0
    request_start_date = None

    for i, date in enumerate(dates):
        if game_count == 0:
            request_start_date = date

        to_add = date_counts[date]

        if game_count + to_add > GAMES_ALLOWED:
            get_statcast_request_url(
                game_date_gt=request_start_date, game_date_lt=date[i - 1]
            )

            request_start_date = date
        else:
            game_count += to_add


# def statcast_pitcher(pitcher_id, start_date, end_date, nathan=False):
def statcast_pitcher(pitcher_id, season, nathan=True, split_by=None):
    if nathan and int(season) < 2017:
        raise ValueError("TrackMan use began in 2017.")

    with closing(
        requests.get(get_statcast_request_url(season=season, pitcher_id=pitcher_id))
    ) as r:
        data = pd.read_csv(io.StringIO(r.content.decode("utf-8")))

    if nathan:
        data = nathan_calculations(data)

    return data


def statcast_batter(batter_id, start_date, end_date, nathan=False):
    pass


def statcast_pitcher_vs_hitter(pitcher_id, batter_id, start_date=None, end_date=None):
    pass


def statcast_video():
    pass


if __name__ == "__main__":
    # for pitcher_id in [501925, 545333]:
    #     data = statcast_pitcher(pitcher_id, 2019)
    #     # data = statcast_pitcher(545333, 2019)
    #     pd.options.display.max_columns = None
    #     # print(data.head(5))
    #     arsenal = get_pitcher_arsenal(data)
    #     print(arsenal)

    statcast("2019-04-02", "2019-04-05")
