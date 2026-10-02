import requests, json, asyncio
import edge_tts
from datetime import datetime
import matplotlib.pyplot as plt

url = "https://api.weather.gov/alerts/active?status=actual&message_type=alert&severity=Extreme,Severe"
headers = {"User-Agent": "WeatherEduBot (your-email@gmail.com)"}
r = requests.get(url, headers=headers, timeout=20)
data = r.json()

if not data['features']:
    print("No severe alerts - no video")
    exit(0)

alert = data['features'][0]['properties']
event = alert['event']
area = alert['areaDesc']
headline = alert['headline']
expires = alert.get('expires', '')
instruction = alert.get('instruction', 'Follow official guidance')

script = f"""National Weather Service has issued a {event} for {area}.
Headline: {headline}.
This alert is in effect until {expires}. If you are in {area}, take action now.
Safety steps: {instruction}. Avoid travel, stay indoors away from windows, and follow local officials.
This is educational coverage using NOAA public domain data with original analysis."""

meta = {
    "title": f"{event} for {area} - {datetime.now().strftime('%b %d, %Y')}",
    "description": f"{headline}\nArea: {area}\nExpires: {expires}\n\n{script}\n\nSource: weather.gov public domain.",
    "script": script
}
with open("meta.json", "w") as f:
    json.dump(meta, f)

plt.figure(figsize=(12,6))
plt.text(0.5, 0.5, f"{event}\n{area}\n{headline[:80]}", ha='center', va='center', fontsize=14)
plt.axis('off')
plt.savefig("map.jpg", bbox_inches='tight')
plt.close()

async def gen_voice():
    communicate = edge_tts.Communicate(script, "en-US-GuyNeural", rate="-5%")
    await communicate.save("audio.mp3")

asyncio.run(gen_voice())
print("Ready")
