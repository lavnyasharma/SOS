import json
from doctors.utils.modelfunctions import doctorinsatnce, getDocId
from cv001.utils.utils import get_JWT_token, get_uid, retdate, rettime
from doctors.ser import HospitalSer, OfficeSer, SpecializationSer, doc_specializationSer, docser, usseSer
from user.utils.jwt import get_tokens_for_user
from cv001.utils.slugs import Gslug
from user.models import user
from user.utils.utils import is_user
from cv001.messages import *
from .models import *
from rest_framework.views import *
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import NotFound


class RegisterAsDoctorView(APIView):
    permission_classes = (AllowAny,)
    usermodel = user
    doctormodel = doctor

    def is_doctor(self, phone_number):
        instance = self.usermodel.objects.filter(
            phone_number=phone_number).first()
        return self.doctormodel.objects.filter(UID=instance.UID).exists()

    def getinsatnce(self, phone):
        instance = self.usermodel.objects.filter(phone_number=phone).first()
        return instance

    def post(self, request):
        try:
            data = request.data.get('otp')
            if data == request.session['otp_instance']:

                phone_number = request.session['phone_number_instance']
                if self.is_doctor(phone_number=phone_number):
                    response = {
                        'success': False,
                        'error': {
                            'message': USER_ALREADY_EXISTS,
                            'code': 409
                        }

                    }
                    return Response(response, status.HTTP_409_CONFLICT, exception=True)

                instance = self.getinsatnce(phone_number)

                if instance.is_doctor == True:
                    response = {
                        'success': True,
                        'data': {
                            'message': "Logged in",
                        }
                    }
                    del request.session['otp_instance']

                    token = get_tokens_for_user(instance)
                    response['data']['token'] = token
                    return Response(response, status.HTTP_200_OK)
                else:
                    response = {
                        'success': False,
                        'error': {
                            'message': 'access denied',
                            'code': 401
                        }
                    }
                    return Response(response, status.HTTP_401_UNAUTHORIZED, exception=True)
            response = {
                'success': False,
                'error': {
                    'message': OTP_INVALID,
                    'code': 409
                }

            }
            return Response(response, status.HTTP_409_CONFLICT, exception=True)
        except Exception as e:
            print(e)
            response = {
                'success': False,
                'error': {
                    'message': SOMTHING_WENT_WRONG,
                    'code': 500
                }
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)


