from cv001.utils.utils import get_JWT_token, get_uid
from doctors.models import doctor
from rest_framework.exceptions import NotFound

def getDocId(request):
    uid = get_uid(get_JWT_token(request=request))
    instance = doctor.objects.filter(UID=uid).first()
    if instance:
        return instance.DOCID
    else:
        raise NotFound(detail='n',
                       code=404)

     
def doctorinsatnce(uid):
    instance = doctor.objects.filter(UID=uid).first()
    if instance:
        return instance
    else:
        raise NotFound(detail='invalid request',
                       code=404)
