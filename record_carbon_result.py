import os
import pandas as pd
from datetime import datetime

carbon_df = pd.read_csv("carbon_emissions.csv")
gate_df = pd.read_csv("carbon_gate_log.csv")
latest_carbon = carbon_df.iloc[-1]
latest_gate = gate_df.iloc[-1]
result = pd.DataFrame([{"run_id": os.getenv("BUILD_NUMBER", "LOCAL"), "timestamp": datetime.now().isoformat(), "grid_carbon_intensity": latest_gate["grid_carbon_intensity"], "decision": latest_gate["decision"], "training_co2": latest_carbon["emissions"], "energy_consumed": latest_carbon["energy_consumed"], "training_duration": latest_carbon["duration"]}])
file = "carbon_aware_emissions.csv"
if os.path.exists(file): result.to_csv(file, mode="a", header=False, index=False)
else: result.to_csv(file, index=False)
print("===== CARBON EXPERIMENT RESULT =====")
print(result.to_string(index=False))