class DoctorView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    doctormodel = doctor
    ser = docser
    usermodel = user

    def post(self, request):
        try:
            uid = get_uid(get_JWT_token(request=request))
            if self.doctormodel.objects.filter(UID=uid).exists():
                print('user')
                response = {
                    'success': True,
                    'data': {
                        'message': USER_ALREADY_EXISTS,
                        'code': 200
                    }
                }
                return Response(response, status.HTTP_200_OK)
            userInstance = self.usermodel.objects.filter(UID=uid).first()
            if userInstance.is_doctor == True:
                print('user is doctor')
                doctorinsatnce = self.doctormodel.objects.create(
                    UID=userInstance.UID,
                    registration_number=request.data.get(
                        'registration_number'),
                    professional_statement=request.data.get(
                        'professional_statement'),
                    practicing_from=retdate(
                        request.data.get('practicing_from')),
                    slug=Gslug(model=self.doctormodel,))
                response = {
                    'success': True,
                    'data': {
                        'message': "created successfully",
                    }
                }
                return Response(response, status.HTTP_201_CREATED)
            else:
                response = {
                    'success': False,
                    'error': {
                        'message': 'access denied',
                        'code': 401
                    }
                }
                return Response(response, status.HTTP_401_UNAUTHORIZED, exception=True)

        except Exception as e:
            print(e)
            response = {
                'success': False,
                'error': {
                    'message': str(e),
                    'code': 500
                }}
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):

        try:
            instance = self.doctormodel.objects.all()
            serinstance = self.ser(instance, many=True)
            response = {
                'success': True,
                'data': {
                    'message': SUCCESS,
                    "data": serinstance.data
                }
            }
            return Response(response, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = {
                'success': False,
                'error': {
                    'message': str(e),
                    'code': 500
                }
            }


class SpecializationView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    Specializationmodel = specialization
    ser = SpecializationSer

    def post(self, request):
        try:
            data = request.data.get("specialization")
            Specializationinstance = self.Specializationmodel.objects.create(
                name=data)
            Specializationinstance.save()
            response = {
                'success': True,
                'data': {
                    'message': SPECIALIZATION_ADDED,
                }
            }
            return Response(response, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = {
                'success': False,
                'error': {
                    'message': SOMTHING_WENT_WRONG,
                    'code': 500
                }
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            Specializationinstance = self.Specializationmodel.objects.all()
            serinstance = self.ser(Specializationinstance, many=True)
            response = {
                'success': True,
                'data': {
                    'message': SUCCESS,
                    'data': serinstance.data
                }
            }
            return Response(response, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = {
                'success': False,
                'error': {
                    'message': SOMTHING_WENT_WRONG,
                    'code': 500
                }
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)


class SpecializationInstanceView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    Specializationmodel = specialization
    ser = SpecializationSer

    def getinsatnce(self, id):
        instance = self.Specializationmodel.objects.filter(SPEID=id).first()
        if instance:
            print("hello")
            return instance
        else:
            raise NotFound(detail='specialization not found',
                           code=status.HTTP_404_NOT_FOUND)

    def get(self, request, speid):
        try:
            Specializationinstance = self.getinsatnce(speid)
            serinstance = self.ser(Specializationinstance)
            response = {
                'success': True,
                'data': {
                    'message': SUCCESS,
                    'data': serinstance.data
                }
            }
            return Response(response, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = {
                'success': False,
                'error': {
                    'message': str(e),
                    'code': 404
                }
            }

            return Response(response, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, speid):
        try:
            instance = self.getinsatnce(speid)
            instance.delete()
            response = {
                'success': True,
                'data': {
                    'message': SUCCESS,
                }
            }
            return Response(response, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = {
                'success': False,
                'error': {
                    'message': str(e),
                    'code': 404
                }
            }

            return Response(response, status=status.HTTP_404_NOT_FOUND)


class doc_specializationView(APIView):
    ser = doc_specializationSer
    model = doc_specialization
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def getinsatnce(self, id):
        instance = self.model.objects.filter(SPEID=id).all()
        if instance:
            return instance
        else:
            raise NotFound(detail='not found',
                           code=status.HTTP_404_NOT_FOUND)

    def post(self, request, speid):
        try:

            doc_instance_doci = getDocId(request=request)
            instance = self.model.objects.create(
                SPEID=speid, DOCID=doc_instance_doci)
            instance.save()
            response = {
                'success': True,
                'data': {
                    'message': SPECIALIZATION_ADDED,
                }
            }
            return Response(response, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = {
                'success': False,
                'error': {
                    'message': str(e),
                    'code': 404
                }
            }
            return Response(response, status.HTTP_404_NOT_FOUND)

    def get(self, request, speid):
        """
        for getting all doctors related to a specilazation
        """
        try:
            instance = self.getinsatnce(speid)
            serinstance = self.ser(instance, many=True)
            response = {
                'success': True,
                'data': {
                    'message': SUCCESS,
                    'data': serinstance.data
                }
            }
            return Response(response, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = {
                'success': False,
                'error': {
                    'message': str(e),
                    'code': 404
                }
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class HospitalView(APIView):
    model = hospital
    ser = HospitalSer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request):
        try:
            docid = getDocId(request=request)
            data = request.data
            enddata = ""
            cw = ""
            if data['end'] == None:
                enddata = None
                Cw = True
            else:
                enddata = retdate(data['end'])
                Cw = False
            instance = self.model.objects.create(
                DOCID=docid, name=data['name'], city=data['city'],
                start=retdate(data['start']), currently_working=Cw, end=enddata)
            instance.save()
            response = {
                'success': True,
                'data': {
                    'message': SUCCESS,
                }
            }
            return Response(response, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = {
                'success': False,
                'error': {
                    'message': str(e),
                    'code': 500
                }
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:

            instance = self.model.objects.all()
            serdata = self.ser(instance, many=True)
            response = {
                'success': True,
                'data': {
                    'message': SUCCESS,
                    'data': serdata.data
                }
            }
            return Response(response, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = {
                'success': False,
                'error': {
                    'message': str(e),
                    'code': 404
                }
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class OfficeView(APIView):
    model = office
    ser = OfficeSer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def post(self, request):
        try:
            docid = getDocId(request=request)
            data = request.data
            instance = self.model.objects.create(
                name=data['name'],
                DOCID=docid, min_time_slot=int(data['min']), first_consultation_fee=data['fee'],
                start=rettime(data['start']), end=rettime(data['end']), monday=data['mon'], tuesday=data['tue'], wednesday=data['wed'], thursday=data['thu'], friday=data['fri'], saturday=data['sat'], sunday=data['sun'])
            response = {
                'success': True,
                'data': {
                    'message': SUCCESS,
                }
            }
            return Response(response, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = {
                'success': False,
                'error': {
                    'message': str(e),
                    'code': 500
                }
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            instance = self.model.objects.all()
            serinstance = self.ser(instance, many=True)
            response = {
                'success': True,
                'data': {
                    'message': SUCCESS,
                    "data": serinstance.data
                }
            }
            return Response(response, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = {
                'success': False,
                'error': {
                    'message': str(e),
                    'code': 500
                }
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Issued :  Date and Time Management to be completed


class OfficeInstanceView(APIView):
    model = office
    ser = OfficeSer
    doc = doctor
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, id):
        try:
            doc = self.doc.objects.filter(slug=id).first()
            instance = self.model.objects.filter(DOCID=doc.DOCID).first()
            serinstance = self.ser(instance)
            response = {
                'success': True,
                'data': {
                    'message': SUCCESS,
                    'data': serinstance.data
                }
            }
            return Response(response, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = {
                'success': False,
                'error': {
                    'message': str(e),
                    'code': 404
                }
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            doc = self.doc.objects.filter(slug=id).first()
            instance = self.model.objects.filter(DOCID=doc.DOCID).first()
            instance.delete()
            response = {
                'success': True,
                'data': {
                    'message': SUCCESS,
                }
            }
            return Response(response, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = {
                'success': False,
                'error': {
                    'message': str(e),
                    'code': 404
                }
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class QualiView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    qualmodel = qualification
    usermodel = user

    def post(self, request):
        try:
            docid = getDocId(request=request)
            data = request.data
            instance = self.qualmodel.objects.create(
                DOCID=docid, name=data['name'], institute=data['institute'],
                year=retdate(data['prodate']), city=data['city'])
            response = {
                'success': True,
                'data': {
                    'message': SUCCESS,
                }
            }
            return Response(response, status.HTTP_200_OK)

        except Exception as e:
            print(e)
            response = {
                'success': False,
                'error': {
                    'message': SOMTHING_WENT_WRONG,
                    'code': 500
                }}
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)


class getAllDoctorData(APIView):
    permission_classes = (AllowAny,)
    model = doctor
    officemodel = office
    ser = docser
    userser = usseSer
    usermodel = user

    def post(self, request):
        try:
            SLUG = request.data["SLUG"]
            response = {
                'success': True,
                'data': {}
            }
            instance = self.model.objects.filter(slug=SLUG).first()
            docid = instance.DOCID
            uid = instance.UID
            userinstance = self.usermodel.objects.filter(UID=uid).first()
            officeinstance = self.officemodel.objects.filter(
                DOCID=docid).first()
            ofid = officeinstance.OFID
            serdata = self.ser(instance,)
            userserdata = self.userser(userinstance)
            response['data']['doctor'] = serdata.data
            response['data']['user'] = userserdata.data
            response['data']['ofid'] = ofid

            return Response(response, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = {
                'success': False,
                'error': {
                    'message': str(e),
                    'code': 404
                }
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
