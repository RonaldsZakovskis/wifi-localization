# The algorithm is based on:
#   X. Zhu and Y. Feng. RSSI-based Algorithm for Indoor Localization, 2013.
#   https://file.scirp.org/pdf/CN_2013071010352139.pdf
# Implementation is inspired from rssi package:
#   https://pypi.org/project/rssi/

from typing import Dict, List, Tuple, Union

import numpy as np


class SignalStrengthLocalizer(object):
    def __init__(self, access_points: List[Dict], dimensions: int = 2):
        """ Sets up the access points and dimensions, to have easier time
            predicting later.

        Args:
            access_points: Near earth reference distance, for example,
                400.
            dimensions: Number of dimensions to predict for. Must be an integer
                in [1, 2, 3], that is, 1 is for (x), 2 is for (x, y) and 3 is
                for (x, y, z).
        """
        self.access_points = access_points
        self.count = len(access_points)
        self.dimensions = dimensions

    @staticmethod
    def _get_distance_from_access_point(
        reference_distance: float,
        reference_signal: int,
        signal_attenuation: float,
        received_signal_strength: int
    ) -> float:
        """ Uses log model to compute an estimated distance from the access point.

        For all of the below -> (i = 1, 2, ..., n).
        This function is for a specific i.
        PL(dB) = PL(d0) - 10 * p * log10(di/d0)
        10 * p * log10(di/d0) = PL(d0) - PL(dB)
        log10(di/d0) = (PL(d0) - PL(dB)) / (10 * p)
        10^((PL(d0) - PL(dB)) / (10 * p)) = di / d0
        di = 10^((PL(d0) - PL(dB)) / (10 * p)) * d0

        Args:
            reference_distance: Near earth reference distance, for example,
                400.
            reference_signal: Signal Strength (RSSI) at reference_distance, for
                example, -69.
            signal_attenuation: Reduction of signal strength during
                transmission in the specific environment. For example, human
                body has value of 3, window or a brick wall has a value of 2,
                etc. For example, 2.
            received_signal_strength: Signal Strength (RSSI) just received from
                the specific access point, for example, -66.

        Returns:
            estimated_distance: Estimated distance to the specific access point.
        """
        signal_difference = reference_signal - received_signal_strength
        distance_coefficient = 10 ** (signal_difference / (10 * signal_attenuation))
        estimated_distance = distance_coefficient * reference_distance
        return estimated_distance

    def _set_distance_from_all_access_points(self, rssi_values) -> None:
        """ Updates the object instance's access points, to hold the current
            estimated distance from the access point.

        Args:
            rssi_values: List of signal strength (RSSI) values for the chosen
                access points.

        Returns:
            None.
        """
        for i in range(self.count):
            ap = self.access_points[i]
            distance_from_access_point = self._get_distance_from_access_point(
                reference_distance=ap["reference"]["distance"],
                reference_signal=ap["reference"]["signal"],
                signal_attenuation=ap["signal_attenuation"],
                received_signal_strength=rssi_values[i]
            )
            self.access_points[i]["distance"] = distance_from_access_point

    def _create_matrices(self) -> Tuple[np.ndarray, np.ndarray]:
        """ Creating A and B matrices as per paper.

        Args:
            None.

        Returns:
            a: A matrix with size (self.count - 1 , self.dimensions).
            b: B matrix with size (self.count - 1 , 1).
        """
        # n is the number of access points used for the localization
        n_minus_1 = self.count - 1
        # Create A matrix with n - 1 rows and a column for each dimension (for
        #   x and possibly also y and z)
        a = np.empty((n_minus_1, self.dimensions))
        # Create B matrix with n - 1 rows and 1 column
        b = np.empty((n_minus_1, 1))

        # Define d_n (distance from the last access point)
        d_n = self.access_points[n_minus_1]["distance"]

        # Define x_n (x coordinate from the last access point)
        x_n = self.access_points[n_minus_1]["location"]["x"]
        if self.dimensions >= 2:
            # Define y_n (y coordinate from the last access point)
            y_n = self.access_points[n_minus_1]["location"]["y"]
        if self.dimensions == 3:
            # Define z_n (z coordinate from the last access point)
            z_n = self.access_points[n_minus_1]["location"]["z"]

        # As per paper formulas, iterate only through first n - 1 access points
        for i in range(n_minus_1):
            ap = self.access_points[i]
            d = ap["distance"]
            if self.dimensions == 1:
                x = ap["location"]["x"]
                a[i] = [2 * (x - x_n)]
                b[i] = [(x ** 2) - (x_n ** 2) - (d ** 2) + (d_n ** 2)]
            elif self.dimensions == 2:
                x, y = ap["location"]["x"], ap["location"]["y"]
                a[i] = [2 * (x - x_n), 2 * (y - y_n)]
                b[i] = [(x ** 2) + (y ** 2) - (x_n ** 2) - (y_n ** 2) - (d ** 2) + (d_n ** 2)]
            else:  # self.dimensions == 3
                x, y, z = ap["location"]["x"], ap["location"]["y"], ap["location"]["z"]
                a[i] = [2 * (x - x_n), 2 * (y - y_n),  2 * (z - z_n)]
                b[i] = [(x ** 2) + (y ** 2) + (z ** 2) - (x_n ** 2) - (y_n ** 2) - (z_n ** 2) - (d ** 2) + (d_n ** 2)]
        return a, b

    def _compute_position_by_trilateration(
        self
    ) -> Union[Tuple[float], Tuple[float, float], Tuple[float, float, float]]:
        """ Uses trilateration algorithm to get the position from given RSSI
            values.

        This method calls _create_matrices() to, well... get the matrices. Then
            we can just calculate the answer: X=(A^T*A)^-1*A^T*B.

        Args:
            None.

        Returns:
            position: The predicted position, depending on the initialized
                amount of dimensions could be (x), (x, y) or (x, y, z).
        """
        a, b = self._create_matrices()
        # A^T
        at = np.transpose(a)
        # A^T*A
        at_a = np.matmul(at, a)
        # (A^T*A)^-1
        inv_at_a = np.linalg.inv(at_a)
        # A^T*B
        at_b = np.matmul(at, b)
        # X=(A^T*A)^-1*A^T*B
        x = np.matmul(inv_at_a, at_b)
        # Extract position
        position = tuple([float(i[0]) for i in tuple(x)])
        return position

    def get_position(
        self,
        rssi_values: List[int]
    ) -> Union[Tuple[float], Tuple[float, float], Tuple[float, float, float]]:
        """ Uses trilateration algorithm to get the position from given RSSI
            values.

        Args:
            rssi_values: List of signal strength (RSSI) values for the chosen
                access points.

        Returns:
            position: The predicted position, depending on the initialized
                amount of dimensions could be (x), (x, y) or (x, y, z).
        """
        self._set_distance_from_all_access_points(rssi_values)
        position = self._compute_position_by_trilateration()
        return position
