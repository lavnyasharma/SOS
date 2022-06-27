import base64
import uuid
from cv001.settings import SECRET_KEY
import datetime
import jwt
from rest_framework_simplejwt.tokens import RefreshToken
sec = SECRET_KEY.encode('ascii')
encoded_key = base64.b64encode(sec)


def get_tokens_for_user(user):

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def sos_jwt(pno):
    claims = {"UID": str(pno), "exp": datetime.datetime.utcnow(
    ) + datetime.timedelta(minutes=1000), "iat": datetime.datetime.utcnow(), 'jti': str(uuid.uuid1())}
    encoded = str(jwt.encode(claims, encoded_key, algorithm="HS256"))
    spi = encoded.split("'")
    return spi[1]


def sos_decode(token):
    try:
        dt = jwt.decode(token, encoded_key, algorithm="HS256")
        return dt['UID']
    except Exception as e:
        print(e)
        return False
