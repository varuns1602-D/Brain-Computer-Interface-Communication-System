import cv2
import time

from vision.face_mesh import FaceMeshDetector
from vision.eye_landmarks import EyeLandmarkExtractor
from blink.ear import EARCalculator
from blink.ear_calibration import EARCalibrator


# ==========================================
# SETTINGS
# ==========================================

OPEN_DURATION = 3.0
PREPARE_DURATION = 2.0
CLOSED_DURATION = 2.0


# ==========================================
# INITIALIZATION
# ==========================================

detector = FaceMeshDetector()
calibrator = EARCalibrator()

cap = cv2.VideoCapture(0)

phase = "OPEN"
phase_start_time = time.time()

calibration_complete = False
results_data = None


print("===== Live EAR Calibration =====")
print("Follow the instructions shown on the camera.")
print("Press Q to quit.")


# ==========================================
# MAIN LOOP
# ==========================================

while True:

    success, frame = cap.read()

    if not success:
        print("Failed to read camera.")
        break

    results = detector.process(frame)

    avg_ear = None

    if results.multi_face_landmarks:

        face_landmarks = results.multi_face_landmarks[0]

        height, width, _ = frame.shape

        # Extract eye landmarks
        left_eye, right_eye = EyeLandmarkExtractor.extract(
            face_landmarks,
            width,
            height
        )

        # Calculate EAR
        left_ear = EARCalculator.calculate(left_eye)
        right_ear = EARCalculator.calculate(right_eye)

        avg_ear = (left_ear + right_ear) / 2.0

        # Draw eye landmarks
        for point in left_eye:
            cv2.circle(
                frame,
                point,
                3,
                (0, 255, 0),
                -1
            )

        for point in right_eye:
            cv2.circle(
                frame,
                point,
                3,
                (0, 255, 0),
                -1
            )

        current_time = time.time()
        elapsed = current_time - phase_start_time

        # ==================================
        # PHASE 1: EYES OPEN
        # ==================================

        if phase == "OPEN":

            cv2.putText(
                frame,
                "KEEP YOUR EYES OPEN",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 255, 0),
                2
            )

            calibrator.add_open_sample(avg_ear)

            remaining = max(
                0,
                OPEN_DURATION - elapsed
            )

            cv2.putText(
                frame,
                f"Time: {remaining:.1f}",
                (30, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2
            )

            if elapsed >= OPEN_DURATION:

                phase = "PREPARE"

                phase_start_time = time.time()

        # ==================================
        # PHASE 2: PREPARE
        # ==================================

        elif phase == "PREPARE":

            cv2.putText(
                frame,
                "PREPARE TO CLOSE YOUR EYES",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2
            )

            remaining = max(
                0,
                PREPARE_DURATION - elapsed
            )

            cv2.putText(
                frame,
                f"Closing in: {remaining:.1f}",
                (30, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 255, 255),
                2
            )

            # IMPORTANT:
            # No samples are collected
            # during the preparation phase.

            if elapsed >= PREPARE_DURATION:

                phase = "CLOSED"

                phase_start_time = time.time()

        # ==================================
        # PHASE 3: EYES CLOSED
        # ==================================

        elif phase == "CLOSED":

            cv2.putText(
                frame,
                "KEEP YOUR EYES CLOSED",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 0, 255),
                2
            )

            calibrator.add_closed_sample(avg_ear)

            remaining = max(
                0,
                CLOSED_DURATION - elapsed
            )

            cv2.putText(
                frame,
                f"Time: {remaining:.1f}",
                (30, 100),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255, 255, 255),
                2
            )

            if elapsed >= CLOSED_DURATION:

                results_data = calibrator.get_results()

                calibration_complete = True

                phase = "COMPLETE"

                print()
                print("===== CALIBRATION COMPLETE =====")

                print(
                    "Open EAR:",
                    round(
                        results_data["open_ear"],
                        3
                    )
                )

                print(
                    "Closed EAR:",
                    round(
                        results_data["closed_ear"],
                        3
                    )
                )

                print(
                    "Threshold:",
                    round(
                        results_data["threshold"],
                        3
                    )
                )

        # ==================================
        # PHASE 4: COMPLETE
        # ==================================

        elif phase == "COMPLETE":

            cv2.putText(
                frame,
                "CALIBRATION COMPLETE",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 255, 0),
                2
            )

            if results_data:

                cv2.putText(
                    frame,
                    f"Open EAR: {results_data['open_ear']:.3f}",
                    (30, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2
                )

                cv2.putText(
                    frame,
                    f"Closed EAR: {results_data['closed_ear']:.3f}",
                    (30, 140),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2
                )

                cv2.putText(
                    frame,
                    f"Threshold: {results_data['threshold']:.3f}",
                    (30, 180),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 255),
                    2
                )

        # Show live EAR
        cv2.putText(
            frame,
            f"Live EAR: {avg_ear:.3f}",
            (30, 230),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 0, 0),
            2
        )

    else:

        cv2.putText(
            frame,
            "NO FACE DETECTED",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

    cv2.imshow(
        "Live EAR Calibration",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ==========================================
# CLEANUP
# ==========================================

cap.release()
detector.close()
cv2.destroyAllWindows()