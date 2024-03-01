from US_Visa_Approval.configuration.mongodb_connection import MongoDBClient
from US_Visa_Approval.constant import *
from US_Visa_Approval.exception import USVisaException

import pandas as pd
import sys
import numpy as np


class USVisaData:

    def __init__(self) -> None:
        
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise USVisaException(e,sys)
        
    
    def export_collection_as_dataframe(self,collection_name:str,database_name:str=None):

        try:
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))
            df = df.drop("_id",axis=1)

            return df
        
        except Exception as e:
            raise USVisaException(e,sys)


