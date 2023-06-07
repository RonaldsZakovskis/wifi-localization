import math

from signal_strength_based.signal_strength_localizer import SignalStrengthLocalizer

from sklearn.metrics import f1_score


def do_coordinates_predictions_with_signal_strength_formulas(information_about_known_access_points, coordinates_to_room_id, dimensions = 2, testing_df = None, testing_batch_size: int = None):
    signal_strength_localizer = SignalStrengthLocalizer(
        access_points=information_about_known_access_points,
        dimensions=dimensions
    )

    nan_value = -99  # TODO: Not sure what to do with this

    values = [0] * len(information_about_known_access_points)
    total_distance_error = 0.0
    correct = 0

    from helpers import get_batch_mean_df

    if testing_batch_size:
        testing_df = get_batch_mean_df(df=testing_df, batch_size=testing_batch_size)

    y_true = []
    y_pred = []

    for index, row in testing_df.iterrows():
        for ap_index, access_point_dict in enumerate(information_about_known_access_points):
            access_point = access_point_dict["name"]

            if isinstance(access_point, str):
                if not math.isnan(row[access_point]):
                    values[ap_index] = row[access_point]
            else:
                sub_values = [nan_value] * len(access_point)
                for sub_ap_index, name in enumerate(access_point):
                    if not math.isnan(row[name]):
                        sub_values[sub_ap_index] = row[name]
                values[ap_index] = max(sub_values)

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

        y_pred.append(predicted_room_id)
        y_true.append(actual_room_id)

    weighted_f1_score = f1_score(y_true=y_true, y_pred=y_pred, average="weighted") * 100
    print(f"Weighted F1 Score: {weighted_f1_score:.2f}%")

    error_in_distance = (total_distance_error / len(testing_df)) / 100
    print(f"Error in distance: {error_in_distance:.2f}")

    accuracy = (correct / len(testing_df)) * 100
    print(f"Final accuracy: {accuracy:.2f}%")
