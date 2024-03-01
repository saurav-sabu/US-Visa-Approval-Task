from US_Visa_Approval.constant import *
from US_Visa_Approval.entity.config_entity import DataIngestionConfig
from US_Visa_Approval.entity.artifact_entity import DataIngestionArtifact

from US_Visa_Approval.logger import logging
from US_Visa_Approval.exception import USVisaException

from US_Visa_Approval.data_access.usvisa_data import USVisaData

import os
import sys
import pandas as pd

from sklearn.model_selection import train_test_split

class DataIngestion:

    def __init__(self,data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):

        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise USVisaException(e,sys)
        

    def export_data_into_feature_store(self):

        try:
            logging.info("Exporting the data from mongodb")
            usvisadata = USVisaData()

            dataframe = usvisadata.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)

            logging.info(f"Shape of dataframe: {dataframe.shape}")

            feature_store_file_path = self.data_ingestion_config.feature_store_file_path

            dir_path = os.path.dirname(feature_store_file_path)

            os.makedirs(dir_path,exist_ok=True)

            logging.info(f"Saving the exported data into feature store file path: {feature_store_file_path}")

            dataframe.to_csv(feature_store_file_path,index=False,header=True)

            return dataframe

        except Exception as e:
            raise USVisaException(e,sys)   


    def  split_data_to_train_test(self,dataframe):

        logging.info("Entered the function to train and split the data")

        try:
            logging.info("Perform train test split on dataframe")
            train_set, test_set = train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Process completed")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)

            logging.info(f"Export to train and test file path")

            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,header=True)

            logging.info(f"Process completed")

        except Exception as e:
            raise USVisaException(e,sys)
        
    
    def initiate_data_ingestion(self) -> DataIngestionArtifact:

        logging.info("Data Ingestion started")

        try:
            dataframe = self.export_data_into_feature_store()
            logging.info("Got the data from mongodb")

            self.split_data_to_train_test(dataframe)

            logging.info("Performed train and test split")

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=self.data_ingestion_config.training_file_path,
                                                            test_file_path=self.data_ingestion_config.testing_file_path)

            logging.info(f"Data Ingestion Artifact: {data_ingestion_artifact}")

            logging.info("Data Ingestion process completed")

            return data_ingestion_artifact

        except Exception as e:
            raise USVisaException(e,sys)  