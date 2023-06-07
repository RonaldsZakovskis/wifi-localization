import math
import time
from pprint import pprint
from typing import Dict, List

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.metrics import f1_score, confusion_matrix, ConfusionMatrixDisplay

import constants as c
from scan_access_points import scan_access_points
from helpers import get_batch_mean_df, get_df_with_specific_measurements


def do_room_predictions_with_fingerprinting(
    training_df: pd.DataFrame,
    testing_df: pd.DataFrame = None,
    specific_measurements = None,
    access_point_names: List[str] = [],
    room_id_to_name: Dict[int, str] = {},
    training_batch_size: int = None,
    testing_batch_size: int = None,
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
    if training_batch_size:
        training_df = get_batch_mean_df(df=training_df, batch_size=training_batch_size)

    if specific_measurements:
        training_df = get_df_with_specific_measurements(df=training_df, specific_measurements=specific_measurements)

    # TODO: It seems that batching for training gives benefits, but make sure

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
        y.append(row[c.ROOM_INDEX_COLUMN])

    # print(f"Example of x: {x[0]}")
    # print(f"Example of y: {y[0]} ({room_id_to_name[y[0]]})")

    # Define the model
    # Let's use Support Vector Classification (SVC)
    model = SVC()
    # Fit the model
    # print("Training...")
    model.fit(x, y)

    if testing_df is None:
        # TODO: Do we need this, Idk, maybe realtime, but then need other, dik think about
        # TODO: Maybe throw this out in different realtime functions
        """#print("Predicting...")
        
        interface = c.NETWORK_INTERFACE
        time_passed = time.time()
        
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
            #print(f"{values} -> {room_id_to_name[predictions]}")

            if time.time() - time_passed >= 60:
                break
        #print("Success!")"""
        pass
    else:
        if testing_batch_size:
            testing_df = get_batch_mean_df(df=testing_df, batch_size=testing_batch_size)

        # TODO: How to draw confusioon matrix if you have a lot of uunmerger batches
        #   Harder to say real guesses, the most chosen? Maybe.
        total = 0
        correct = 0
        """confusion_matrix = [  # np array maybe easier
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
        ]"""

        values = [nan_value] * len(access_point_names)
        y_true = []
        y_pred = []
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

            # Make a prediction
            predictions = model.predict([values])
            # Summarize the prediction
            predictions = predictions[0]

            total += 1
            if predictions == row[c.ROOM_INDEX_COLUMN]:
                correct += 1

            y_pred.append(predictions)
            y_true.append(row[c.ROOM_INDEX_COLUMN])

            # confusion_matrix[int(row[c.ROOM_INDEX_COLUMN])][int(predictions)] += 1

            # print(f"Predicted {predictions}, Actual {row['room_index']}")
            # print(f"{values} -> {room_id_to_name[predictions]}")
            # print(f"Rolling precision = {correct / total}\n")
            # Do some analysis, how far are the wrong predictions, hopefully there arent any that are many far away
            # Rolling precision = 0.7481422924901185

        weighted_f1_score = f1_score(y_true=y_true, y_pred=y_pred, average="weighted") * 100
        print(f"Weighted F1 Score: {weighted_f1_score:.2f}%")

        # conf_matrix = confusion_matrix(y_true=y_true, y_pred=y_pred)
        # print(conf_matrix)
        # Should I do % of guesses or smt?

        # pprint(confusion_matrix)
        #for actual in range(17):
        #    confusion_sum = sum(confusion_matrix[actual])
        #    a = 0 if confusion_sum == 0 else confusion_matrix[actual][actual] / confusion_sum
        #    a *= 100
        #    # print(f"{actual} was guessed correctly {a:.2f}% of times")
        # TODO: Get a nice way to represent the confusion matrix

        # disp = ConfusionMatrixDisplay(confusion_matrix=conf_matrix)
        # disp.plot()
        # plt.show()

        # plt.imshow(confusion_matrix)
        # plt.title("Actual vs. predicted")
        # plt.show()

        # Let's print the accuracy in %
        accuracy = (correct / total) * 100
        print(f"Final accuracy: {accuracy:.2f}%")
    # TODO: Get #room.measurement to prediction (later in heatmap)
