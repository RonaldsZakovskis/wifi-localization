import math
from typing import List

import pandas as pd
import matplotlib.pyplot as plt

import visualize_configurations as v


def go_go_go():
    # 1 - University, 2 - House (1st floor), 3 - House (2nd floor), 4 - Apartment
    location = 1

    if location == 1:
        df = pd.read_csv("data/university_training.csv")
        room_id_to_measurements = v.amount_of_measurements_university
        rooms = v.rooms_university
        measurements = v.measurements_university
        numbers = v.numbers_university
        rows = v.rows_university
        columns = v.columns_university
    elif location == 2:
        df = pd.read_csv("data/house_training.csv")
        room_id_to_measurements = v.amount_of_measurements_house_1st_floor
        rooms = v.rooms_house_1st_floor
        measurements = v.measurements_house_1st_floor
        numbers = v.numbers_house_1st_floor
        rows = v.rows_house_1st_floor
        columns = v.columns_house_1st_floor
    elif location == 3:
        df = pd.read_csv("data/house_training.csv")
        room_id_to_measurements = v.amount_of_measurements_house_2nd_floor
        rooms = v.rooms_house_2nd_floor
        measurements = v.measurements_house_2nd_floor
        numbers = v.numbers_house_2nd_floor
        rows = v.rows_house_2nd_floor
        columns = v.columns_house_2nd_floor
    else:  # location == 3
        df = pd.read_csv("data/apartment_training.csv")
        room_id_to_measurements = v.amount_of_measurements_apartment
        rooms = v.rooms_apartment
        measurements = v.measurements_apartment
        numbers = v.numbers_apartment
        rows = v.rows_apartment
        columns = v.columns_apartment

    middle = int(math.ceil(len(df)/2))

    fifty_percent_columns = []
    for column in df.columns:
        if count_non_nans(list(df[column])) >= middle:
            fifty_percent_columns.append(column)

    if "Unnamed: 0" in fifty_percent_columns:
        fifty_percent_columns.remove("Unnamed: 0")
    fifty_percent_columns.remove("measurement_index")
    fifty_percent_columns.remove("room_index")
    fifty_percent_columns.remove("batch_index")

    print("Columns that were present 50% total:")
    print(fifty_percent_columns)
    print(len(fifty_percent_columns), "\n")

    # Non-(MAC (SSID)) columns are:
    #   Unnamed: 0
    #   measurement_index
    #   room_index
    #   batch_index

    access_points = {}  # room_id: measurement_id

    min_aps_found = None
    max_aps_found = None
    for room_index, amount_of_measurements in room_id_to_measurements.items():
        access_points[room_index] = {}
        room_df = df[df["room_index"] == room_index]
        for measurement in range(1, amount_of_measurements + 1):
            measurement_df = room_df[room_df["measurement_index"] == measurement]
            access_points_found = 0
            for column in measurement_df.columns:
                if count_non_nans(list(measurement_df[column])) != 0:
                    access_points_found += 1
            access_points[room_index][measurement] = access_points_found
            print(f"Room: {room_index}; Measurement: {measurement}; APs: {access_points_found}")
            if min_aps_found is None or access_points_found < min_aps_found:
                min_aps_found = access_points_found
            if max_aps_found is None or access_points_found > max_aps_found:
                max_aps_found = access_points_found

    print(f"Min APs detected: {min_aps_found}")
    print(f"Max APs detected: {max_aps_found}")

    for row_id in range(rows):
        for col_id in range(columns):
            room_id = rooms[row_id][col_id]
            if room_id != -1:
                measurement_id = measurements[row_id][col_id]
                numbers[row_id][col_id] = access_points[room_id][measurement_id]
            else:
                numbers[row_id][col_id] = -1

    fig, ax = plt.subplots(1, 1)

    # just rooms with max 7 you can print
    img = ax.imshow(numbers, cmap='viridis', vmin=0,
                    vmax=max_aps_found)  # , extent=[0, 10, 0, 10])  # TODO: max is aps found

    plt.xlabel("x (m)")
    plt.ylabel("y (m)")

    fig.colorbar(img, label="Uztvertie piekļuves punkti")

    # plt.title()

    plt.show()

    print(f"50% number: {len(fifty_percent_columns)}")


def count_non_nans(a: List[float]) -> int:
    non_nans = 0
    for value in a:
        if not math.isnan(value):
            non_nans += 1
    return non_nans
