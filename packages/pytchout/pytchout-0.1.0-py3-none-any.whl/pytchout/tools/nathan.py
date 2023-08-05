import pandas as pd
import numpy as np
import math

from pytchout.utils import decimal_time_to_spin_direction


# Environmental constant
K = 0.005383

# Standard gravity in ft/s^2
G = 32.174

# Distance of the pitcher's mound in feet
MOUND_DISTANCE = 60.5

# Distance of the initial Statcast measurement in feet
STATCAST_INITIAL_MEASUREMENT = 50.0

# Length of the plate in feet
PLATE_LENGTH = 17.0 / 12.0

# Number of inches in a foot
INCHES_PER_FOOT = 12.0

# Theoretical height of a parallel release point
ECKERSLEY_LINE = 2.85


def nathan_calculations(pitches):
    nathan_data = pitches.dropna(subset=["pitch_type"]).copy()

    # Referred to as 'yR' in the Nathan spreadsheet, named 'release_pos_y' here to be consistent with the release point naming for other dimensions
    nathan_data["release_pos_y"] = calculate_y_release_point(nathan_data)

    nathan_data["tR"] = calculate_release_time(nathan_data)

    (
        nathan_data["vxR"],
        nathan_data["vyR"],
        nathan_data["vzR"],
    ) = calculate_velocity_components_at_release(nathan_data)

    nathan_data["tf"] = calculate_flight_time(nathan_data)

    nathan_data["x_mvt"], nathan_data["y_mvt"] = calculate_induced_movement(nathan_data)

    (
        nathan_data["vxbar"],
        nathan_data["vybar"],
        nathan_data["vzbar"],
    ) = calculate_average_velocity_components(nathan_data)

    nathan_data["vbar"] = calculate_average_velocity(nathan_data)

    nathan_data["adrag"] = calculate_average_drag(nathan_data)

    (
        nathan_data["amagx"],
        nathan_data["amagy"],
        nathan_data["amagz"],
    ) = calculate_magnus_acceleration_components(nathan_data)

    nathan_data["amag"] = calculate_magnus_acceleration(nathan_data)

    nathan_data["Mx"], nathan_data["Mz"] = calculate_magnus_movement(nathan_data)

    nathan_data["Cd"] = calculate_drag_coefficient(nathan_data)

    nathan_data["Cl"] = calculate_lift_coefficient(nathan_data)

    nathan_data["S"] = calculate_spin_factor(nathan_data)

    nathan_data["spinT"] = calculate_transverse_spin(nathan_data)

    (
        nathan_data["phi"],
        nathan_data["spin_axis_decimal"],
        nathan_data["spin_direction"],
    ) = calculate_spin_axis(nathan_data)

    nathan_data["spin_eff"] = calculate_spin_efficiency(nathan_data)

    nathan_data["theta"] = calculate_gyro_angle(nathan_data)

    # Not technically a Nathan calculation but fits here
    nathan_data["release_angle"] = calculate_release_angle(nathan_data)

    """
    # Sanity check
    nathan_data['spinTx'], nathan_data['spinTy'], nathan_data['spinTz'] = calculate_transverse_spin_components(nathan_data)

    nathan_data['spin_check'] = calculate_spin_check(nathan_data)

    if any(nathan_data['spin_check']) > 0.001 or any(nathan_data['spin_check']) < -0.001:
        print('warning: spin check has failed')
    """

    # include spin direction AND tilt

    pitches[
        [
            "induced_horz_break",
            "induced_vert_break",
            "tilt_decimal",
            "spin_direction",
            "spin_eff",
            "gyro_angle",
            "release_angle",
        ]
    ] = nathan_data[
        [
            "x_mvt",
            "y_mvt",
            "spin_axis_decimal",
            "spin_direction",
            "spin_eff",
            "theta",
            "release_angle",
        ]
    ].copy()

    return pitches


def calculate_y_release_point(data):
    release_extension = data["release_extension"]

    return MOUND_DISTANCE - release_extension


def calculate_release_time(data):
    vy0 = data["vy0"]
    ay = data["ay"]
    release_pos_y = data["release_pos_y"]

    return time_in_air(vy0, ay, release_pos_y, STATCAST_INITIAL_MEASUREMENT, False)


def calculate_velocity_components_at_release(data):
    vx0 = data["vx0"]
    vy0 = data["vy0"]
    vz0 = data["vz0"]

    ax = data["ax"]
    ay = data["ay"]
    az = data["az"]

    tR = data["tR"]

    vxR = vx0 + (ax * tR)
    vyR = vy0 + (ay * tR)
    vzR = vz0 + (az * tR)

    return vxR, vyR, vzR


def calculate_flight_time(data):
    vyR = data["vyR"]
    ay = data["ay"]
    release_pos_y = data["release_pos_y"]

    return time_in_air(vyR, ay, release_pos_y, PLATE_LENGTH, True)


def calculate_induced_movement(data):
    plate_x = data["plate_x"]
    plate_z = data["plate_z"]

    vxR = data["vxR"]
    vyR = data["vyR"]
    vzR = data["vzR"]

    release_pos_x = data["release_pos_x"]
    release_pos_y = data["release_pos_y"]
    release_pos_z = data["release_pos_z"]

    tf = data["tf"]

    x_mvt = (
        plate_x - release_pos_x - (vxR / vyR) * (PLATE_LENGTH - release_pos_y)
    ) * INCHES_PER_FOOT
    z_mvt = (
        plate_z
        - release_pos_z
        - (vzR / vyR) * (PLATE_LENGTH - release_pos_y)
        + (0.5 * G * (tf ** 2))
    ) * INCHES_PER_FOOT

    return -x_mvt, z_mvt


