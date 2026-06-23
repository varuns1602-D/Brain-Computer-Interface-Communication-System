import cv2
import mediapipe as mp

LEFT_IRIS = [474, 475, 476, 477]

mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True
)

cap = cv2.VideoCapture(0)

while True:

    success, frame = cap.read()

    if not success:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:

        face_landmarks = results.multi_face_landmarks[0]

        h, w, _ = frame.shape

        iris_points = []

        for idx in LEFT_IRIS:

            landmark = face_landmarks.landmark[idx]

            x = int(landmark.x * w)
            y = int(landmark.y * h)

            iris_points.append((x, y))

            cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

        iris_x = sum(p[0] for p in iris_points) / len(iris_points)

        if iris_x < w * 0.40:
            direction = "LEFT"

        elif iris_x > w * 0.60:
            direction = "RIGHT"

        else:
            direction = "CENTER"

        cv2.putText(
            frame,
            direction,
            (50, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    cv2.imshow("Gaze Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()