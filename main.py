import pandas as pd


import constants as c
from data import gather_data, merge_csvs, walking_data_gatherer, reorder_columns, long_data_gatherer
from fingerprinting_based.rooms import do_room_predictions_with_fingerprinting
from fingerprinting_based.coordinates import do_coordinates_predictions_with_fingerprinting
from signal_strength_based.coordinates import do_coordinates_predictions_with_signal_strength_formulas


def run_fingerprinting_for_rooms():
    """ University """
    training_df = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/grid/university/training.csv")
    testing_df = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/grid/university/testing.csv")
    room_id_to_name = c.ROOM_ID_TO_NAME_UNIVERSITY
    experiments = [
        # [
        #     c.ROUTER_UNIVERSITY_3,
        #     c.ROUTER_UNIVERSITY_14_3,
        #     c.ROUTER_UNIVERSITY_16_7,
        # ],
        # [
        #     c.ROUTER_UNIVERSITY_3,
        #     c.ROUTER_UNIVERSITY_14_3,
        #     c.ROUTER_UNIVERSITY_16_7,
        #     c.ROUTER_UNIVERSITY_18_1,
        #     c.ROUTER_UNIVERSITY_301,
        #     c.ROUTER_UNIVERSITY_303,
        #     c.ROUTER_UNIVERSITY_304,
        #     c.ROUTER_UNIVERSITY_305,
        #     c.ROUTER_UNIVERSITY_345_18
        # ],
        c.ROUTERS_UNIVERSITY,
    ]
    specific_measurements_one_each_room = [
        (1, 4),
        (2, 4),
        (3, 4),
        (4, 4),
        (5, 4),
        (6, 4),
        (14, 3),
        (16, 5),
        (18, 1),
        (301, 4),
        (302, 6),
        (303, 9),
        (304, 3),
        (305, 6),
        (345, 20),
        (347, 3),
    ]
    specific_measurements_four_each_room = [
        (1, 1),
        (1, 3),
        (1, 4),
        (1, 6),
        (2, 1),
        (2, 3),
        (2, 5),
        (2, 8),
        (3, 1),
        (3, 4),
        (3, 5),
        (3, 7),
        (4, 1),
        (4, 3),
        (4, 5),
        (4, 7),
        (5, 1),
        (5, 5),
        (5, 6),
        (5, 8),
        (6, 1),
        (6, 3),
        (6, 4),
        (6, 6),
        (14, 1),
        (14, 3),
        (14, 19),
        (14, 21),
        (16, 1),
        (16, 7),
        (16, 15),
        (16, 21),
        (18, 1),
        (18, 3),
        (18, 13),
        (18, 15),
        (301, 1),
        (301, 2),
        (301, 3),
        (301, 4),
        (302, 1),
        (302, 2),
        (302, 5),
        (302, 6),
        (303, 1),
        (303, 3),
        (303, 7),
        (303, 9),
        (304, 1),
        (304, 3),
        (304, 7),
        (304, 9),
        (305, 1),
        (305, 2),
        (305, 5),
        (305, 6),
        (345, 1),
        (345, 8),
        (345, 17),
        (345, 24),
        (347, 1),
        (347, 2),
        (347, 3),
    ]
    training_batch_size = 30
    testing_batch_size = 1

    """ House """
    """training_df = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/grid/house/training.csv")
    testing_df = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/grid/house/testing.csv")
    room_id_to_name = c.ROOM_ID_TO_NAME_HOUSE
    experiments = [
        [c.ROUTER_HOUSE],
        [c.ROUTER_HOUSE, c.IPHONE],
        [c.ROUTER_HOUSE, c.IPHONE, c.ATOM],
        [c.ROUTER_HOUSE, c.IPHONE, c.ATOM, c.STICK],
    ]
    specific_measurements_one_each_room = [
        (0, 6),
        (1, 5),
        (2, 4),
        (3, 25),
        (4, 12),
        (5, 4),
        (6, 8),
        (7, 1),
        (8, 1),
        (9, 8),
        (10, 14),
        (11, 6),
        (12, 6),
        (13, 3),
        (14, 1),
        (15, 1),
        (16, 2),
    ]
    specific_measurements_four_each_room = [
        (0, 1),
        (0, 11),
        (0, 24),
        (0, 39),
        (1, 1),
        (1, 9),
        (1, 19),
        (1, 27),
        (2, 1),
        (2, 2),
        (2, 3),
        (2, 4),
        (3, 1),
        (3, 6),
        (3, 25),
        (3, 30),
        (4, 1),
        (4, 3),
        (4, 22),
        (4, 24),
        (5, 1),
        (5, 2),
        (5, 3),
        (5, 4),
        (6, 1),
        (6, 5),
        (6, 11),
        (6, 14),
        (7, 1),
        (7, 3),
        (7, 7),
        (7, 9),
        (8, 1),
        (8, 2),
        (8, 3),
        (9, 1),
        (9, 2),
        (9, 9),
        (9, 10),
        (10, 1),
        (10, 6),
        (10, 13),
        (10, 22),
        (11, 1),
        (11, 3),
        (11, 4),
        (11, 6),
        (12, 1),
        (12, 3),
        (12, 13),
        (12, 15),
        (13, 1),
        (13, 2),
        (13, 5),
        (13, 6),
        (14, 1),
        (14, 4),
        (14, 13),
        (14, 16),
        (15, 1),
        (15, 2),
        (15, 3),
        (16, 1),
        (16, 2),
        (16, 3),
        (16, 4),
    ]
    training_batch_size = 25
    testing_batch_size = 1"""

    """ Apartment """
    """training_df = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/grid/apartment/training.csv")
    # testing_df = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/grid/apartment/testing_1h.csv")
    testing_df = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/grid/apartment/testing_1d.csv")
    # testing_df = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/grid/apartment/testing_1w.csv")
    room_id_to_name = c.ROOM_ID_TO_NAME_APARTMENT
    experiments = [
        [c.ROUTER_APARTMENT],
        [c.ROUTER_APARTMENT, c.STICK],
        [c.ROUTER_APARTMENT, c.STICK, c.IPHONE],
        [c.ROUTER_APARTMENT, c.STICK, c.IPHONE, c.ATOM],
        [c.ROUTER_APARTMENT, c.STICK, c.IPHONE, c.ATOM, c.XIAOMI],
    ]
    specific_measurements_one_each_room = [
        (0, 12),
        (1, 5),
        (2, 5),
        (3, 1)
    ]
    specific_measurements_four_each_room = [
        (0, 1),
        (0, 4),
        (0, 9),
        (0, 12),
        (1, 1),
        (1, 2),
        (1, 5),
        (1, 6),
        (2, 1),
        (2, 5),
        (2, 16),
        (2, 20),
        (3, 1),
        (3, 2),
        (3, 3),
        (3, 4)
    ]
    training_batch_size = 50
    testing_batch_size = 1"""

    for index, access_point_names in enumerate(experiments):
        print(f"Experiment {index}:")
        do_room_predictions_with_fingerprinting(
            training_df=training_df,
            testing_df=testing_df,
            specific_measurements=None,
            access_point_names=access_point_names,
            room_id_to_name=room_id_to_name,
            training_batch_size=training_batch_size,
            testing_batch_size=testing_batch_size,
        )


