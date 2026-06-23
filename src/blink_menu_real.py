import cv2
import mediapipe as mp
import math
import time
import numpy as np

# -------------------------
# MENU OPTIONS
# -------------------------
options = [
    "HELP",
    "WATER",
    "FOOD",
    "YES",
    "NO"
]

selected = 0

# -------------------------
# EYE LANDMARKS
# -------------------------
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

EAR_THRESHOLD = 0.20
REQUIRED_FRAMES = 2
COOLDOWN = 0.8

# -------------------------
# MEDIAPIPE
# -------------------------
mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True
)

cap = cv2.VideoCapture(0)

start_time = time.time()

blink_count = 0
closed_frames = 0
last_blink_time = 0


def distance(p1, p2):
    return math.sqrt(
        (p1[0] - p2[0]) ** 2 +
        (p1[1] - p2[1]) ** 2
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

    frame = cv2.flip(frame, 1)

    # Startup delay
    if time.time() - start_time < 2:

        cv2.putText(
            frame,
            "Initializing...",
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2
        )

        cv2.imshow("Eye Controlled Menu", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        continue

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

        for idx in RIGHT_EYE:

            landmark = face_landmarks.landmark[idx]

            x = int(landmark.x * w)
            y = int(landmark.y * h)

            right_points.append((x, y))

        left_ear = calculate_ear(left_points)
        right_ear = calculate_ear(right_points)

        avg_ear = (left_ear + right_ear) / 2

        current_time = time.time()

        if avg_ear < EAR_THRESHOLD:
            closed_frames += 1
        else:
            closed_frames = 0
        if (
            closed_frames >= REQUIRED_FRAMES and
            current_time - last_blink_time > COOLDOWN
):

            blink_count += 1
            selected = (selected + 1) % len(options)

            print("================================")
            print("BLINK DETECTED")
            print("Blink Count:", blink_count)
            print("Selected Index:", selected)
            print("================================")

    last_blink_time = current_time

    # MOVE MENU
    selected = (selected + 1) % len(options)

    print("Moved To:", options[selected])

    # -------------------------
    # DRAW MENU
    # -------------------------

    menu_x = 20
    menu_y = 120

    cv2.putText(
        frame,
        f"Blinks: {blink_count}",
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        "Blink = Next Option",
        (20, 85),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 255, 255),
        2
    )

    for i, option in enumerate(options):

        color = (0, 0, 255)

        if i == selected:
            color = (0, 255, 0)

        cv2.putText(
            frame,
            option,
            (menu_x, menu_y + i * 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            color,
            2
        )

    cv2.imshow("Eye Controlled Menu", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()