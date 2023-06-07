import math
import time
from typing import List, Dict

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

import constants as c
from scan_access_points import scan_access_points
from helpers import get_batch_mean_df, get_df_with_specific_measurements


def do_coordinates_predictions_with_fingerprinting(
    training_df: pd.DataFrame,
    testing_df: pd.DataFrame = None,
    specific_measurements = None,
    access_point_names: List[str] = [],
    room_id_to_name: Dict[int, str] = {},
    training_batch_size: int = None,
    testing_batch_size: int = None,
    coordinate_dimensions: int = 2,  # This is extra for rooms
):
    """ Trains a Linear Regression model on the passed data filtering to only
        the given access points and dimensions, then tries to predict the
        location for a minute.

    Model trains on the passed data: [AP_1, AP_2..., AP_N] -> [x, (y, (z))]

    Args:
        df: Dataframe with measurements with metadata. We assume it has columns
            named "x" (if coordinate_dimensions is at least 1), "y" (if
            coordinate_dimensions is at least 2) and "z" (if
            coordinate_dimensions is 3). We assume that at least 1 sample is
            present, although more should be present to have meaningful
            results.
        access_point_names: List of access point names to include in the
            prediction process (order is important).
        coordinate_dimensions: Number of dimensions to predict for. Must be an
            integer in [1, 2, 3], that is, 1 is for (x), 2 is for (x, y) and
            3 is for (x, y, z).

    Returns:
        None.
    """
    from helpers import get_batch_mean_df

    if training_batch_size:
        training_df = get_batch_mean_df(df=training_df, batch_size=training_batch_size)

    if specific_measurements:
        training_df = get_df_with_specific_measurements(df=training_df, specific_measurements=specific_measurements)

    nan_value = -99  # TODO: Not sure what to do with this

    x = []
    y = []

    for index, row in training_df.iterrows():
        values = [nan_value] * len(access_point_names)
        for ap_index, access_point in enumerate(access_point_names):
            if isinstance(access_point, str):
                if not math.isnan(row[access_point]):
                    values[ap_index] = row[access_point]
            else:
                sub_values = [nan_value] * len(access_point)
                for sub_ap_index, name in enumerate(access_point):
                    if not math.isnan(row[name]):
                        sub_values[sub_ap_index] = row[name]
                values[ap_index] = max(sub_values)
        x.append(values)
        y.append([row[axis] for axis in ["x", "y", "z"][:coordinate_dimensions]])

    # print(f"Example of x: {x[0]}")
    # print(f"Example of y: {y[0]}")

    # Define the model
    model = LinearRegression()
    # Fit the model
    # print("Training...")
    model.fit(x, y)

    # interface = c.NETWORK_INTERFACE
    # time_passed = time.time()

    if testing_df is None:
        # TODO: Do we need this, Idk, maybe realtime, but then need other, dik think about
        """# print("Predicting...")
        while True:
            access_points = scan_access_points(interface=interface)
            values = [0] * len(access_point_names)
            for access_point in access_points:
                column_name = f"{access_point['address']} ({access_point['ssid']})"
                for index, name in enumerate(access_point_names):
                    if column_name == name:
                        values[index] = access_point["signal"]

            # Make a prediction
            predictions = model.predict([values])
            # Summarize the prediction
            predictions = predictions[0]
            # print(f"{values} -> {predictions}")

            if time.time() - time_passed >= 60:
                break
        # print("Success!")"""
        pass
    else:
        if testing_batch_size:
            testing_df = get_batch_mean_df(df=testing_df, batch_size=testing_batch_size)

        values = [nan_value] * len(access_point_names)
        total = 0.0
        for index, row in testing_df.iterrows():
            for ap_index, access_point in enumerate(access_point_names):
                if isinstance(access_point, str):
                    if not math.isnan(row[access_point]):
                        values[ap_index] = row[access_point]
                else:
                    sub_values = [nan_value] * len(access_point)
                    for sub_ap_index, name in enumerate(access_point):
                        if not math.isnan(row[name]):
                            sub_values[sub_ap_index] = row[name]
                    values[ap_index] = max(sub_values)
            actual_coordinates = [row[axis] for axis in ["x", "y", "z"][:coordinate_dimensions]]

            # Make a prediction
            predictions = model.predict([values])
            # Summarize the prediction
            predicted_coordinates = list(predictions[0])

            distance_error = math.dist(actual_coordinates, predicted_coordinates)
            # print(f"Distance error: {distance_error}")
            total += distance_error
        error_in_distance = (total / len(testing_df)) / 100
        print(f"Error in distance: {error_in_distance:.2f}")

        """          total += 1
            if predictions == row['room_index']:
                correct += 1
            confusion_matrix[int(row['room_index'])][int(predictions)] += 1

            print(f"Predicted {predictions}, Actual {row['room_index']}")
            print(f"{values} -> {room_id_to_name[predictions]}")
            print(f"Rolling precision = {correct / total}\n")
            # Do some analysis, how far are the wrong predictions, hopefully there arent any that are many far away
            # Rolling precision = 0.7481422924901185
        pprint(confusion_matrix)
        for actual in range(17):
            confusion_sum = sum(confusion_matrix[actual])
            a = 0 if confusion_sum == 0 else confusion_matrix[actual][actual] / confusion_sum
            a *= 100
            print(f"{actual} was guessed correctly {a:.2f}% of times")

        accuracy = correct / total
        print(f"Final accuracy: {accuracy}")"""

        # plt.imshow(confusion_matrix)
        # plt.title("Actual vs. predicted")
        # plt.show()