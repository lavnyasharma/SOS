from .token import *
from ..models import PasswordChangeRequestModel

def PasswodToken():
    try:
        token = Token()
        while 1:
            if PasswordChangeRequestModel.objects.filter(token=token).exists():
                token  = Token()
            else:
                return token
    except Exception as e:
        print(e)
        raise Exception("something went wrong")