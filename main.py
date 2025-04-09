from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

url = "https://routes.googleapis.com/directions/v2:computeRoutes"

headers = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": API_KEY,
    "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,"
}

body = {
    "origin": {
        "address": "570 Emerson Street, Coquitlam, BC"
    },
    "destination": {
        "address": "989 Richards Street, Vancouver, BC"
    },
    "travelMode": "DRIVE",
    "computeAlternativeRoutes": True,
}


response = requests.post(url, headers=headers, data=json.dumps(body))

if response.status_code == 200:
    data = response.json()
    for route in data.get("routes"):
        print("Route Duration:", route.get("duration"))
        print("Route Distance (meters):", route.get("distanceMeters"))
else:
    print("Error:", response.status_code, response.text)
