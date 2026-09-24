# ======================================
# AUTO DRIFT MONITORING PIPELINE
# ======================================

from drift.drift_detector import detect_drift, drift_detected
import subprocess

print("\n===== AUTO PIPELINE STARTED =====\n")

# Run drift detection
report = detect_drift()

# Check drift condition
if drift_detected(report):

    print("\nDrift detected -> Starting retraining pipeline...\n")

    # Run retraining script
    subprocess.run(["python", "pipeline/retrain.py"])

else:
    print("\nNo drift detected. Model is stable.")

print("\n===== AUTO PIPELINE FINISHED =====")