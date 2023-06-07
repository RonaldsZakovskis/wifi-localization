import time
from typing import Dict, List

import pandas as pd

from scan_access_points import scan_access_points


def gather_data(
    interface: str,
    include_measurement_index: bool = True,
    include_room_index: bool = True,
    coordinate_dimensions: int = 0,
    batch_size: int = 1,  # TODO
    batch_time_difference: float = 0.1,  # TODO
    alert_presence_for_access_points: List[str] = None
) -> pd.DataFrame:
    """ Gathers information about nearby access points by taking multiple
        measurements, potentially asking for more information about each
        measurement.

    Args:
        interface: Name of the network interface, for example, "wlan0". If you
            are not sure about your necessary network interface name, enter the
            "iwconfig" in the terminal.
        include_measurement_index: If true, index of the measurement will be
            prompted. It might be useful when you want to retake a specific
            measurement, or you want to take the measurements in a specific
            order, or example, 5-1-3-2-4, instead of 1-2-3-4-5.
        include_room_index: If true, index of the room will be prompted.
        coordinate_dimensions: Number of dimensions to include. Must be an
            integer in [0, 1, 2, 3], that is, 1 is for (x), 2 is for (x, y) and
            3 is for (x, y, z).
        alert_presence_for_access_points: List of known access points to alert
            if they are not present in the scanned access points. This might be
            very useful if you have set up several access points, and one of
            them suddenly turns off, so you don't do a lot of measurements and
            afterward see "Oh, no, it turned off!" (as sometimes access points
            have a tendency to turn off (phones) or the battery to die
            (microcomputers)).

    Returns:
        df: Taken measurements holding information about the nearby access
            points and metadata about the specific measurement.
    """
    def get_measurement_details() -> Dict:
        """ Get the necessary details for the following measurement by
            optionally asking for input many times.

        Args:
            None.

        Returns:
            details: Dictionary holding the necessary details for the following
                measurement.
        """
        print("--------------------------------------------")
        details = {}
        if include_room_index:
            details["room_index"] = int(input("Room index: "))
        if include_measurement_index:
            details["measurement_index"] = int(input("Measurement index: "))
        if coordinate_dimensions >= 1:
            details["x"] = float(input("x: "))
        if coordinate_dimensions >= 2:
            details["y"] = float(input("y: "))
        if coordinate_dimensions == 3:
            details["z"] = float(input("z: "))
        return details

    if alert_presence_for_access_points is None:
        alert_presence_for_access_points = []

    # Setup
    counter = 0
    df = pd.DataFrame()

    print("Data gathering started!")
    measurements_details = get_measurement_details()
    while True:
        for i in range(5, 0, -1):
            print(f"Measurement in {i} second(s)...")
            time.sleep(1)
        print("Stand still...")
        known_access_point_presence = [0] * len(alert_presence_for_access_points)
        for i in range(batch_size):
            access_points = scan_access_points(interface=interface)
            print(f"({i + 1}/{batch_size}) {len(access_points)} APs detected!")  # TODO: Make optional, with verbose parameter?
            for access_point in access_points:
                column_name = f"{access_point['address']} ({access_point['ssid']})"

                if column_name in alert_presence_for_access_points:
                    known_access_point_presence[alert_presence_for_access_points.index(column_name)] += 1

                df.loc[counter, column_name] = access_point["signal"]
            for k, v in measurements_details.items():
                df.loc[counter, k] = v
            df.loc[counter, "batch_index"] = i + 1
            time.sleep(batch_time_difference)
            counter += 1
        for index, access_point_was_present in enumerate(known_access_point_presence):
            if access_point_was_present == 0:
                print(f"{alert_presence_for_access_points[index]} was never detected!")
            elif access_point_was_present < batch_size:
                print(f"{alert_presence_for_access_points[index]} sometimes wasn't detected!")

        print("You can move again!")

        continue_gathering = int(input("Continue measuring (0 = no; 1 = yes)? "))
        if continue_gathering == 0:
            break
        # Starting the next step
        measurements_details = get_measurement_details()

    return df


def filter_columns(
    df: pd.DataFrame,
    columns_to_leave: List[str]
) -> pd.DataFrame:
    """ Gathers information about nearby access points by taking multiple
        measurements, potentially asking for more information about each
        measurement.

    Args:
        df: A pandas dataframe.
        columns_to_leave: A list of columns to keep in the dataframe.

    Returns:
        df: The same passed dataframe, but with filtered columns.
    """
    columns = df.columns
    for column in columns:
        if column not in columns_to_leave:
            df = df.drop(columns=[column])
    return df


def merge_csvs(file_names: List[str]):
    df = pd.DataFrame()
    for file in file_names:
        data = pd.read_csv(file)
        df = pd.concat([df, data], axis=0)
    df.to_csv("merged_files.csv", index=False)
    #training_data = pd.read_csv("data/house_training.csv")
    #print(training_data)
    #a = training_data[training_data['room_index'] == 15]
    # print(a[a['measurement_index'] == 2].shape)

    #testing_data = pd.read_csv("data/house_testing.csv")
    #print(testing_data)
    #b = testing_data[testing_data['room_index'] == 15]
    # print(b[b['measurement_index'] == 2].shape)

    #for i in range(1, 28):
    # #   print(i)
    #    print(a[a['measurement_index'] == i].shape)
    #    print(b[b['measurement_index'] == i].shape)


def reorder_columns(df: pd.DataFrame, priority_columns = []) -> pd.DataFrame:
    cols = df.columns.tolist()
    new_order = priority_columns
    if "room_index" in cols:
        new_order.append("room_index")
    if "measurement_index" in cols:
        new_order.append("measurement_index")
    if "batch_index" in cols:
        new_order.append("batch_index")
    if "x" in cols:
        new_order.append("x")
    if "y" in cols:
        new_order.append("y")
    if "z" in cols:
        new_order.append("z")

    for col in new_order:
        print(col)
        cols.remove(col)
    new_order += cols
    df = df[new_order]
    return df


def walking_data_gatherer(interface: str, how_many_seconds: int = 60):
    print("Data gathering started!")

    # Setup
    counter = 0
    df = pd.DataFrame()
    start = time.time()

    while time.time() - start < how_many_seconds:
        time_passed = time.time() - start
        access_points = scan_access_points(interface=interface)
        df.loc[counter, "time_passed"] = time.time() - start
        print(f"Time passed: {time_passed:.3f}/{how_many_seconds:.3f} seconds ||| APs detected: {len(access_points)}")
        for access_point in access_points:
            column_name = f"{access_point['address']} ({access_point['ssid']})"
            df.loc[counter, column_name] = access_point["signal"]
        counter += 1

    df.to_csv("movement-data.csv")


def long_data_gatherer(interface: str, how_many_seconds: int, pause_seconds):
    print("Data gathering started!")

    # Setup
    counter = 0
    df = pd.DataFrame()
    start = time.time()

    while time.time() - start < how_many_seconds:
        time_passed = time.time() - start
        access_points = scan_access_points(interface=interface)
        df.loc[counter, "time_passed"] = time.time() - start
        print(f"Time passed: {time_passed:.3f}/{how_many_seconds:.3f} seconds ||| APs detected: {len(access_points)}")
        for access_point in access_points:
            column_name = f"{access_point['address']} ({access_point['ssid']})"
            df.loc[counter, column_name] = access_point["signal"]
        counter += 1
        time.sleep(pause_seconds)

    df.to_csv("long-data.csv")
