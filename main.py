import pandas as pd


import constants as c
from data import gather_data, merge_csvs, walking_data_gatherer, reorder_columns
from fingerprinting_based.rooms import do_room_predictions_with_fingerprinting
from fingerprinting_based.coordinates import do_coordinates_predictions_with_fingerprinting
from signal_strength_based.coordinates import do_coordinates_predictions_with_signal_strength_formulas

# TODO: Move to another file
ROUTER_APARTMENT = "A4:BD:C4:2E:D7:70 (Dignajas Rozes)"
ROUTER_APARTMENT_5G = "A4:BD:C4:2E:D7:74 (Dignajas Rozes 5G)"
ROUTER_HOUSE = "C4:EA:1D:B9:49:5F (TNCAPB9495F)"
XIAOMI = "9A:62:AB:67:28:4B (PhPhPhone)"
ATOM = "94:B9:7E:A9:10:15 (M5Atom)"
STICK = "4C:75:25:CD:DD:E9 (M5Stick)"
IPHONE = "6A:51:48:7C:54:95 (RosaMaria \\xF0\\x9F\\x92\\x95)"


def run_fingerprinting_for_rooms():
    """ University """
    # TODO

    """ House """
    # training_df = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/house_training.csv")
    # testing_df = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/house_testing.csv")
    """room_id_to_name = {
        0: "Office, 2nd floor",
        1: "First bedroom, 2nd floor",
        2: "Upper stairs, 2nd floor",
        3: "Toilet, 2nd floor",
        4: "Second bedroom, 2nd floor",
        5: "Third bedroom, 2nd floor",
        6: "Hallway, 2nd floor",
        7: "Storage room, 2nd floor",
        8: "Lower stairs, 1st floor",
        9: "Boiler room, 1st floor",
        10: "Toilet, 1st floor",
        11: "Wardrobe, 1st floor",
        12: "Living room, 1st floor",
        13: "Kitchen, 1st floor",
        14: "Garage, 1st floor",
        15: "Terrace, 1st floor",
        16: "Outside, 1st floor",
    }
    do_room_predictions_with_fingerprinting(
        df=df,
        access_point_names=access_point_names_house,
        room_id_to_name=room_id_to_name,
        test_df=test_df
    )"""

    """ Apartment """
    # Changed all RosaMaria MACs to be 6A:51:48:7C:54:95 (RosaMaria \xF0\x9F\x92\x95), because they change all the time
    # Dignajas Rozes had -60, Dignajas Rozes 5G had -61
    training_df = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/apartment_training.csv")
    testing_df = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/apartment_testing_1d.csv")  # TODO: Also try 1h
    room_id_to_name = {
        0: "Bedroom",
        1: "Bathroom",
        2: "Living room",
        3: "Hallway"
    }

    experiments = [
        [XIAOMI],
        [ATOM, IPHONE],
        [STICK, IPHONE, ROUTER_APARTMENT],
        [STICK, IPHONE, ROUTER_APARTMENT, ATOM],
        [STICK, IPHONE, ROUTER_APARTMENT, ATOM, XIAOMI],
    ]

    for index, access_point_names in enumerate(experiments):
        print(f"Index: {index}")
        do_room_predictions_with_fingerprinting(
            df=training_df,
            test_df=testing_df,
            access_point_names=access_point_names,
            room_id_to_name=room_id_to_name,

        )
        input("Pause")
        # I want output:
        # * Accuracy in %
        # TODO:
        #   Heatmap with wrong borders
        #   Confusion matrix


