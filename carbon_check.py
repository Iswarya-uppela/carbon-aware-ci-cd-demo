import requests
import sys
import os

# Detect trigger source
event = os.environ.get("GITHUB_EVENT_NAME", "push")
job_type = os.environ.get("JOB_TYPE", "flexible").lower()

if event == "push":
    print("📌 Triggered by auto push → Defaulting to 'flexible'")
else:
    print(f"📌 Triggered manually → Job type selected: {job_type}")

# Urgent jobs skip checks
if job_type == "urgent":
    print("🚀 Job type = urgent → Skipping carbon intensity check. Running job immediately.")
    sys.exit(0)

# Flexible jobs check carbon intensity API
url = "https://api.carbonintensity.org.uk/intensity"
resp = requests.get(url).json()
data = resp["data"][0]

forecast = data["intensity"]["forecast"]
actual = data["intensity"]["actual"]
index = data["intensity"]["index"]

print(f"🔎 Forecast: {forecast} gCO₂/kWh")
print(f"📊 Actual:   {actual} gCO₂/kWh")
print(f"🌍 Index:    {index}")
print(f"⚡ Job type: {job_type}")

# Threshold for "green energy"
THRESHOLD = 200  

if actual < THRESHOLD:
    print("✅ Carbon intensity is low now → running job")
    sys.exit(0)
elif forecast < THRESHOLD:
    print("⏳ Forecast shows lower intensity soon → delaying job")
    sys.exit(1)
else:
    print("⚠️ High carbon intensity now and in forecast → delaying job")
    sys.exit(1)
