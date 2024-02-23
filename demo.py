from US_Visa_Approval.exception import USVisaException
import sys

try:
    a = 1/0
except Exception as e:
    raise USVisaException(e,sys)