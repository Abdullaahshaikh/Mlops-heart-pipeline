import os
import requests
import pandas as pd
from datetime import datetime

api_key = os.getenv("ELECTRICITY_MAPS_API_KEY")

if not api_key:
    raise Exception("ELECTRICITY_MAPS_API_KEY is not set")

response = requests.get(
    "https://api.electricitymaps.com/v3/carbon-intensity/latest?zone=IN",
    headers={"auth-token": api_key},
    timeout=15
)

data = response.json()
print("API Status:", response.status_code)

if response.status_code != 200:
    raise Exception(f"Electricity Maps API error: {data}")

carbon_intensity = data["carbonIntensity"]

decision = "DELAY" if carbon_intensity > 700 else "PROCEED"

timestamp = datetime.now().isoformat()

print(f"Grid carbon intensity: {carbon_intensity} gCO2eq/kWh")
print(f"DECISION: {decision}")

# Log only the carbon-gate decision.
gate_log = pd.DataFrame([{
    "timestamp": timestamp,
    "grid_carbon_intensity": carbon_intensity,
    "decision": decision
}])

file = "carbon_gate_log.csv"

if os.path.exists(file):
    gate_log.to_csv(file, mode="a", header=False, index=False)
else:
    gate_log.to_csv(file, index=False)

if decision == "DELAY":
    raise SystemExit(1)
