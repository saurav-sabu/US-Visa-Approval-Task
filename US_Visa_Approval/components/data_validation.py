from US_Visa_Approval.exception import USVisaException
from US_Visa_Approval.logger import logging
from US_Visa_Approval.entity.artifact_entity import *
from US_Visa_Approval.entity.config_entity import *
from US_Visa_Approval.constant import *
from US_Visa_Approval.utils.main_utils import *

from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection

import pandas as pd
import json
import sys

class DataValidation:

    def __init__(self,data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise USVisaException(e,sys)
        

    def validate_number_of_columns(self,dataframe):
        try:
            status = len(dataframe.columns) == len(self._schema_config["columns"])
            logging.info(f"Number of required columns there: {status}")
            return status
        except Exception as e:
            raise USVisaException(e,sys)
        
    
    def is_column_exist(self,df):
        try:
            dataframe_columns = df.columns
            missing_numerical_columns = []
            missing_categorical_columns = []

            for column in self._schema_config["numerical_columns"]:
                if column not in dataframe_columns:
                    missing_numerical_columns.append(column)

            if len(missing_numerical_columns)>0:
                logging.info(f"Missing numerical columns: {missing_numerical_columns}")

            for column in self._schema_config["categorical_columns"]:
                if column not in dataframe_columns:
                    missing_categorical_columns.append(column)

            if len(missing_categorical_columns)>0:
                logging.info(f"Missing categorical columns: {missing_categorical_columns}")

            return False if len(missing_categorical_columns) > 0 or len(missing_numerical_columns)>0 else True
        
        except Exception as e:
            raise USVisaException(e,sys)
        

    @staticmethod
    def read_data(file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise USVisaException(e,sys)
        
    
    def detect_dataset_drift(self,reference_df,current_df):

        try:
            data_drift_profile = Profile(sections=[DataDriftProfileSection()])
            data_drift_profile.calculate(reference_df,current_df)

            report = data_drift_profile.json()
            json_report = json.loads(report)

            write_yaml_file(file_path=self.data_validation_config.drift_report_file_path,content=json_report)

            n_features = json_report["data_drift"]["data"]["metrics"]["n_features"]
            n_drifted_features = json_report["data_drift"]["data"]["metrics"]["n_drifted_features"]

            logging.info(f"{n_drifted_features}/{n_features} drift detected")

            drift_status = json_report["data_drift"]["data"]["metrics"]["dataset_drift"]
            return drift_status
        
        except Exception as e:
            raise USVisaException(e,sys)
        
    def initiate_data_validation(self) -> DataValidationArtifact:

        try:
            validation_error_msg = ""
            logging.info("Starting data validation")

            train_df, test_df = (DataValidation.read_data(file_path=self.data_ingestion_artifact.train_file_path),
                                 DataValidation.read_data(file_path=self.data_ingestion_artifact.test_file_path))
            
            status = self.validate_number_of_columns(train_df)
            logging.info(f"All required columns are present in training dataframe: {status}")

            if not status:
                validation_error_msg+=f"columns are missing in train dataframe"
            
            status = self.validate_number_of_columns(test_df)
            logging.info(f"All required columns are present in testing dataframe: {status}")
            if not status:
                validation_error_msg+=f"columns are missing in test dataframe"

            status = self.is_column_exist(train_df)
            if not status:
                validation_error_msg+=f"columns are missing in train dataframe"

            status = self.is_column_exist(test_df)
            if not status:
                validation_error_msg+=f"columns are missing in test dataframe"

            validation_status = len(validation_error_msg) == 0

            if validation_status:
                drift_status = self.detect_dataset_drift(train_df,test_df)
                if drift_status:
                    logging.info("Drift detected")
                    validation_error_msg = "Drift detected"
                else:
                    validation_error_msg = "Drift not detected"

            else:
                logging.info(f"Validation error: {validation_error_msg}")


            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                message = validation_error_msg,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            logging.info(f"Data validation artifact {data_validation_artifact}")
            return data_validation_artifact
        
        except Exception as e:
            raise USVisaException(e,sys)

