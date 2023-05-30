import time
from pprint import pprint
from typing import Dict, List

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.svm import SVC

import constants as c
from scan_access_points import scan_access_points


def do_room_predictions_with_fingerprinting(
    df: pd.DataFrame,
    access_point_names: List[str],
    room_id_to_name: Dict[int, str],
    test_df: pd.DataFrame = None
):
    """ Trains an SVC model on the passed data filtering to only the given
    access points, then tries to predict the room for a minute.

    Model trains on the passed data: [AP_1, AP_2..., AP_N] -> Room

    Args:
        df: Dataframe with measurements with metadata. We assume it has a
            columns named "room_index". We assume that at least 1 sample of
            each class (room) is present, although more might need to be
            present to have meaningful results.
        access_point_names: List of access point names to include in the
            prediction process (order is important).
        room_id_to_name: Dictionary mapping room index present in data to a
            room name, for example, "Living room".

    Returns:
        None.
    """
    x = []
    y = []

    print(df.columns)
    for index, row in df.iterrows():
        # print(access_point_names)
        print(row)
        x.append([row[name] for name in access_point_names])
        y.append(row["room_index"])

    print(f"Example of x: {x[0]}")
    print(f"Example of y: {y[0]} ({room_id_to_name[y[0]]})")

    # Define the model
    # Let's use Support Vector Classification (SVC)
    model = SVC()
    # Fit the model
    print("Training...")
    model.fit(x, y)

    interface = c.NETWORK_INTERFACE
    time_passed = time.time()

    if test_df is None:  # TODO: Do we need this, Idk, maybe realtime, but then need other, dik think about
        print("Predicting...")
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
            print(f"{values} -> {room_id_to_name[predictions]}")

            if time.time() - time_passed >= 60:
                break
        print("Success!")
    else:
        # print(test_df)
        total = 0
        correct = 0
        confusion_matrix = [  # np array maybe easier
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

        values = [0] * len(access_point_names)
        # Wrong DF -> Wrong Results
        for index, row in test_df.iterrows():
            for ap_index, access_point in enumerate(access_point_names):
                values[ap_index] = row[access_point]  # This assumes that there are no NaNs

            # Make a prediction
            predictions = model.predict([values])
            # Summarize the prediction
            predictions = predictions[0]

            total += 1
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
        print(f"Final accuracy: {accuracy}")

        # plt.imshow(confusion_matrix)
        # plt.title("Actual vs. predicted")
        # plt.show()
