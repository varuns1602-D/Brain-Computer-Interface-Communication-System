"""
EAR Calibration Module
----------------------
Calculates a personalized EAR threshold using
samples collected while the user's eyes are open
and closed.
"""


class EARCalibrator:

    def __init__(self):
        self.open_samples = []
        self.closed_samples = []

    def add_open_sample(self, ear):
        """Add an EAR measurement with eyes open."""
        self.open_samples.append(ear)

    def add_closed_sample(self, ear):
        """Add an EAR measurement with eyes closed."""
        self.closed_samples.append(ear)

    def calculate_threshold(self):
        """
        Calculate a personalized EAR threshold.

        Returns
        -------
        float
            EAR threshold between average open
            and closed eye EAR values.
        """

        if not self.open_samples or not self.closed_samples:
            raise ValueError(
                "Calibration requires both open-eye and closed-eye samples."
            )

        average_open = sum(self.open_samples) / len(self.open_samples)

        average_closed = (
            sum(self.closed_samples) / len(self.closed_samples)
        )

        threshold = (average_open + average_closed) / 2.0

        return threshold

    def get_results(self):
        """Return calibration statistics."""

        if not self.open_samples or not self.closed_samples:
            raise ValueError(
                "Calibration requires both open-eye and closed-eye samples."
            )

        average_open = sum(self.open_samples) / len(self.open_samples)

        average_closed = (
            sum(self.closed_samples) / len(self.closed_samples)
        )

        threshold = (average_open + average_closed) / 2.0

        return {
            "open_ear": average_open,
            "closed_ear": average_closed,
            "threshold": threshold
        }

    def reset(self):
        """Clear all calibration samples."""

        self.open_samples.clear()
        self.closed_samples.clear()