from dotenv import load_dotenv
import os
import requests
import pandas as pd
import json

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

url = "https://routes.googleapis.com/directions/v2:computeRoutes"

headers = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": API_KEY,
    "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,"
}

df = pd.read_excel("locations.xlsx")

longest_distance = []
longest_duration = []

for index, row in df.iterrows():
    origin_address = row['start_address']
    destination_address = row['end_address']
    
    body = {
    "origin": {
        "address": origin_address
    },
    "destination": {
        "address": destination_address
    },
    "travelMode": "DRIVE",
    "computeAlternativeRoutes": True,
    }
    response = requests.post(url, headers=headers, data=json.dumps(body))

    if response.status_code == 200:
        data = response.json()
        # Get the routes with the longest distance
        routes = data.get("routes")
        longest_route = max(routes, key=lambda x: x["distanceMeters"])
        distance_km = longest_route["distanceMeters"] / 1000 * 1.1 + 1
        duration = longest_route["duration"]
        longest_distance.append(distance_km)
        longest_duration.append(duration)
    else:
        print("Error:", response.status_code, response.text)

df["distance_km"] = longest_distance
df["duration"] = longest_duration

df.to_excel("locations.xlsx", index=False)

    

