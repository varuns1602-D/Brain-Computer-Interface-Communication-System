import cv2

from vision.face_mesh import FaceMeshDetector


detector = FaceMeshDetector()

cap = cv2.VideoCapture(0)

print("Face Mesh Test Started")
print("Press Q to quit")


while True:

    success, frame = cap.read()

    if not success:
        print("Failed to read camera.")
        break

    results = detector.process(frame)

    if results.multi_face_landmarks:
        cv2.putText(
            frame,
            "FACE DETECTED",
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

    cv2.imshow("Face Mesh Module Test", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


cap.release()
detector.close()
cv2.destroyAllWindows()