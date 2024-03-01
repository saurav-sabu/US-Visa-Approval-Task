import sys

from US_Visa_Approval.entity.config_entity import DataIngestionConfig
from US_Visa_Approval.entity.artifact_entity import DataIngestionArtifact
from US_Visa_Approval.components.data_ingestion import DataIngestion

from US_Visa_Approval.logger import logging
from US_Visa_Approval.exception import USVisaException


class TrainPipeline:

    def __init__(self) -> None:
        self.data_ingestion_config = DataIngestionConfig()


    def start_data_ingestion(self) -> DataIngestionArtifact:

        try:
            logging.info("start_data_ingestion method started")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

            logging.info("Got train and test data")

            return data_ingestion_artifact

        except Exception as e:
            raise USVisaException(e,sys) 
        
    
    def run_pipeline(self):

        try:
            data_ingestion_artifact = self.start_data_ingestion()

        except Exception as e:
            raise USVisaException(e,sys)


