from blink.ear_calibration import EARCalibrator


calibrator = EARCalibrator()


# Simulated open-eye EAR readings
open_values = [
    0.34,
    0.35,
    0.33,
    0.36,
    0.34
]


# Simulated closed-eye EAR readings
closed_values = [
    0.14,
    0.15,
    0.13,
    0.14,
    0.15
]


for value in open_values:
    calibrator.add_open_sample(value)


for value in closed_values:
    calibrator.add_closed_sample(value)


results = calibrator.get_results()


print("===== EAR Calibration Test =====")

print(
    "Average Open EAR:",
    round(results["open_ear"], 3)
)

print(
    "Average Closed EAR:",
    round(results["closed_ear"], 3)
)

print(
    "Calculated Threshold:",
    round(results["threshold"], 3)
)