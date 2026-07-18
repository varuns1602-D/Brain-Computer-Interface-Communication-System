import cv2

from vision.face_mesh import FaceMeshDetector
from vision.eye_landmarks import EyeLandmarkExtractor


detector = FaceMeshDetector()

cap = cv2.VideoCapture(0)

print("Eye Landmarks Test Started")
print("Press Q to quit")


while True:

    success, frame = cap.read()

    if not success:
        print("Failed to read camera.")
        break

    results = detector.process(frame)

    if results.multi_face_landmarks:

        face_landmarks = results.multi_face_landmarks[0]

        height, width, _ = frame.shape

        left_eye, right_eye = EyeLandmarkExtractor.extract(
            face_landmarks,
            width,
            height
        )

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

        cv2.putText(
            frame,
            "EYES DETECTED",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    else:

        cv2.putText(
            frame,
            "NO FACE",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            2
        )

    cv2.imshow(
        "Eye Landmarks Test",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
detector.close()
cv2.destroyAllWindows()