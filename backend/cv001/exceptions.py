from rest_framework.exceptions import APIException
from rest_framework import status

class invalidinput(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = ('invalid input')
    default_code = '406'