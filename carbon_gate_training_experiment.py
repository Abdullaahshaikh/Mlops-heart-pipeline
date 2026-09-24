import os
import subprocess
import pandas as pd
from datetime import datetime

THRESHOLD = 700

# Controlled scenarios
scenarios = [
    {
        "scenario": "Observed Low-Carbon Condition",
        "grid_carbon_intensity": 618
    },
    {
        "scenario": "Controlled High-Carbon Condition",
        "grid_carbon_intensity": 800
    }
]

results = []

for s in scenarios:
    carbon = s["grid_carbon_intensity"]
    decision = "DELAY" if carbon > THRESHOLD else "PROCEED"

    print("\n========================================")
    print(s["scenario"])
    print(f"Grid carbon intensity: {carbon} gCO2eq/kWh")
    print(f"Threshold: {THRESHOLD} gCO2eq/kWh")
    print(f"Decision: {decision}")

    training_executed = "No"

    if decision == "PROCEED":
        print("Training allowed. Running train.py...")
        process = subprocess.run(
            ["python", "train.py"],
            capture_output=True,
            text=True
        )

        training_executed = "Yes"

        print(process.stdout)

        if process.returncode != 0:
            print(process.stderr)
            raise RuntimeError("Training failed.")

    else:
        print("Training BLOCKED because grid carbon intensity is above threshold.")

    results.append({
        "timestamp": datetime.now().isoformat(),
        "scenario": s["scenario"],
        "grid_carbon_intensity": carbon,
        "threshold": THRESHOLD,
        "decision": decision,
        "training_executed": training_executed
    })

df = pd.DataFrame(results)

df.to_csv(
    "carbon_gate_training_experiment.csv",
    index=False
)

print("\n========================================")
print("FINAL CONTROLLED EXPERIMENT")
print("========================================")
print(df.to_string(index=False))
print("\nSaved: carbon_gate_training_experiment.csv")
