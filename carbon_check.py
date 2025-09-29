import requests
import sys
import os

# Get job type from workflow input or default to "flexible"
job_type = os.environ.get("JOB_TYPE", "flexible").lower()

# 🚨 If urgent → always run
if job_type == "urgent":
    print("🚀 Job type = urgent → Skipping carbon intensity check. Running job immediately.")
    sys.exit(0)

# 🌱 If flexible → check UK Carbon Intensity API
url = "https://api.carbonintensity.org.uk/intensity"
try:
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    data = resp.json()["data"][0]
except Exception as e:
    print(f"❌ Failed to fetch carbon intensity data: {e}")
    # Fail safe: allow job to continue if API unavailable
    sys.exit(0)

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
