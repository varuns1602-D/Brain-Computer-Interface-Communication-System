import cv2

from vision.face_mesh import FaceMeshDetector
from vision.eye_landmarks import EyeLandmarkExtractor
from blink.ear import EARCalculator


# Initialize Face Mesh
detector = FaceMeshDetector()

# Open webcam
cap = cv2.VideoCapture(0)

print("===== Live EAR Test =====")
print("Press Q to quit")


while True:

    success, frame = cap.read()

    if not success:
        print("Failed to read camera.")
        break

    # Detect face landmarks
    results = detector.process(frame)

    if results.multi_face_landmarks:

        face_landmarks = results.multi_face_landmarks[0]

        height, width, _ = frame.shape

        # Extract both eye landmarks
        left_eye, right_eye = EyeLandmarkExtractor.extract(
            face_landmarks,
            width,
            height
        )

        # Calculate EAR for both eyes
        left_ear = EARCalculator.calculate(left_eye)
        right_ear = EARCalculator.calculate(right_eye)

        # Calculate average EAR
        avg_ear = (left_ear + right_ear) / 2.0

        # Draw left-eye landmarks
        for point in left_eye:
            cv2.circle(
                frame,
                point,
                3,
                (0, 255, 0),
                -1
            )

        # Draw right-eye landmarks
        for point in right_eye:
            cv2.circle(
                frame,
                point,
                3,
                (0, 255, 0),
                -1
            )

        # Display EAR values
        cv2.putText(
            frame,
            f"Left EAR: {left_ear:.3f}",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Right EAR: {right_ear:.3f}",
            (30, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Average EAR: {avg_ear:.3f}",
            (30, 130),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
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
        "Live EAR Test",
        frame
    )

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
detector.close()
cv2.destroyAllWindows()