def run_fingerprinting_for_coordinates():
    """ University """
    # TODO

    """ House """
    # TODO

    """ Apartment """
    training_df = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/apartment_training.csv")
    testing_df = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/apartment_testing_1d.csv")  # TODO: Also try 1h

    room_id_to_name = {
        0: "Bedroom",
        1: "Bathroom",
        2: "Living room",
        3: "Hallway"
    }

    experiments = [
        [XIAOMI],
        [ATOM, IPHONE],
        [STICK, IPHONE, ROUTER_APARTMENT],
        [STICK, IPHONE, ROUTER_APARTMENT, ATOM],
        [STICK, IPHONE, ROUTER_APARTMENT, ATOM, XIAOMI],
    ]

    # TODO: Do I need room names?

    for access_point_names in experiments:
        do_coordinates_predictions_with_fingerprinting(
            df=training_df,
            test_df=testing_df,  # # TODO: Fefinitely add testing df
            access_point_names=access_point_names,
            coordinate_dimensions=2
        )
        # I want output:
        # * Accuracy in m
        # TODO:
        #   Accuracy heatmap or that cool drawing idk


def run_trilateration_for_coordinates_and_rooms():
    # "signal_attenuation": 2,  # TODO: Does it make sense to move it to reference?
    # # TODO: Does it make sense to take it out?

    testing_df = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/apartment_testing_1d.csv")  # TODO: Also try 1h

    # Can I get distance and signal dynamically, by choosing some random room, then calculating the difference between using normal distance measure and signal we already have

    # Room: 2; Measurement: 4; x = 364; y = 385.
    # other coordinates
    # math dist.
    #
    # signal from table
    # done
    # What precision can I get if I listen a long time?

    signal_attenuation = 3.6
    information_about_apartment_router = {
        "name": ROUTER_APARTMENT,
        "signal_attenuation": signal_attenuation,
        "location": {
            "x": 645,
            "y": 274
        },
        "reference": {
            "distance": 302,  # TODO: Can we get this dynamically?
            "signal": -57,
        }
    }
    information_about_atom = {
        "name": ATOM,
        "signal_attenuation": signal_attenuation,
        "location": {
            "x": 541,
            "y": 727
        },
        "reference": {
            "distance": 385,
            "signal": -66,
        }
    }
    information_about_stick = {
        "name": STICK,
        "signal_attenuation": signal_attenuation,
        "location": {
            "x": 10,
            "y": 722
        },
        "reference": {
            "distance": 489,
            "signal": -66,
        }
    }
    information_about_iphone = {
        "name": IPHONE,
        "signal_attenuation": signal_attenuation,
        "location": {
            "x": 85,
            "y": 37
        },
        "reference": {
            "distance": 446,
            "signal": -58,
        }
    }
    information_about_xiaomi = {
        "name": XIAOMI,
        "signal_attenuation": signal_attenuation,
        "location": {
            "x": 318,
            "y": 253
        },
        "reference": {
            "distance": 140,
            "signal": -52,
        }
    }

    def apartment_coordinates_to_room_id(coordinates):
        # only works with 2D, because this is meant for apartments ony
        x, y = coordinates
        if y > 442:  # 0 or 1
            if x < 450:
                return 0
            else:
                return 1
        else:  # 2 or 3
            if x < 523:
                return 2
            else:
                return 3

    experiments = [
        [information_about_stick, information_about_iphone, information_about_apartment_router],
        [information_about_stick, information_about_iphone, information_about_apartment_router, information_about_atom],
        [information_about_stick, information_about_iphone, information_about_apartment_router, information_about_atom, information_about_xiaomi],
    ]

    # TODO: Do I need room names?

    for information_about_known_access_points in experiments:
        do_coordinates_predictions_with_signal_strength_formulas(
            test_df=testing_df,  # # TODO: Fefinitely add testing df
            information_about_known_access_points=information_about_known_access_points,
            dimensions=2,
            coordinates_to_room_id=apartment_coordinates_to_room_id
        )
        input("Pause! ")
        # I want output:
        # * Accuracy in m and in %
        # TODO:
        #   Something fancier?


