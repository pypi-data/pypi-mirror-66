import pandas as pd
from pandas import DataFrame

import numpy as np

from pytchout.utils import df_mean
from pytchout.utils import decimal_time_to_clock_time
from pytchout.utils import tilt_to_spin_direction

from pytchout.misc import get_pitch_types
from pytchout.misc import get_pitch_counts


# Iron out details later
def determine_primary_fb(data):
    fb_types = ["FF", "FT", "FC", "SI"]

    fbs = data.query("pitch_type in @fb_types")

    primary_fb = fbs[fbs["number_thrown"] == fbs["number_thrown"].max()][
        "pitch_type"
    ].item()

    data["primary_fb"] = np.where(data["pitch_type"] == primary_fb, True, False)

    print(data)


def calculate_pitch_differences_from_primary(data):
    pass


def get_pitcher_arsenal(pitches, min_number_thrown=0, min_percent_thrown=0.0):
    if pitches["pitcher"].nunique(dropna=True) > 1:
        raise ValueError(
            "Data includes pitches from more than one pitcher. Feature not yet implemented."
        )

    if pitches["game_year"].nunique(dropna=True) > 1:
        raise ValueError(
            "Data includes more than one season. Feature not yet implemented."
        )

    pitch_metrics = get_arsenal_pitch_metrics(
        pitches, min_number_thrown, min_percent_thrown
    )
    # pitch_results = get_arsenal_pitch_results(pitches, min_pitches)

    return pitch_metrics  # , pitch_results


def get_arsenal_pitch_metrics(pitches, min_number_thrown, min_percent_thrown):
    pitch_types = get_pitch_types(pitches)

    pitch_metric_columns = [
        "season",
        "pitcher",
        "pitcher_id",
        "pitch_type",
        "number_thrown",
        "percent_thrown",
        "velocity",
        "spin_rate",
        "bauer_units",
        "horz_break",
        "vert_break",
        "spin_direction",
        "tilt",
        "spin_eff",
        "gyro_angle",
        "horz_release_point",
        "vert_release_point",
        "release_extensions",
        "release_angle",
    ]

    pitch_metrics = []
    total_pitches = pitches["pitch_type"].dropna().count()

    for pitch in pitch_types:
        data = pitches.query("pitch_type == @pitch")
        if data["pitch_type"].count() < min_number_thrown:
            continue
        if data["pitch_type"].count() / total_pitches * 100 < min_percent_thrown:
            continue
        pitch_metrics.append(get_single_pitch_metrics(data, total_pitches))

    return DataFrame(pitch_metrics, columns=pitch_metric_columns).sort_values(
        by=["number_thrown", "pitch_type"], ascending=False
    )


def get_single_pitch_metrics(data, total_pitches=None):
    if data["pitch_type"].nunique(dropna=True) > 1:
        raise ValueError("Data includes more than one pitch type.")

    season = list(data["game_year"])[0]

    pitcher = list(data["player_name"])[0]
    pitcher_id = list(data["pitcher"])[0]

    pitch_type = list(data["pitch_type"])[0]
    number_thrown = data["pitch_type"].count()

    if total_pitches:
        percent_thrown = (number_thrown / total_pitches * 100).round(1)
    else:
        percent_thrown = 100.0

    velocity = df_mean(data, "release_speed").round(1)
    spin_rate = df_mean(data, "release_spin_rate").round(0).astype("int64")
    bauer_units = (spin_rate / velocity).round(1)

    horz_break = df_mean(data, "induced_horz_break").round(1)
    vert_break = df_mean(data, "induced_vert_break").round(1)

    spin_direction = df_mean(data, "spin_direction").round(0).astype("int64")
    tilt = decimal_time_to_clock_time(df_mean(data, "tilt_decimal"), minutes_round=5)

    spin_efficiency = (df_mean(data, "spin_eff") * 100).round(1)
    gyro_angle = df_mean(data, "gyro_angle").round(1)

    horz_release_point = df_mean(data, "release_pos_x").round(1)
    vert_release_point = df_mean(data, "release_pos_z").round(1)
    release_extension = df_mean(data, "release_extension").round(1)
    release_angle = df_mean(data, "release_angle").round(1)

    return [
        season,
        pitcher,
        pitcher_id,
        pitch_type,
        number_thrown,
        percent_thrown,
        velocity,
        spin_rate,
        bauer_units,
        horz_break,
        vert_break,
        spin_direction,
        tilt,
        spin_efficiency,
        gyro_angle,
        horz_release_point,
        vert_release_point,
        release_extension,
        release_angle,
    ]


