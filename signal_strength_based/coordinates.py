import math

from signal_strength_based.signal_strength_localizer import SignalStrengthLocalizer


def do_coordinates_predictions_with_signal_strength_formulas(information_about_known_access_points, coordinates_to_room_id, dimensions = 2, test_df = None):
    # TODO: Signal attenuation is from 2 to 6, depending on the environment,
    #   not really its even bigger i think the rang i mean

    signal_strength_localizer = SignalStrengthLocalizer(
        access_points=information_about_known_access_points,
        dimensions=dimensions
    )

    values = [0] * len(information_about_known_access_points)
    total_distance_error = 0.0
    correct = 0

    for index, row in test_df.iterrows():
        for ap_index, access_point_dict in enumerate(information_about_known_access_points):
            values[ap_index] = row[access_point_dict["name"]]  # This assumes that there are no NaNs
        actual_coordinates = [row[axis] for axis in ["x", "y", "z"][:dimensions]]

        # print(values)
        predicted_coordinates = list(signal_strength_localizer.get_position(values))
        # print(f"Actual coordinates: {actual_coordinates}")
        # print(f"Position (x, y) is {predicted_coordinates}")

        distance_error = math.dist(actual_coordinates, predicted_coordinates)

        # print(f"Distance error: {distance_error}")
        total_distance_error += distance_error

        actual_room_id = int(row['room_index'])
        predicted_room_id = coordinates_to_room_id(predicted_coordinates)
        # print(f"Actual room ID: {actual_room_id}")
        # print(f"Predicted room ID: {predicted_room_id}")
        # print("Correct" if actual_room_id == predicted_room_id else "False")
        if actual_room_id == predicted_room_id:
            correct += 1

    print(f"Error in distance: {total_distance_error / len(test_df)}")
    print(f"Rooom-level accuracy: {correct / len(test_df)}")

    """ Unused:
    for _ in range(10):
        # TODO: Get all known AP RSSI levels
        rssi_values = [-66, -49, -76]
        position = rssi_localizer.getNodePosition(rssi_values)
        print(f"Position (x, y) is ({position[0][0]:.2f}, {position[1][0]:.2f})")
        time.sleep(1)
    """
