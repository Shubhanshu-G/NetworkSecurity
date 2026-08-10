from pymongo import collection, database

from mongoDB_push_data import MONGO_DB_URL
from networksecurity.exception.exception import CustomException 
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
import os 
import sys
import numpy  as np 
import pandas as pd
import pymongo

from typing import List
from sklearn.model_selection import train_test_split

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL", MONGO_DB_URL)
class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig):
        try:
            logging.info(f"{'>>'*20} Data Ingestion {'<<'*20}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise CustomException(e, sys)

    def export_collection_as_dataframe(self):   ### Read data from mongo db
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]
            logging.info(f"Exporting collection: {collection_name} from database: {database_name}")

            df = pd.DataFrame(list(collection.find()))
            print("================================")
            print("Database:", database_name)
            print("Collection:", collection_name)
            print("Records:", len(df))
            print("================================")
            if "_id" in df.columns:
                df = df.drop(columns=["_id"], axis=1)

            df.replace({"na":np.nan}, inplace=True)
            logging.info(f"Exported {len(df)} records from collection: {collection_name}")

            return df
        except Exception as e:
            raise CustomException(e, sys)

    def export_data_to_feature_store(self, dataframe: pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            logging.info(f"Exported data to feature store at: {feature_store_file_path}")

            return dataframe

        except Exception as e:
            raise CustomException(e, sys)
            
    def iniitiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_to_feature_store(dataframe)
        except Exception as e:
            raise CustomException(e, sys)

    def split_data_as_train_test(self,dataframe: pd.DataFrame):
        try:
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Performed train test split on the dataframe")

            logging.info(
                "Exited split_data_as_train_test method of Data_Ingestion class"
            )
            
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            
            os.makedirs(dir_path, exist_ok=True)
            
            logging.info(f"Exporting train and test file path.")
            
            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False, header=True
            )

            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )
            logging.info(f"Exported train and test file path.")

            
        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_ingestion(self):
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_to_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            dataingestionartifact = DataIngestionArtifact(
                training_file_path=self.data_ingestion_config.training_file_path,
                testing_file_path=self.data_ingestion_config.testing_file_path
            )
            logging.info(f"Training CSV: {self.data_ingestion_config.training_file_path}")
            logging.info(f"Testing CSV: {self.data_ingestion_config.testing_file_path}")
            logging.info(f"Feature Store CSV: {self.data_ingestion_config.feature_store_file_path}")
            logging.info(f"Data ingestion completed successfully.")
            return dataingestionartifact
        except Exception as e:
            raise CustomException(e, sys)