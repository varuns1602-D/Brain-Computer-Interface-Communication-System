import cv2
import mediapipe as mp
import math

LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True
)

cap = cv2.VideoCapture(0)

blink_count = 0
blink_detected = False

def distance(p1, p2):
    return math.sqrt(
        (p1[0] - p2[0])**2 +
        (p1[1] - p2[1])**2
    )

def calculate_ear(points):
    horizontal = distance(points[0], points[3])

    vertical1 = distance(points[1], points[5])
    vertical2 = distance(points[2], points[4])

    return (vertical1 + vertical2) / (2.0 * horizontal)

while True:

    success, frame = cap.read()

    if not success:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb)

    if results.multi_face_landmarks:

        face_landmarks = results.multi_face_landmarks[0]

        h, w, _ = frame.shape

        left_points = []
        right_points = []

        for idx in LEFT_EYE:

            landmark = face_landmarks.landmark[idx]

            x = int(landmark.x * w)
            y = int(landmark.y * h)

            left_points.append((x, y))

            cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

        for idx in RIGHT_EYE:

            landmark = face_landmarks.landmark[idx]

            x = int(landmark.x * w)
            y = int(landmark.y * h)

            right_points.append((x, y))

            cv2.circle(frame, (x, y), 3, (0, 255, 0), -1)

        left_ear = calculate_ear(left_points)
        right_ear = calculate_ear(right_points)

        avg_ear = (left_ear + right_ear) / 2

        cv2.putText(
            frame,
            f"EAR: {avg_ear:.2f}",
            (30, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

        if avg_ear < 0.20:

            if not blink_detected:
                blink_count += 1
                blink_detected = True

        else:
            blink_detected = False

        cv2.putText(
            frame,
            f"Blinks: {blink_count}",
            (30, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 0, 0),
            2
        )

    cv2.imshow("Blink Counter", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()