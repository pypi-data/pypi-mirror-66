import pandas as pd
import numpy as np
import math


def parse_rapsodo_data(file):
    pass


def get_pitch_types(pitches, column="pitch_type"):
    pitch_types = list(pitches[column].unique())
    for pitch in pitch_types:
        if isinstance(pitch, float) and math.isnan(pitch):
            pitch_types.remove(pitch)
    return pitch_types


# TODO: Combine the following two into one
def get_pitch_counts(pitches, column="pitch_type"):
    return dict(pitches[column].value_counts(dropna=True))


def get_column_counts(data, column):
    return dict(data[column].value_counts(dropna=True))


def get_player_ids_from_name(first_name, last_name):
    pass


def get_player_name_from_id(player_id, source="mlb"):
    pass


def pitcher_arsenal(pitches):
    pass


def update_player_id_map():
    pass
