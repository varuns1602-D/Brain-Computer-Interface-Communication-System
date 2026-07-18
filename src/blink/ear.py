"""
EAR (Eye Aspect Ratio) Calculator
---------------------------------
This module calculates the Eye Aspect Ratio (EAR)
from six eye landmark points.
"""

import math


class EARCalculator:

    @staticmethod
    def distance(point1, point2):
        """
        Calculate Euclidean distance between two points.
        """

        return math.sqrt(
            (point1[0] - point2[0]) ** 2 +
            (point1[1] - point2[1]) ** 2
        )

    @staticmethod
    def calculate(points):
        """
        Calculate Eye Aspect Ratio (EAR).

        Parameters
        ----------
        points : list
            Six eye landmark points.

        Returns
        -------
        float
            EAR value.
        """

        horizontal = EARCalculator.distance(points[0], points[3])

        vertical1 = EARCalculator.distance(points[1], points[5])
        vertical2 = EARCalculator.distance(points[2], points[4])

        ear = (vertical1 + vertical2) / (2.0 * horizontal)

        return ear