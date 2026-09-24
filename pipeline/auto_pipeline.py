# ======================================
# AUTO DRIFT MONITORING PIPELINE
# ======================================

from drift.drift_detector import detect_drift, drift_detected
import subprocess

print("\n===== AUTO PIPELINE STARTED =====\n")

report = detect_drift()

if drift_detected(report):

    print("\nDrift detected -> Starting retraining...\n")

    subprocess.run(["python", "train.py"], check=True)

    print("\nRetraining completed successfully.")

else:
    print("\nNo drift detected. Model is stable.")

print("\n===== AUTO PIPELINE FINISHED =====")
