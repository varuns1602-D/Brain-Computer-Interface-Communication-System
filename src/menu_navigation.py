import cv2

options = [
    "HELP",
    "WATER",
    "FOOD",
    "YES",
    "NO"
]

selected = 0

while True:

    frame = 255 * \
        __import__("numpy").ones((500, 800, 3), dtype="uint8")

    for i, option in enumerate(options):

        color = (0, 0, 255)

        if i == selected:
            color = (0, 255, 0)

        cv2.putText(
            frame,
            option,
            (100, 100 + i * 60),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            color,
            2
        )

    cv2.imshow("Communication Menu", frame)

    key = cv2.waitKey(0)

    if key == ord('b'):
        selected = (selected + 1) % len(options)

    elif key == ord('q'):
        break

cv2.destroyAllWindows()