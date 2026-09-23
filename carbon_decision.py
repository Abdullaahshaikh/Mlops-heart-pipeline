import os
import requests
import pandas as pd

# ==========================================
# Carbon-Aware Decision Layer
# ==========================================

df = pd.read_csv("carbon_emissions.csv")

# Baseline CO2
baseline_co2 = df.head(10)["emissions"].mean()

# Latest training CO2
latest_co2 = df.iloc[-1]["emissions"]

# ==========================================
# Electricity Maps - India
# ==========================================

api_key = os.getenv("ELECTRICITY_MAPS_API_KEY")

response = requests.get(
    "https://api.electricitymaps.com/v3/carbon-intensity/latest?zone=IN",
    headers={"auth-token": api_key}
)

data = response.json()

# Debug / validation
print("API Status:", response.status_code)
print("API Response:", data)

if response.status_code != 200:
    raise Exception(f"Electricity Maps API error: {data}")

carbon_intensity = data["carbonIntensity"]

# ==========================================
# Results
# ==========================================

print(f"Baseline average CO2: {baseline_co2:.8e} kg")
print(f"Latest training CO2: {latest_co2:.8e} kg")
print(f"Grid carbon intensity: {carbon_intensity} gCO2eq/kWh")

# ==========================================
# Carbon-Aware Decision
# ==========================================

if carbon_intensity > 500:
    print(
        "DECISION: High grid carbon intensity - "
        "consider delaying training."
    )
else:
    print(
        "DECISION: Grid carbon intensity acceptable - "
        "training can proceed."
    )