def run_fingerprinting_for_coordinates():
    # TODO: Do I need room names? Here and above
    # TODO: I could merge these as well, if needed
    """ University """
    """training_df = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/grid/university/training.csv")
    testing_df = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/grid/university/testing.csv")
    room_id_to_name = c.ROOM_ID_TO_NAME_UNIVERSITY
    experiments = [
        [
            c.ROUTER_UNIVERSITY_3,
            c.ROUTER_UNIVERSITY_14_3,
            c.ROUTER_UNIVERSITY_16_7,
        ],
        [
            c.ROUTER_UNIVERSITY_3,
            c.ROUTER_UNIVERSITY_14_3,
            c.ROUTER_UNIVERSITY_16_7,
            c.ROUTER_UNIVERSITY_18_1,
            c.ROUTER_UNIVERSITY_301,
            c.ROUTER_UNIVERSITY_303,
            c.ROUTER_UNIVERSITY_304,
            c.ROUTER_UNIVERSITY_305,
            c.ROUTER_UNIVERSITY_345_18
        ],
        c.ROUTERS_UNIVERSITY,
    ]
    specific_measurements_one_each_room = [
        (1, 4),
        (2, 4),
        (3, 4),
        (4, 4),
        (5, 4),
        (6, 4),
        (14, 3),
        (16, 5),
        (18, 1),
        (301, 4),
        (302, 6),
        (303, 9),
        (304, 3),
        (305, 6),
        (345, 20),
        (347, 3),
    ]
    specific_measurements_four_each_room = [
        (1, 1),
        (1, 3),
        (1, 4),
        (1, 6),
        (2, 1),
        (2, 3),
        (2, 5),
        (2, 8),
        (3, 1),
        (3, 4),
        (3, 5),
        (3, 7),
        (4, 1),
        (4, 3),
        (4, 5),
        (4, 7),
        (5, 1),
        (5, 5),
        (5, 6),
        (5, 8),
        (6, 1),
        (6, 3),
        (6, 4),
        (6, 6),
        (14, 1),
        (14, 3),
        (14, 19),
        (14, 21),
        (16, 1),
        (16, 7),
        (16, 15),
        (16, 21),
        (18, 1),
        (18, 3),
        (18, 13),
        (18, 15),
        (301, 1),
        (301, 2),
        (301, 3),
        (301, 4),
        (302, 1),
        (302, 2),
        (302, 5),
        (302, 6),
        (303, 1),
        (303, 3),
        (303, 7),
        (303, 9),
        (304, 1),
        (304, 3),
        (304, 7),
        (304, 9),
        (305, 1),
        (305, 2),
        (305, 5),
        (305, 6),
        (345, 1),
        (345, 8),
        (345, 17),
        (345, 24),
        (347, 1),
        (347, 2),
        (347, 3),
    ]
    training_batch_size = 30
    testing_batch_size = 1"""

    """ House """
    """training_df = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/grid/house/training.csv")
    testing_df = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/grid/house/testing.csv")
    room_id_to_name = c.ROOM_ID_TO_NAME_HOUSE
    experiments = [
        [c.ROUTER_HOUSE],
        [c.ROUTER_HOUSE, c.IPHONE],
        [c.ROUTER_HOUSE, c.IPHONE, c.ATOM],
        [c.ROUTER_HOUSE, c.IPHONE, c.ATOM, c.STICK],
    ]
    specific_measurements_one_each_room = [
        (0, 6),
        (1, 5),
        (2, 4),
        (3, 25),
        (4, 12),
        (5, 4),
        (6, 8),
        (7, 1),
        (8, 1),
        (9, 8),
        (10, 14),
        (11, 6),
        (12, 6),
        (13, 3),
        (14, 1),
        (15, 1),
        (16, 2),
    ]
    specific_measurements_four_each_room = [
        (0, 1),
        (0, 11),
        (0, 24),
        (0, 39),
        (1, 1),
        (1, 9),
        (1, 19),
        (1, 27),
        (2, 1),
        (2, 2),
        (2, 3),
        (2, 4),
        (3, 1),
        (3, 6),
        (3, 25),
        (3, 30),
        (4, 1),
        (4, 3),
        (4, 22),
        (4, 24),
        (5, 1),
        (5, 2),
        (5, 3),
        (5, 4),
        (6, 1),
        (6, 5),
        (6, 11),
        (6, 14),
        (7, 1),
        (7, 3),
        (7, 7),
        (7, 9),
        (8, 1),
        (8, 2),
        (8, 3),
        (9, 1),
        (9, 2),
        (9, 9),
        (9, 10),
        (10, 1),
        (10, 6),
        (10, 13),
        (10, 22),
        (11, 1),
        (11, 3),
        (11, 4),
        (11, 6),
        (12, 1),
        (12, 3),
        (12, 13),
        (12, 15),
        (13, 1),
        (13, 2),
        (13, 5),
        (13, 6),
        (14, 1),
        (14, 4),
        (14, 13),
        (14, 16),
        (15, 1),
        (15, 2),
        (15, 3),
        (16, 1),
        (16, 2),
        (16, 3),
        (16, 4),
    ]
    # TODO: Experients??
    training_batch_size = 25
    testing_batch_size = 1"""

    """ Apartment """
    training_df = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/grid/apartment/training.csv")
    # testing_df = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/grid/apartment/testing_1h.csv")
    testing_df = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/grid/apartment/testing_1d.csv")
    # testing_df = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/grid/apartment/testing_1w.csv")

    room_id_to_name = c.ROOM_ID_TO_NAME_APARTMENT

    experiments = [
        [c.ROUTER_APARTMENT],
        [c.ROUTER_APARTMENT, c.STICK],
        [c.ROUTER_APARTMENT, c.STICK, c.IPHONE],
        [c.ROUTER_APARTMENT, c.STICK, c.IPHONE, c.ATOM],
        [c.ROUTER_APARTMENT, c.STICK, c.IPHONE, c.ATOM, c.XIAOMI],
    ]

    specific_measurements_one_each_room = [
        (0, 12),
        (1, 5),
        (2, 5),
        (3, 1)
    ]
    specific_measurements_four_each_room = [
        (0, 1),
        (0, 4),
        (0, 9),
        (0, 12),
        (1, 1),
        (1, 2),
        (1, 5),
        (1, 6),
        (2, 1),
        (2, 5),
        (2, 16),
        (2, 20),
        (3, 1),
        (3, 2),
        (3, 3),
        (3, 4)
    ]

    training_batch_size = 50
    testing_batch_size = 1

    for index, access_point_names in enumerate(experiments):
        print(f"Experiment {index}:")
        do_coordinates_predictions_with_fingerprinting(
            training_df=training_df,
            testing_df=testing_df,
            specific_measurements=None,
            access_point_names=access_point_names,
            room_id_to_name=room_id_to_name,
            training_batch_size=training_batch_size,
            testing_batch_size=testing_batch_size,
            coordinate_dimensions=2
        )


