import requests
import os

PREDICTION_KEY = "b60f54b23d6042efb7d3e79ce17d9803"
ENDPOINT = "https://eastus.api.cognitive.microsoft.com/"
PROJECT_ID = "2fc5fc86-ff7b-491e-80c4-96502f9c5aa8"
ITERATION_ID = "b9e47635-e263-4b6a-a2f8-aaf4d4b385a7"  
HEADERS = {
    "Prediction-Key": PREDICTION_KEY,
    "Content-Type": "application/json"
}

def detect_occupancy_from_image_url(image_url):
    api_url = (
        f"{ENDPOINT}customvision/v3.0/Prediction/{PROJECT_ID}/classify/iterations/{ITERATION_ID}/url"
    )

    body = {"Url": image_url}
    try:
        response = requests.post(api_url, headers=HEADERS, json=body)
        response.raise_for_status()
        predictions = response.json().get("predictions", [])
        
        # Return the most likely tag
        best = max(predictions, key=lambda x: x["probability"])
        tag = best["tagName"]
        confidence = best["probability"]

        return {
            "tag": tag,
            "confidence": confidence,
            "occupied": tag in ["medium", "full"]  # Customize your logic
        }

    except Exception as e:
        print("[ERROR] Azure prediction failed:", e)
        return {"error": str(e), "occupied": True}
