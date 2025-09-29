import requests
import sys
import os
from datetime import datetime

# Get job type from workflow input (default flexible if not provided)
job_type = os.environ.get("JOB_TYPE", "flexible").lower()

# HTML template for index.html
def write_html(message):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    with open("index.html", "w") as f:
        f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Carbon-Aware CI/CD Demo</title>
</head>
<body style="font-family: Arial; text-align: center; margin: 50px;">
  <h1>🌱 Carbon-Aware CI/CD Demo</h1>
  <p>{message}</p>
  <p><i>Deployed at {timestamp}</i></p>
</body>
</html>""")

# If urgent, skip checks and allow job
if job_type == "urgent":
    msg = "🚀 Job was marked <b>urgent</b> → Skipped carbon intensity check and deployed immediately."
    print(msg)
    write_html(msg)
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
    msg = "✅ Pipeline ran during <b>low carbon hours</b>! 🌱 The grid was green, so we deployed this page."
    print(msg)
    write_html(msg)
    sys.exit(0)
elif forecast < THRESHOLD:
    msg = "⏳ Forecast shows greener energy soon → Job delayed to reduce emissions."
    print(msg)
    sys.exit(1)
else:
    msg = "⚠️ High carbon intensity now and in forecast → Job delayed."
    print(msg)
    sys.exit(1)
