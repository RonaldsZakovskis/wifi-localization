import time
from typing import Dict, List

import pandas as pd

from scan_access_points import scan_access_points


def gather_data(
    interface: str,
    include_measurement_index: bool = True,
    include_room_index: bool = True,
    coordinate_dimensions: int = 0
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
        if include_measurement_index:
            details["measurement_index"] = int(input("Measurement index: "))
        if include_room_index:
            details["room_index"] = int(input("Room index: "))
        if coordinate_dimensions >= 1:
            details["x"] = float(input("x: "))
        if coordinate_dimensions >= 2:
            details["y"] = float(input("y: "))
        if coordinate_dimensions == 3:
            details["z"] = float(input("z: "))
        return details

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
        access_points = scan_access_points(interface=interface)
        for access_point in access_points:
            column_name = f"{access_point['address']} ({access_point['ssid']})"
            df.loc[counter, column_name] = access_point["signal"]
        for k, v in measurements_details.items():
            df.loc[counter, k] = v
        print("You can move again!")

        continue_gathering = int(input("Continue measuring (0 = no; 1 = yes)? "))
        if continue_gathering == 0:
            break
        # Starting the next step
        measurements_details = get_measurement_details()
        counter += 1

    print("This is the final df:")
    print(df)
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
