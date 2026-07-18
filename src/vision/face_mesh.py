"""
Face Mesh Module
----------------
Handles MediaPipe Face Mesh initialization and
processes video frames to detect facial landmarks.
"""

import cv2
import mediapipe as mp


class FaceMeshDetector:
    """
    Detects facial landmarks using MediaPipe Face Mesh.
    """

    def __init__(
        self,
        max_num_faces=1,
        refine_landmarks=True,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ):
        self.mp_face_mesh = mp.solutions.face_mesh

        self.face_mesh = self.mp_face_mesh.FaceMesh(
            max_num_faces=max_num_faces,
            refine_landmarks=refine_landmarks,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )

    def process(self, frame):
        """
        Process an OpenCV BGR frame and return
        MediaPipe Face Mesh results.
        """

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        results = self.face_mesh.process(rgb_frame)

        return results

    def close(self):
        """
        Release MediaPipe Face Mesh resources.
        """

        self.face_mesh.close()