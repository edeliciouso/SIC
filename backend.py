from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from predictor import predict_image
from pathlib import Path
from PIL import Image
import shutil
import requests

UBIDOTS_TOKEN = "xxx"
UBIDOTS_DEVICE_LABEL = "xxx"
UBIDOTS_URL = f"https://industrial.api.ubidots.com/api/v1.6/devices/{UBIDOTS_DEVICE_LABEL}/"
HEADERS = {"X-Auth-Token": UBIDOTS_TOKEN, "Content-Type": "application/json"}

app = FastAPI()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
DETECTED_DIR = Path("detected")
DETECTED_DIR.mkdir(exist_ok=True)

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    temp_path = UPLOAD_DIR / file.filename
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Predict ingredient and confidence
    ingredient, confidence = predict_image(str(temp_path))
    detected_image_path = DETECTED_DIR / f"{ingredient}.png"

    # Save as PNG
    img = Image.open(temp_path)
    img.save(detected_image_path)

    # Send data to Ubidots
    payload = {
        "ingredient_str": {
        "value": 1,
        "context": {
            "name": ingredient
        }
    },
        "confidence": confidence
    }
    try:
        requests.post(UBIDOTS_URL, headers=HEADERS, json=payload)
    except Exception as e:
        print(f"Failed to send to Ubidots: {e}")

    return JSONResponse(content={"ingredient": ingredient, "confidence": confidence})
