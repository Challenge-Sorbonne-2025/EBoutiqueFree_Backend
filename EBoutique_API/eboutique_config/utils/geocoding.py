import requests
import os

def geocode_address(adresse):
    api_key = os.getenv("GOOGLE_MAPS_API_KEY")
    if not api_key:
        raise ValueError("Clé API Google Maps manquante")

    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": adresse, "key": api_key}
    response = requests.get(url, params=params)

    if response.status_code != 200:
        return None, None

    data = response.json()
    if data["status"] != "OK":
        return None, None

    location = data["results"][0]["geometry"]["location"]
    return location["lat"], location["lng"]
