import sys
import os

import certifi
ca = certifi.where()

from dotenv import load_dotenv
load_dotenv()
mongo_db_url = os.getenv("MONGODB_URL_KEY")

import pymongo
from networksecurity.exception.exception import CustomException
from networksecurity.logging.logger import logging

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from uvicorn import run as app_run
from starlette.responses import RedirectResponse
import pandas as pd

from networksecurity.utils.main_utils.utils import load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel


client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)

from networksecurity.constant.training_pipeline import DATA_INGESTION_COLLECTION_NAME
from networksecurity.constant.training_pipeline import DATA_INGESTION_DATABASE_NAME

database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

# --------------------------------------------------------------------
# /train route — commented out for deployment.
# TrainingPipeline pulls in mlflow/dagshub (heavy deps not needed at
# serving time, and not present in the trimmed deployment
# requirements.txt), so leaving this uncommented on a size-limited
# platform (Vercel, etc.) will break the build/import.
#
# To train: uncomment this route AND add mlflow/dagshub back into
# requirements.txt, then run locally (or on a platform without a
# size cap). For normal deployment, keep it commented — /predict
# only needs the already-trained final_model/ artifacts.
# --------------------------------------------------------------------
# from networksecurity.pipeline.training_pipeline import TrainingPipeline
# from fastapi.responses import Response
#
# @app.get("/train")
# async def train_route():
#     try:
#         train_pipeline = TrainingPipeline()
#         train_pipeline.run_pipeline()
#         return Response("Training is successful")
#     except Exception as e:
#         raise CustomException(e, sys)

@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        preprocesor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")
        network_model = NetworkModel(preprocessor=preprocesor, model=final_model)
        y_pred = network_model.predict(df)
        df['predicted_column'] = y_pred
        df.to_csv('prediction_output/output.csv')
        table_html = df.to_html(classes='table table-striped')
        return templates.TemplateResponse(
            request=request,
            name="table.html",
            context={"request": request, "table": table_html}
        )
    except Exception as e:
        raise CustomException(e, sys)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app_run(app, host="0.0.0.0", port=port)