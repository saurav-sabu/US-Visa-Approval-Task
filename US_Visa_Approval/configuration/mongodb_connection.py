import os
import sys
import pymongo

from US_Visa_Approval.constant import *
from US_Visa_Approval.exception import USVisaException
from US_Visa_Approval.logger import logging

class MongoDBClient:

    client = None

    def __init__(self,database_name = DATABASE_NAME):
        
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGODB_URL_KEY)
                if mongo_db_url is None:
                    raise Exception(f"Environment Key: {MONGODB_URL_KEY} is not set")
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url)
            
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info("MongoDB connection successful")
        
        except Exception as e:
            raise USVisaException(e,sys)
                                