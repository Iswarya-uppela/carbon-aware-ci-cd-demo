import requests
import sys
import os

# Get job type from workflow input
job_type = os.environ.get("JOB_TYPE", "flexible").lower()

# If urgent, skip checks and allow job
if job_type == "urgent":
    print("🚀 Job type = urgent → Skipping carbon intensity check. Running job immediately.")
    sys.exit(0)

# If flexible, check carbon intensity API
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

# Threshold for green
THRESHOLD = 200  

if actual < THRESHOLD:
    print("✅ Carbon intensity is low now → running job")
    sys.exit(0)
elif forecast < THRESHOLD:
    print("⏳ Forecast says greener energy soon → delaying job")
    sys.exit(1)
else:
    print("⚠️ High carbon intensity now and in forecast → delaying job")
    sys.exit(1)