def calculate_average_velocity_components(data):
    vxR = data["vxR"]
    vyR = data["vyR"]
    vzR = data["vzR"]

    ax = data["ax"]
    ay = data["ay"]
    az = data["az"]

    tf = data["tf"]

    vxbar = ((2 * vxR) + (ax * tf)) / 2
    vybar = ((2 * vyR) + (ay * tf)) / 2
    vzbar = ((2 * vzR) + (az * tf)) / 2

    return vxbar, vybar, vzbar


def calculate_average_velocity(data):
    vxbar = data["vxbar"]
    vybar = data["vybar"]
    vzbar = data["vzbar"]

    return n_dimensional_euclidean_distance(vxbar, vybar, vzbar)


def calculate_average_drag(data):
    ax = data["ax"]
    ay = data["ay"]
    az = data["az"]

    vxbar = data["vxbar"]
    vybar = data["vybar"]
    vzbar = data["vzbar"]

    vbar = data["vbar"]

    return -((ax * vxbar) + (ay * vybar) + ((az + G) * vzbar)) / vbar


def calculate_magnus_acceleration_components(data):
    ax = data["ax"]
    ay = data["ay"]
    az = data["az"]

    vxbar = data["vxbar"]
    vybar = data["vybar"]
    vzbar = data["vzbar"]

    adrag = data["adrag"]

    vbar = data["vbar"]

    amagx = ax + (adrag * vxbar / vbar)
    amagy = ay + (adrag * vybar / vbar)
    amagz = az + (adrag * vzbar / vbar) + G

    return amagx, amagy, amagz


def calculate_magnus_acceleration(data):
    amagx = data["amagx"]
    amagy = data["amagy"]
    amagz = data["amagz"]

    return n_dimensional_euclidean_distance(amagx, amagy, amagz)


def calculate_magnus_movement(data):
    amagx = data["amagx"]
    amagz = data["amagz"]

    tf = data["tf"]

    Mx = 0.5 * amagx * (tf ** 2) * INCHES_PER_FOOT
    Mz = 0.5 * amagz * (tf ** 2) * INCHES_PER_FOOT

    return Mx, Mz


def calculate_drag_coefficient(data):
    adrag = data["adrag"]
    vbar = data["vbar"]

    return adrag / ((vbar ** 2) * K)


def calculate_lift_coefficient(data):
    amag = data["amag"]
    vbar = data["vbar"]

    return amag / ((vbar ** 2) * K)


def calculate_spin_factor(data):
    Cl = data["Cl"]

    return 0.4 * Cl / (1 - (2.32 * Cl))


def calculate_transverse_spin(data):
    S = data["S"]
    vbar = data["vbar"]

    return 78.92 * S * vbar


def calculate_transverse_spin_components(data):
    spinT = data["spinT"]

    vxbar = data["vxbar"]
    vybar = data["vybar"]
    vzbar = data["vzbar"]

    amagx = data["amagx"]
    amagy = data["amagy"]
    amagz = data["amagz"]

    vbar = data["vbar"]

    amag = data["amag"]

    spinTx = spinT * ((vybar * amagz) - (vzbar * amagy)) / (amag * vbar)
    spinTy = spinT * ((vzbar * amagx) - (vxbar * amagz)) / (amag * vbar)
    spinTz = spinT * ((vxbar * amagy) - (vybar * amagx)) / (amag * vbar)

    return spinTx, spinTy, spinTz


def calculate_spin_check(data):
    spinTx = data["spinTx"]
    spinTy = data["spinTy"]
    spinTz = data["spinTz"]

    spinT = data["spinT"]

    return n_dimensional_euclidean_distance(spinTx, spinTy, spinTz) - spinT


def calculate_spin_axis(data):
    amagx = data["amagx"]
    amagz = data["amagz"]

    arctan = np.arctan2(amagz, -amagx)

    phi = np.where(amagz > 0, arctan * 180 / np.pi, 360 + arctan * 180 / np.pi)

    spin_axis_decimal = 3 - (1 / 30) * phi

    spin_axis_decimal = np.where(
        spin_axis_decimal <= 0, spin_axis_decimal + 12, spin_axis_decimal
    )

    spin_direction = []

    for axis in spin_axis_decimal:
        spin_direction.append(decimal_time_to_spin_direction(axis))

    return phi.round(0).astype("int64"), spin_axis_decimal, spin_direction


def calculate_spin_efficiency(data):
    spinT = data["spinT"]
    release_spin_rate = data["release_spin_rate"]

    return spinT / release_spin_rate


def calculate_gyro_angle(data):
    spin_eff = data["spin_eff"]

    spin_eff = np.where((spin_eff >= -1.0) & (spin_eff <= 1.0), spin_eff, -1.0)

    theta = np.where(spin_eff >= 0, (np.arccos(spin_eff) * 180) / np.pi, np.nan)

    return theta


def calculate_release_angle(data):
    # Release width
    release_pos_x = data["release_pos_x"]
    # Release height
    release_pos_z = data["release_pos_z"]

    return np.degrees(np.arctan2((release_pos_z - ECKERSLEY_LINE), abs(release_pos_x)))


# Move all of these to utils at some point maybe
def time_in_air(velocity, acceleration, position, adjustment, positive=True):
    if positive:
        direction_factor = 1
    else:
        direction_factor = -1

    return (
        -velocity
        - np.sqrt(
            (velocity ** 2)
            - (2 * acceleration * (direction_factor * (position - adjustment)))
        )
    ) / acceleration


def n_dimensional_euclidean_distance(*args):
    return np.sqrt(sum([component ** 2 for component in args]))


def n_dimensional_euclidean_distance_squared(*args):
    return sum([component ** 2 for component in args])
