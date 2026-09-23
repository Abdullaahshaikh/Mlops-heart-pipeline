import os
import requests
import pandas as pd
from datetime import datetime

df = pd.read_csv("carbon_emissions.csv")
latest_co2 = df.iloc[-1]["emissions"]

api_key = os.getenv("ELECTRICITY_MAPS_API_KEY")

response = requests.get(
    "https://api.electricitymaps.com/v3/carbon-intensity/latest?zone=IN",
    headers={"auth-token": api_key}
)

data = response.json()
print("API Status:", response.status_code)

if response.status_code != 200:
    raise Exception(f"Electricity Maps API error: {data}")

carbon_intensity = data["carbonIntensity"]

decision = "DELAY" if carbon_intensity > 700 else "PROCEED"

print(f"Latest training CO2: {latest_co2:.8e} kg")
print(f"Grid carbon intensity: {carbon_intensity} gCO2eq/kWh")
print(f"DECISION: {decision}")

log = pd.DataFrame([{
    "timestamp": datetime.now().isoformat(),
    "grid_carbon_intensity": carbon_intensity,
    "training_co2": latest_co2,
    "decision": decision
}])

log.to_csv("carbon_aware_emissions.csv", mode="a", header=False, index=False)

if decision == "DELAY":
    raise SystemExit(1)
