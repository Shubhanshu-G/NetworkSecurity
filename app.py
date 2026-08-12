import sys
import os
import certifi
import pymongo

from dotenv import load_dotenv

from networksecurity.constant import training_pipeline
from networksecurity.pipeline.training_pipeline import TrainingPipeline

from networksecurity.logging.logger import logging
from networksecurity.exception.exception import CustomException

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import Response
from starlette.responses import RedirectResponse

from uvicorn import run as app_run

import pandas as pd

from networksecurity.constant.training_pipeline import (
    DATA_INGESTION_DATABASE_NAME,
    DATA_INGESTION_COLLECTION_NAME
)


# ==========================================
# Environment Variables
# ==========================================

ca = certifi.where()

load_dotenv()

mongo_db_url = os.getenv("MONGO_DB_URL")


# ==========================================
# MongoDB Connection
# ==========================================

client = pymongo.MongoClient(
    mongo_db_url,
    tlsCAFile=ca
)

database = client[DATA_INGESTION_DATABASE_NAME]

collection = database[DATA_INGESTION_COLLECTION_NAME]


# ==========================================
# FastAPI Application
# ==========================================

app = FastAPI()


# ==========================================
# CORS Configuration
# ==========================================

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==========================================
# Home Route
# ==========================================

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")


# ==========================================
# Training Route
# ==========================================

@app.get("/train")
async def train_route():

    try:

        training_pipeline = TrainingPipeline()

        training_pipeline.run_pipeline()

        return Response("Training is successful")

    except Exception as e:

        raise CustomException(e, sys)



if __name__ == "__main__":

    app_run(
        app,
        host="localhost",
        port=8000
    )