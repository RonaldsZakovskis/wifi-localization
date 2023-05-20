import time
from typing import Dict, List

import pandas as pd
from sklearn.svm import SVC

import constants as c
from scan_access_points import scan_access_points


def do_room_predictions_with_fingerprinting(
    df: pd.DataFrame,
    access_point_names: List[str],
    room_id_to_name: Dict[int, str]
):
    """ Trains an SVC model on the passed data filtering to only the given
    access points, then tries to predict the room for a minute.

    Model trains on the passed data: [AP_1, AP_2..., AP_N] -> Room

    Args:
        df: Dataframe with measurements with metadata. We assume it has a
            columns named "room". We assume that at least 1 sample of each
            class (room) is present, although more might need to be present to
            have meaningful results.
        access_point_names: List of access point names to include in the
            prediction process (order is important).
        room_id_to_name: Dictionary mapping room index present in data to a
            room name, for example, "Living room".

    Returns:
        None.
    """
    x = []
    y = []

    for index, row in df.iterrows():
        x.append([row[name] for name in access_point_names])
        y.append(row["room"])

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
