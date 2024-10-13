from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import shutil
import os
from predict import predict
from classes import class_to_idx, calorie_map
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):

    if not os.path.exists("temp"):
        os.makedirs("temp")

    file_location = f"temp/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    class_name = predict(file_location, model_path="food_classifier2.pth", class_to_idx=class_to_idx)

    if class_name:
        calories = calorie_map.get(class_name, None)
        return JSONResponse(content={"İsmi: ": class_name, "Kalori": calories})

    return JSONResponse(content={"error": "Belirli bir sınıf bulunamadı."}, status_code=400)

# uvicorn main:app --reload
