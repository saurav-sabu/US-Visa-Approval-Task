from US_Visa_Approval.exception import USVisaException
from US_Visa_Approval.logger import logging

import sys
import yaml
import os

def read_yaml_file(file_path:str):
    try:
        with open(file_path,"rb") as file:
            return yaml.safe_load(file)
    
    except Exception as e:
        raise USVisaException(e,sys)
    

def write_yaml_file(file_path:str,content:object,replace:bool=False):
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)

        with open(file_path,"w") as file:
            yaml.dump(content,file)
    
    except Exception as e:
        raise USVisaException(e,sys)