def run_trilateration_for_coordinates_and_rooms():
    signal_attenuation = 3.6

    """ University """
    """training_df = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/grid/university/training.csv")
    testing_df = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/grid/university/testing.csv")

    information_about_university_3_router = {
        "name": c.ROUTER_UNIVERSITY_3,
        "signal_attenuation": signal_attenuation,
        "location": {
            "x": 3195,
            "y": 1623
        },
        "reference": {
            "distance": 1952,
            "signal": -60
        }
    }
    information_about_university_14_3_router = {
        "name": c.ROUTER_UNIVERSITY_14_3,
        "signal_attenuation": signal_attenuation,
        "location": {
            "x": 623,
            "y": 1310
        },
        "reference": {
            "distance": 4523,
            "signal": -72
        }
    }
    information_about_university_14_21_router = {
        "name": c.ROUTER_UNIVERSITY_14_21,
        "signal_attenuation": signal_attenuation,
        "location": {
            "x": 660,
            "y": 188
        },
        "reference": {
            "distance": 4667,
            "signal": -81
        }
    }
    information_about_university_16_7_router = {
        "name": c.ROUTER_UNIVERSITY_16_7,
        "signal_attenuation": signal_attenuation,
        "location": {
            "x": 5325,
            "y": 1310
        },
        "reference": {
            "distance": 255,
            "signal": -64
        }
    }
    information_about_university_16_15_router = {
        "name": c.ROUTER_UNIVERSITY_16_15,
        "signal_attenuation": signal_attenuation,
        "location": {
            "x": 4011,
            "y": 709
        },
        "reference": {
            "distance": 1373,
            "signal": -51
        }
    }
    information_about_university_18_1_router = {
        "name": c.ROUTER_UNIVERSITY_18_1,
        "signal_attenuation": signal_attenuation,
        "location": {
            "x": 5982,
            "y": 1310
        },
        "reference": {
            "distance": 859,
            "signal": -64
        }
    }
    information_about_university_18_15_router = {
        "name": c.ROUTER_UNIVERSITY_18_15,
        "signal_attenuation": signal_attenuation,
        "location": {
            "x": 6426,
            "y": 314
        },
        "reference": {
            "distance": 1740,
            "signal": -65
        }
    }
    information_about_university_301_router = {
        "name": c.ROUTER_UNIVERSITY_301,
        "signal_attenuation": signal_attenuation,
        "location": {
            "x": 3930,
            "y": 1910
        },
        "reference": {
            "distance": 1283,
            "signal": -59
        }
    }
    information_about_university_303_router = {
        "name": c.ROUTER_UNIVERSITY_303,
        "signal_attenuation": signal_attenuation,
        "location": {
            "x": 4599,
            "y": 2249
        },
        "reference": {
            "distance": 935,
            "signal": -58
        }
    }
    information_about_university_304_router = {
        "name": c.ROUTER_UNIVERSITY_304,
        "signal_attenuation": signal_attenuation,
        "location": {
            "x": 5429,
            "y": 2304
        },
        "reference": {
            "distance": 865,
            "signal": -53
        }
    }
    information_about_university_305_router = {
        "name": c.ROUTER_UNIVERSITY_305,
        "signal_attenuation": signal_attenuation,
        "location": {
            "x": 5822,
            "y": 2894
        },
        "reference": {
            "distance": 1562,
            "signal": -70
        }
    }
    information_about_university_345_18_router = {
        "name": c.ROUTER_UNIVERSITY_345_18,
        "signal_attenuation": signal_attenuation,
        "location": {
            "x": 1326,
            "y": 1666
        },
        "reference": {
            "distance": 3820,
            "signal": -70
        }
    }
    information_about_university_345_24_router = {
        "name": c.ROUTER_UNIVERSITY_345_24,
        "signal_attenuation": signal_attenuation,
        "location": {
            "x": 2270,
            "y": 1666
        },
        "reference": {
            "distance": 2878,
            "signal": -67
        }
    }

    def university_coordinates_to_room_id(coordinates) -> int:
        x, y = coordinates
        if y <= 1353:  # 14, 16 or 18
            if x <= 3195:  # Way, way over the line
                return 14
            elif x <= 5349:  # right on the side
                return 16
            else:
                return 18
        elif y >= 1623:  # 1, 345, 347, 301, 302, 303, 304, 305 or 6
            if x <= 933:
                return 1
            elif x <= 2460:
                return 345
            elif x <= 2857:
                return 347
            elif x <= 3940:
                return 301
            elif x <= 4413:
                return 302
            elif x <= 5116:
                return 303
            else:  # 304, 305 or 6
                if y <= 2302:  # 304 or 6'
                    if x <= 5818:
                        return 304
                    else:
                        return 6
                else:  # 305 or 6''
                    if x <= 5822:
                        return 305
                    else:
                        return 6
        else:  # 2, 3, 4 or 5
            if x <= 1613:
                return 2
            elif x <= 3195:
                return 3
            elif x <= 4833:
                return 4
            else:
                return 5

    dimensions = 2

    testing_batch_size = 1

    coordinates_to_room_id_fun = university_coordinates_to_room_id

    experiments = [
        [
            information_about_university_3_router,
            information_about_university_14_3_router,
            information_about_university_14_21_router,
            information_about_university_16_7_router,
            information_about_university_16_15_router,
            information_about_university_18_1_router,
            information_about_university_18_15_router,
            information_about_university_301_router,
            information_about_university_303_router,
            information_about_university_304_router,
            information_about_university_305_router,
            information_about_university_345_18_router,
            information_about_university_345_24_router
        ]
    ]"""

    """ House """
    """training_df = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/grid/house/training.csv")  # Used kind of
    testing_df = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/grid/house/testing.csv")

    information_about_house_router = {
        "name": c.ROUTER_HOUSE,
        "signal_attenuation": signal_attenuation,
        "location": {
            "x": 746,
            "y": 849,
            "z": 0
        },
        "reference": {
            "distance": 407,
            "signal": -63,
        }
    }
    information_about_atom = {
        "name": c.ATOM,
        "signal_attenuation": signal_attenuation,
        "location": {
            "x": 220,
            "y": 795,
            "z": 101
        },
        "reference": {
            "distance": 523,
            "signal": -67,
        }
    }
    information_about_stick = {
        "name": c.STICK,
        "signal_attenuation": signal_attenuation,
        "location": {
            "x": 1156,
            "y": 259,
            "z": 115
        },
        "reference": {
            "distance": 565,
            "signal": -57,
        }
    }
    information_about_iphone = {
        "name": c.IPHONE,
        "signal_attenuation": signal_attenuation,
        "location": {
            "x": 1267,
            "y": 876,
            "z": 337
        },
        "reference": {
            "distance": 775,
            "signal": -67,
        }
    }

    def house_coordinates_to_room_id(coordinates) -> int:
        x, y, z = coordinates
        if z < 270:  # 1st floor
            if x <= 100 or x >= 1311 or y <= 100 or y >= 1310 or (x >= 716 and y <= 199) or (x <= 465 and y >= 946):
                return 0
            elif y >= 1046:
                return 1
            elif x <= 479:
                return 4
            elif y <= 551:  # 6, 7 or 8
                if x <= 984:  # 6 or 8
                    if y >= 333 or (x >= 589 and y >= 233):
                        return 6
                    else:
                        return 8
                else:
                    return 7
            else:  # 2, 3 or 5
                if x <= 709:
                    if y <= 786:
                        return 5
                    else:
                        return 2
                else:
                    return 3
        else:  # 2nd floor
            if x <= 478:  # 11 or 12
                if y <= 689:
                    return 12
                else:
                    return 11
            elif x <= 676:  # 9 or 15
                if y <= 567:
                    return 15
                else:
                    return 9
            elif x <= 888:  # 10', 13 or 16
                if y <= 394:
                    return 16
                elif y >= 695:
                    return 10
                else:
                    return 13
            else:  # 10'' or 14
                if y <= 596:
                    return 14
                else:
                    return 10

    dimensions = 3

    testing_batch_size = 1

    coordinates_to_room_id_fun = house_coordinates_to_room_id

    experiments = [
        [information_about_stick, information_about_iphone, information_about_house_router, information_about_atom],
    ]"""

    """ Apartment """
    training_df = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/grid/apartment/training.csv")
    # testing_df = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/grid/apartment/testing_1h.csv")
    testing_df = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/grid/apartment/testing_1d.csv")
    # testing_df = pd.read_csv("/home/ronaldsz/Repositories/wifi-localization/data/grid/apartment/testing_1w.csv")

    information_about_apartment_router = {
        "name": c.ROUTER_APARTMENT,
        "signal_attenuation": signal_attenuation,
        "location": {
            "x": 645,
            "y": 274
        },
        "reference": {
            "distance": 302,
            "signal": -57,
        }
    }
    information_about_atom = {
        "name": c.ATOM,
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
        "name": c.STICK,
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
        "name": c.IPHONE,
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
        "name": c.XIAOMI,
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

    testing_batch_size = 1

    def apartment_coordinates_to_room_id(coordinates):
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
                
    coordinates_to_room_id_fun = apartment_coordinates_to_room_id

    dimensions = 2

    experiments = [
        [information_about_stick, information_about_iphone, information_about_apartment_router],
        [information_about_stick, information_about_iphone, information_about_apartment_router, information_about_atom],
        [information_about_stick, information_about_iphone, information_about_apartment_router, information_about_atom, information_about_xiaomi],
    ]

    for index, information_about_known_access_points in enumerate(experiments):
        print(f"Experiment {index}:")
        do_coordinates_predictions_with_signal_strength_formulas(
            testing_df=testing_df,
            information_about_known_access_points=information_about_known_access_points,
            dimensions=dimensions,
            testing_batch_size=testing_batch_size,
            coordinates_to_room_id=coordinates_to_room_id_fun
        )


if __name__ == "__main__":  # If this file is run directly
    mode = 2

    if mode == 1:  # Fingerprinting (rooms)
        run_fingerprinting_for_rooms()
    elif mode == 2:  # Fingerprinting (coordinates)
        run_fingerprinting_for_coordinates()
    elif mode == 3:  # Signal strength (coordinates and rooms)
        run_trilateration_for_coordinates_and_rooms()
    elif mode == 4:  # Gather data
        # TODO: We could also make these into constants
        alerts_apartment = [c.STICK, "EE:6E:14:1B:7A:BF (RosaMaria \\xF0\\x9F\\x92\\x95)", c.ROUTER_APARTMENT[0], c.ROUTER_APARTMENT[1], c.ATOM, c.XIAOMI]
        # alerts_house = [STICK, IPHONE, ROUTER_HOUSE, ATOM]
        # alerts_university = []
        # alerts_random = [c.STICK]
        df = gather_data(
            interface=c.NETWORK_INTERFACE,
            include_measurement_index=True,
            include_room_index=True,
            coordinate_dimensions=0,
            batch_size=50,
            batch_time_difference=0.5,
            alert_presence_for_access_points=alerts_apartment
        )
        df.to_csv("grid-data.csv")
    elif mode == 5:  # Real time walking data
        walking_data_gatherer(
            interface="wlp0s20f3",
            how_many_seconds=30,
        )
    elif mode == 6:  # Long walking data
        long_data_gatherer(
            interface="wlp0s20f3",
            how_many_seconds=10,
            pause_seconds=1
        )
    elif mode == 7:  # Merge .csv files from data gathering
        # files = ["14_10-21.csv", "16_15-21.csv", "16_8-14.csv", "1.csv", "301.csv", "303.csv", "305.csv", "345_9-24.csv", "3.csv", "5.csv", "14_1-9.csv", "16_1-7.csv", "18.csv", "2.csv", "302.csv", "304.csv", "345_1-8.csv", "347.csv", "4.csv", "6.csv"]
        files = ["0.csv", "1.csv", "2.csv", "3.csv"]
        merge_csvs(files)
    elif mode == 8:
        from visualize import go_go_go
        go_go_go()
    elif mode == 9:  # sort csv
        file_path = "/home/ronaldsz/Repositories/wifi-localization/data (copy)/university_testing.csv"
        testing_df = pd.read_csv(file_path)
        # print(testing_df)
        df = testing_df.sort_values(["room_index", "measurement_index", "batch_index"])
        df.to_csv("university_testing.csv")
    elif mode == 10:  # Reorder columns
        file_path = "/home/ronaldsz/Repositories/wifi-localization/data/apartment_testing_1w.csv"
        df = pd.read_csv(file_path)
        df = reorder_columns(df, priority_columns=[c.ROUTER_APARTMENT[0], c.ROUTER_APARTMENT[1], c.IPHONE, c.XIAOMI, c.STICK, c.ATOM])
        # df = reorder_columns(df, priority_columns=[c.ROUTER_HOUSE, c.IPHONE, c.STICK, c.ATOM])
        # df = reorder_columns(df)
        df.to_csv("apartment_testing_1w.csv")
    elif mode == 11:  # Strongest APs and their names
        # Just router files
        file_path = "/home/ronaldsz/Repositories/wifi-localization/data/university_routers/345_24.csv"
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
    elif mode == 12:  # Strongest APs and their names (copy)
        # Big files
        file_path = "/home/ronaldsz/Repositories/wifi-localization/data/university_testing.csv"
        df = pd.read_csv(file_path)
        df = df[df["room_index"] == 301]
        df = df[df["measurement_index"] == 4]
        # print(df)
        # a = input("Pause! ")
        aps = {}
        for col in list(df.columns):
            signal_strength_float = df[col].mean()
            import math
            if math.isnan(signal_strength_float):
                signal_strength_float = -666
            signal_strength = round(signal_strength_float)
            aps[col] = signal_strength

        strongest_aps = sorted(aps.items(), key=lambda x: x[1], reverse=True)
        strongest_aps = dict(strongest_aps)

        for name, signal_strength in strongest_aps.items():
            if name not in ["batch_index", "Unnamed: 0", "room_index", "measurement_index"]:
                print(f"{name}: {signal_strength}")
    elif mode == 13:
        file_path = "/home/ronaldsz/Repositories/wifi-localization/data/house_training.csv"
        df = pd.read_csv(file_path)
        print(df)
        single_sub_measurement_df = df[df["batch_index"] == 1]
        print(single_sub_measurement_df)
        import matplotlib.pyplot as plt

        # ax1 = df.plot.scatter(x="x", y="y", c="DarkBlue")  # 2d

        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        # If I want I can use different shape
        ax1 = ax.scatter(df["x"], df["y"], df["z"])
        """
        - Router #3.7: x = 746; y = 849; z = 0.
        - M5 Atom #4.4: x = 220; y = 795; z = 101.
        - M5 Stick #7.8: x = 1156; y = 259; z = 115.
        - iPhone #10.12: x = 1267; y = 876; z = 337.
        """
        known_x = [746, 220, 1156, 1267]
        known_y = [849, 795, 259, 876]
        known_z = [0, 101, 115, 337]
        ax2 = ax.scatter(known_x, known_y, known_z)



        plt.show()
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
