import sys

from US_Visa_Approval.entity.config_entity import DataIngestionConfig,DataValidationConfig
from US_Visa_Approval.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from US_Visa_Approval.components.data_ingestion import DataIngestion
from US_Visa_Approval.components.data_validation import DataValidation

from US_Visa_Approval.logger import logging
from US_Visa_Approval.exception import USVisaException


class TrainPipeline:

    def __init__(self) -> None:
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()


    def start_data_ingestion(self) -> DataIngestionArtifact:

        try:
            logging.info("start_data_ingestion method started")
            data_ingestion = DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()

            logging.info("Got train and test data")

            return data_ingestion_artifact

        except Exception as e:
            raise USVisaException(e,sys) 
        

    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact) -> DataValidationArtifact:

        try:
            logging.info("start_data_validation method started")
            data_validation = DataValidation(data_ingestion_artifact=data_ingestion_artifact,data_validation_config=self.data_validation_config,)
            
            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("Performed the data validation")

            return data_validation_artifact

        except Exception as e:
            raise USVisaException(e,sys) 
        
    
    def run_pipeline(self):

        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)

        except Exception as e:
            raise USVisaException(e,sys)


