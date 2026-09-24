import pandas as pd
from datetime import datetime

# Controlled carbon-intensity scenarios
scenarios = [
    {
        "scenario": "Observed Low-Carbon Condition",
        "grid_carbon_intensity": 618,
        "threshold": 700
    },
    {
        "scenario": "Controlled High-Carbon Condition",
        "grid_carbon_intensity": 800,
        "threshold": 700
    }
]

results = []

for s in scenarios:
    carbon = s["grid_carbon_intensity"]
    threshold = s["threshold"]

    decision = "DELAY" if carbon > threshold else "PROCEED"
    training_executed = "No" if decision == "DELAY" else "Yes"

    results.append({
        "timestamp": datetime.now().isoformat(),
        "scenario": s["scenario"],
        "grid_carbon_intensity": carbon,
        "threshold": threshold,
        "decision": decision,
        "training_executed": training_executed
    })

result_df = pd.DataFrame(results)

result_df.to_csv(
    "carbon_gate_controlled_experiment.csv",
    index=False
)

print("\n===== CARBON-AWARE CONTROLLED EXPERIMENT =====")
print(result_df.to_string(index=False))
print("\nSaved: carbon_gate_controlled_experiment.csv")
