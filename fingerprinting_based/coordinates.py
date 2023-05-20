import time
from typing import List

import pandas as pd
from sklearn.linear_model import LinearRegression

import constants as c
from scan_access_points import scan_access_points


def do_coordinates_predictions_with_fingerprinting(
    df: pd.DataFrame,
    access_point_names: List[str],
    coordinate_dimensions: int = 2
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
    x = []
    y = []

    for index, row in df.iterrows():
        x.append([row[name] for name in access_point_names])
        y.append([row[axis] for axis in ["x", "y", "z"][:coordinate_dimensions]])

    print(f"Example of x: {x[0]}")
    print(f"Example of y: {y[0]}")

    # Define the model
    model = LinearRegression()
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
        print(f"{values} -> {predictions}")

        if time.time() - time_passed >= 60:
            break
    print("Success!")
