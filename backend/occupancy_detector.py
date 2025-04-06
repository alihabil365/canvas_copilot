import os
import requests
from dotenv import load_dotenv

load_dotenv()

AZURE_KEY = os.getenv("AZURE_VISION_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_VISION_ENDPOINT")

def detect_occupancy_from_image_url(image_url):
    vision_url = f"{AZURE_ENDPOINT}/vision/v3.2/analyze?visualFeatures=Objects"

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_KEY,
        "Content-Type": "application/json"
    }

    body = { "url": image_url }

    response = requests.post(vision_url, headers=headers, json=body)
    if response.status_code != 200:
        print("Azure error:", response.text)
        return {"status": "error", "details": response.text}

    objects = response.json().get("objects", [])
    people = [obj for obj in objects if obj["object"].lower() == "person"]
    return {
        "people_detected": len(people),
        "occupied": len(people) > 0
    }
if __name__ == "__main__":
    test_image_url = "https://raw.githubusercontent.com/USFGDSC/Canvas-API-Data/main/Canvas%20API%20Dataset/LIB_medium.jpg"
    result = detect_occupancy_from_image_url(test_image_url)
    print(result)