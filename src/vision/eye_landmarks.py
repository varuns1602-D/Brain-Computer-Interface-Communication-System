"""
Eye Landmarks Module
--------------------
Extracts left and right eye landmark points
from MediaPipe Face Mesh landmarks.
"""


class EyeLandmarkExtractor:

    # Six landmarks used for EAR calculation
    LEFT_EYE = [33, 160, 158, 133, 153, 144]
    RIGHT_EYE = [362, 385, 387, 263, 373, 380]

    @staticmethod
    def _extract_points(face_landmarks, indices, frame_width, frame_height):
        """
        Convert normalized MediaPipe landmarks
        into pixel coordinates.
        """

        points = []

        for index in indices:

            landmark = face_landmarks.landmark[index]

            x = int(landmark.x * frame_width)
            y = int(landmark.y * frame_height)

            points.append((x, y))

        return points

    @classmethod
    def extract(cls, face_landmarks, frame_width, frame_height):
        """
        Extract left and right eye landmark points.

        Returns
        -------
        tuple
            (left_eye_points, right_eye_points)
        """

        left_eye = cls._extract_points(
            face_landmarks,
            cls.LEFT_EYE,
            frame_width,
            frame_height
        )

        right_eye = cls._extract_points(
            face_landmarks,
            cls.RIGHT_EYE,
            frame_width,
            frame_height
        )

        return left_eye, right_eye