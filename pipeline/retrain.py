import sys
import os
import subprocess

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from drift.drift_detector import detect_drift, drift_detected

print("\n===== AUTO RETRAINING PIPELINE STARTED =====\n")

report = detect_drift()

if drift_detected(report):
    print("\nDrift detected -> Starting retraining...\n")
    subprocess.run(["python", "train.py"], check=True)
    print("\nRetraining completed successfully.")
else:
    print("\nNo drift detected. Model is stable.")

print("\n===== AUTO RETRAINING PIPELINE FINISHED =====")