if __name__ == "__main__":  # If this file is run directly
    mode = 10

    if mode == 1:  # Fingerprinting (rooms)
        run_fingerprinting_for_rooms()
    elif mode == 2:  # Fingerprinting (coordinates)
        run_fingerprinting_for_coordinates()
    elif mode == 3:  # Signal strength (coordinates and rooms)
        run_trilateration_for_coordinates_and_rooms()
    elif mode == 4:  # Gather data
        # TODO: We could also make these into constants
        # alerts_apartment = [STICK, IPHONE, ROUTER_APARTMENT, ROUTER_APARTMENT_5G, ATOM, XIAOMI]
        # alerts_house = [STICK, IPHONE, ROUTER_HOUSE, ATOM]
        # alerts_university = []
        alerts_random = [STICK]
        df = gather_data(
            interface=c.NETWORK_INTERFACE,
            include_measurement_index=True,
            include_room_index=True,
            coordinate_dimensions=0,
            batch_size=20,
            batch_time_difference=0.1,
            alert_presence_for_access_points=alerts_random
        )
        df.to_csv("grid-data.csv")
    elif mode == 5:  # Real time walking data
        walking_data_gatherer(
            interface="wlp0s20f3",
            how_many_seconds=10,
        )
    elif mode == 6:  # Merge .csv files from data gathering
        files = ["14_10-21.csv", "16_15-21.csv", "16_8-14.csv", "1.csv", "301.csv", "303.csv", "305.csv", "345_9-24.csv", "3.csv", "5.csv", "14_1-9.csv", "16_1-7.csv", "18.csv", "2.csv", "302.csv", "304.csv", "345_1-8.csv", "347.csv", "4.csv", "6.csv"]
        merge_csvs(files)
    elif mode == 7:
        from visualize import go_go_go
        go_go_go()
    elif mode == 8:  # sort csv
        file_path = "/home/ronaldsz/Repositories/wifi-localization/data (copy)/university_testing.csv"
        testing_df = pd.read_csv(file_path)
        # print(testing_df)
        df = testing_df.sort_values(["room_index", "measurement_index", "batch_index"])
        df.to_csv("university_testing.csv")
    elif mode == 9:  # Reorder columns
        file_path = "/home/ronaldsz/Repositories/wifi-localization/data (copy)/house_testing.csv"
        df = pd.read_csv(file_path)
        # df = reorder_columns(df, priority_columns=[ROUTER_APARTMENT, ROUTER_APARTMENT_5G, IPHONE, XIAOMI, STICK, ATOM])
        df = reorder_columns(df, priority_columns=[ROUTER_HOUSE, IPHONE, STICK, ATOM])
        # df = reorder_columns(df)
        df.to_csv("new_house_testing.csv")
    elif mode == 10:  # Strongest APs and their names
        file_path = "/home/ronaldsz/Repositories/wifi-localization/0_routers/304.csv"
        df = pd.read_csv(file_path)
        aps = {}
        for col in list(df.columns):
            signal_strength = round(df[col].mean())
            aps[col] = signal_strength

        strongest_aps = sorted(aps.items(), key=lambda x: x[1], reverse=True)
        strongest_aps = dict(strongest_aps)

        for name, signal_strength in strongest_aps.items():
            if name not in ["batch_index", "Unnamed: 0", "room_index", "measurement_index"]:
                print(f"{name}: {signal_strength}")
    else:  # TODO: Unfinished stuff
        """
        # from fingerprinting_based.data import gather_data, filter_columns
        df = gather_data(
            interface="wlp0s20f3",
            include_measurement_index=True,
            include_room_index=True,
            coordinate_dimensions=0
        )
        df.to_csv("wifi-localization-full.csv")

        # TODO: Create a file: known_access_points.*, which included in .gitignore
        #   So I don't have to commit the SSIDs and MAC addresses of my APs.
        columns_to_stay = [
            "measurement_index",
            "room_index"
        ]
        df_filtered = filter_columns(df, columns_to_stay)
        print(df_filtered)
        df.to_csv("wifi-localization-filtered.csv")

        columns_to_rename = {
            "measurement_index": "measurement",
            "room_index": "room"
        }
        df_renamed = df_filtered.rename(columns=columns_to_rename)
        print(df_renamed)
        df.to_csv("wifi-localization-renamed.csv")
        """
        pass
