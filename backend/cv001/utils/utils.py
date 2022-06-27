from cv001.settings import SECRET_KEY
import jwt
import datetime


def get_uid(token):

    result = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return result['UID']


def get_JWT_token(request):
    return request.META['HTTP_AUTHORIZATION'].split('Bearer ')[1]


def retdate(data):
    y = int(data.split('-')[0])
    m = int(data.split('-')[1])
    if len(data.split('-')) == 3:
        d = int(data.split('-')[2])
    else:
        d = int('01')
    print(datetime.date(y, m, d))
    return datetime.datetime(y, m, d)

def rettime(data):
    h = int(data.split(':')[0])
    if len(data.split(':')) == 2:
        m = int(data.split(':')[1])
    else:
        m = int('00')
    if len(data.split(':')) == 3:
        s = int(data.split(':')[2])
    else:
        s = int('00')
    print(datetime.time(h, m, s))
    return datetime.time(h, m, s)
