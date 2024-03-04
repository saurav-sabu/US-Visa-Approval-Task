from US_Visa_Approval.exception import USVisaException
from US_Visa_Approval.logger import logging

import sys
import yaml

def read_yaml_file(file_path:str):
    try:
        with open(file_path,"rb") as file:
            return yaml.safe.load(file)
    
    except Exception as e:
        raise USVisaException(e,sys)