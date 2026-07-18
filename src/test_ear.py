from blink.ear import EARCalculator

eye = [
    (0, 0),
    (2, 2),
    (4, 2),
    (6, 0),
    (4, -2),
    (2, -2)
]

ear = EARCalculator.calculate(eye)

print("EAR =", round(ear, 3))