# possibly extend to give this information for pitcher as whole?
def get_arsenal_pitch_results(pitches, min_pitches):
    pitch_types = get_pitch_types(pitches)

    pitch_result_columns = [
        "Pitcher",
        "Pitcher ID",
        "Pitch Type",
        "# Thrown",
        "% Thrown",
        "Strikes",
        "Balls",
        "SO",
        "BB",
        "Weak%",
        "Topped%",
        "Under%",
        "Burner%",
        "Solid%",
        "Barrel%",
        "Hard Hit%",
        "BABIP",
        "BA",
        "xBA",
        "wOBA",
        "xwOBA",
        "ISO",
        "EV",
        "LA",
        "Distance",
        "LD%",
        "GB%",
        "FB%",
        "IFFB%",
        "HR/FB",
        "O-Swing%",
        "Z-Swing%",
        "Swing%",
        "O-Contact%",
        "Z-Contact%",
        "Zone%",
        "SwStr%",
        "Whiff%",
    ]

    pitch_metrics = []

    for pitch in pitch_types:
        data = pitches.query("pitch_type == @pitch")
        if data["pitch_type"].count() < min_pitches:
            continue
        pitch_metrics.append(get_single_pitch_results(data))

    pitch_metrics.append(get_single_pitch_results(pitches, total=True))

    return DataFrame(data, columns=pitch_result_columns).sort_values(
        by=["# Thrown", "Pitch Type"], ascending=False
    )


def get_single_pitch_results(data, total=False):
    if total:
        pitch_type = "ALL"
    else:
        if data["pitch_type"].nunique(dropna=True) > 1:
            raise ValueError("Data includes more than one pitch type.")

        pitch_type = data["pitch_type"][0]

    # Change all 'query' calls to 'where' calls
    strikes = data.query('type in ["S", "X"]')["type"].count()
    balls = data.query('type == "B"')["type"].count()

    strikeouts = data.query('events == "strikeout"')["events"].count()
    walks = data.query('events == "walk"')["events"].count()

    weak = data.query("launch_speed_angle == 1")["launch_speed_angle"].count()
    topped = data.query("launch_speed_angle == 2")["launch_speed_angle"].count()
    under = data.query("launch_speed_angle == 3")["launch_speed_angle"].count()
    burner = data.query("launch_speed_angle == 4")["launch_speed_angle"].count()
    solid = data.query("launch_speed_angle == 5")["launch_speed_angle"].count()
    barrel = data.query("launch_speed_angle == 6")["launch_speed_angle"].count()
    hard_hit = data.query("launch_speed >= 95")["launch_speed"].count()

    # balls_in_play =

    hit_events = ["single", "double", "triple", "home_run"]
    at_bat_events = hit_events + [
        "field_error",
        "field_out",
        "fielders_choice",
        "fielders_choice_out",
        "force_out",
        "grounded_into_double_play",
        "other_out",
        "strikeout",
        "triple_play",
    ]
    plate_appearance_events = at_bat_events + [
        "walk",
        "hit_by_pitch",
        "sac_bunt",
        "sac_fly",
    ]

    at_bats = data.query("events in @at_bat_events")["events"].count()
    plate_appearances = data.query("events in @plate_appearance_events")[
        "events"
    ].count()
    hits = data.query("events in @hit_events")["events"].count()
    xhits = data["estimated_ba_using_speedangle"].sum()

    # very slight variations from numbers online
    ba = (hits / at_bats).round(3)
    xba = (xhits / at_bats).round(3)

    woba_value = data["woba_value"].sum()
    xwoba_value = data["estimated_woba_using_speedangle"].sum()
    woba_denom = data["woba_denom"].sum()

    woba = (woba_value / woba_denom).round(3)
    xwoba = (xwoba_value / woba_denom).round(3)

    print(woba)
    print(xwoba)

    swings_and_misses = data.query('description == "swinging_strike"')[
        "description"
    ].count()
    total_swings = data.query(
        'type in ["S", "X"] and description not in ["called_strike", "foul_bunt", "missed_bunt"]'
    )["description"].count()
    whiff_percentage = (swings_and_misses / total_swings * 100).round(1)

    return [whiff_percentage]
