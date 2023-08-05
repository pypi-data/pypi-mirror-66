import io
import requests
import pandas as pd
import zipfile

from contextlib import closing
from datetime import datetime


gamelog_columns = [
    "date",
    "game_num",
    "day_of_week",
    "visiting_team",
    "visiting_team_league",
    "visiting_game_num",
    "home_team",
    "home_team_league",
    "home_team_game_num",
    "visiting_score",
    "home_score",
    "num_outs",
    "day_night",
    "completion_info",
    "forfeit_info",
    "protest_info",
    "park_id",
    "attendance",
    "time_of_game_minutes",
    "visiting_line_score",
    "home_line_score",
    "visiting_abs",
    "visiting_hits",
    "visiting_doubles",
    "visiting_triples",
    "visiting_homeruns",
    "visiting_rbi",
    "visiting_sac_hits",
    "visiting_sac_flies",
    "visiting_hbp",
    "visiting_bb",
    "visiting_iw",
    "visiting_k",
    "visiting_sb",
    "visiting_cs",
    "visiting_gdp",
    "visiting_ci",
    "visiting_lob",
    "visiting_pitchers_used",
    "visiting_individual_er",
    "visiting_er",
    "visiting__wp",
    "visiting_balks",
    "visiting_po",
    "visiting_assists",
    "visiting_errors",
    "visiting_pb",
    "visiting_dp",
    "visiting_tp",
    "home_abs",
    "home_hits",
    "home_doubles",
    "home_triples",
    "home_homeruns",
    "home_rbi",
    "home_sac_hits",
    "home_sac_flies",
    "home_hbp",
    "home_bb",
    "home_iw",
    "home_k",
    "home_sb",
    "home_cs",
    "home_gdp",
    "home_ci",
    "home_lob",
    "home_pitchers_used",
    "home_individual_er",
    "home_er",
    "home_wp",
    "home_balks",
    "home_po",
    "home_assists",
    "home_errors",
    "home_pb",
    "home_dp",
    "home_tp",
    "ump_home_id",
    "ump_home_name",
    "ump_first_id",
    "ump_first_name",
    "ump_second_id",
    "ump_second_name",
    "ump_third_id",
    "ump_third_name",
    "ump_lf_id",
    "ump_lf_name",
    "ump_rf_id",
    "ump_rf_name",
    "visiting_manager_id",
    "visiting_manager_name",
    "home_manager_id",
    "home_manager_name",
    "winning_pitcher_id",
    "winning_pitcher_name",
    "losing_pitcher_id",
    "losing_pitcher_name",
    "save_pitcher_id",
    "save_pitcher_name",
    "game_winning_rbi_id",
    "game_winning_rbi_name",
    "visiting_starting_pitcher_id",
    "visiting_starting_pitcher_name",
    "home_starting_pitcher_id",
    "home_starting_pitcher_name",
    "visiting_1_id",
    "visiting_1_name",
    "visiting_1_pos",
    "visiting_2_id",
    "visiting_2_name",
    "visiting_2_pos",
    "visiting_2_id.1",
    "visiting_3_name",
    "visiting_3_pos",
    "visiting_4_id",
    "visiting_4_name",
    "visiting_4_pos",
    "visiting_5_id",
    "visiting_5_name",
    "visiting_5_pos",
    "visiting_6_id",
    "visiting_6_name",
    "visiting_6_pos",
    "visiting_7_id",
    "visiting_7_name",
    "visiting_7_pos",
    "visiting_8_id",
    "visiting_8_name",
    "visiting_8_pos",
    "visiting_9_id",
    "visiting_9_name",
    "visiting_9_pos",
    "home_1_id",
    "home_1_name",
    "home_1_pos",
    "home_2_id",
    "home_2_name",
    "home_2_pos",
    "home_3_id",
    "home_3_name",
    "home_3_pos",
    "home_4_id",
    "home_4_name",
    "home_4_pos",
    "home_5_id",
    "home_5_name",
    "home_5_pos",
    "home_6_id",
    "home_6_name",
    "home_6_pos",
    "home_7_id",
    "home_7_name",
    "home_7_pos",
    "home_8_id",
    "home_8_name",
    "home_8_pos",
    "home_9_id",
    "home_9_name",
    "home_9_pos",
    "misc",
    "acquisition_info",
]


game_types = {
    "regular": "",
    "world_series": "ws",
    "all_star": "as",
    "wild_card": "wc",
    "lds": "dv",
    "lcs": "lc",
}


def get_retrosheet_request_url(year, game_type="regular"):
    if game_type not in game_types.keys():
        raise ValueError("Invalid game type provided.")

    return f"http://www.retrosheet.org/gamelogs/gl{game_types[game_type]}{year}.zip"


def retrosheet_game_logs(year, game_type="regular"):
    if game_type not in game_types.keys():
        raise ValueError("Invalid game type provided.")

    with closing(
        requests.get(
            get_retrosheet_request_url(year=year, game_type=game_type), stream=True
        )
    ) as r:
        z = zipfile.ZipFile(io.BytesIO(r.content))

    data = pd.read_csv(
        z.open(f"GL{game_types[game_type]}{year}.TXT"), names=gamelog_columns
    )

    data = datestrings_to_datetime(data)

    return data


def datestrings_to_datetime(data, date_format="%Y%m%d"):
    data["date"] = pd.to_datetime(data["date"], format=date_format)

    return data


if __name__ == "__main__":
    data = retrosheet_game_logs(2019)
    print(data)
