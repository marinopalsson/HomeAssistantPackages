import requests
import json

url = "https://api.ust.is/aq/a/getStations"
response = requests.get(url)
data = json.loads(response.text)

markdown = "# Loftgæðastöðvar á Íslandi  \nhttps://loftgæði.is  \nhttps://api.ust.is/aq\n\n"

for station in data:
    if station["activity_end"] is None:
        name = station["name"]
        local_id = station["local_id"]
        latitude = station["latitude"]
        longitude = station["longitude"]
        pollutants = station["parameters"].strip('{}').split(',')

        pollutants_list = ', '.join(pollutants)

        markdown += f"## {name}  \n"
        markdown += f"Stöðvarnúmer: {local_id}  \n"
        markdown += f"Mengunarefni: {pollutants_list}  \n"
        markdown += f"Staðsetning: [Google Maps](https://maps.google.com/maps?q={latitude},{longitude})\n\n  "

with open("stodvar_listi.md", "w", encoding="utf-8") as file:
    file.write(markdown)

print("Markdown file created: air_quality_stations.md")
