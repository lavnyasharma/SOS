from ast import Not
from asyncio.windows_events import NULL
from datetime import datetime
from http.client import NOT_FOUND
import json
from time import time
from user.utils.password import PasswodToken
from rest_framework_simplejwt.tokens import RefreshToken
from cv001.settings import FRONT_END_LINK
from datetime import timedelta
from user.utils.sms import sms_
from .utils.utils import is_user
from cv001.messages import *
from rest_framework.exceptions import NotFound
from .utils.modelFunctions import savephone, savepin, update_address
from django.utils import timezone
from cv001.utils.uid import decode_id, encode_id
from cv001.utils.utils import get_JWT_token, get_uid
from .models import Address, PasswordChangeRequestModel, PhoneNumber, Pincode, user, EmailToken, img, fmctoken
from .ser import AddressSer, PhoneSer, PincodeSer, UpdateSer, UserProfileSer
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .utils.otp import genrate_otp
from .utils.email import *
import re
from .utils.jwt import get_tokens_for_user
from django.db.models import Q
from django.contrib.auth import authenticate
from geopy.geocoders import Nominatim


class RegisterPhoneView(views.APIView):
    model = user
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            data = request.data.get('phone_number')
            if re.match(r'^(\+91[\-\s]?)?[0]?(91)?[78965432189]\d{9}$', data):
                if not is_user(data):
                    otp = genrate_otp()
                    request.session['otp'] = otp
                    request.session['phone_instance'] = data
                    print(otp)
                    # if sms_(message='concric: Your otp is &&OTP&&'.replace('&&OTP&&', otp), to='91'+data):
                    # send_email(
                    #     email='2020a1r067@mietjammu.in', request=request, message=otp)
                    if 1:

                        response = {
                            'success': True,
                            'data': {
                                'code': 200,
                                'phone_number': data,
                                'message': OTP_SENT,

                            }
                        }
                        return Response(response, status.HTTP_200_OK)
                    response = {
                        'success': False,
                        'error': {
                            'message': INVALID_PHONE_NUMBER,
                            'code': 400
                        }

                    }
                    return Response(response, status.HTTP_400_BAD_REQUEST, exception=True)

                response = {
                    'success': False,
                    'error': {
                        'message': USER_ALREADY_EXISTS,
                        'code': 409
                    }

                }
                return Response(response, status.HTTP_409_CONFLICT, exception=True)
            response = {
                'success': False,
                'error': {

                    'message': INVALID_PHONE_NUMBER,
                    'code': 400
                }

            }
            return Response(response, status.HTTP_400_BAD_REQUEST, exception=True)
        except Exception as e:
            response = {
                'success': False,
                'error': {
                    'message': str(e),
                    'code': 500
                }
            }
            print(e)
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR, exception=True)


class OtpView(views.APIView):
    """
    regestration otp verification happens here
    """

    permission_classes = (AllowAny,)
    model = user
    passwordModel = PasswordChangeRequestModel

    def post(self, request):

        try:
            print(request.session['otp'])
            otp = request.data.get('otp')
            number = request.session['phone_instance']
            if not is_user(number):
                if otp == request.session['otp']:
                    del request.session['otp']

                    ptoken = PasswodToken()
                    if self.passwordModel.objects.filter(UID=number).exists():
                        self.passwordModel.objects.filter(
                            UID=number).delete()
                    PasswordInstance = self.passwordModel.objects.create(
                        UID=number, password=number, token=ptoken)

                    response = {
                        'success': True,
                        'data': {
                            'message': OTP_CONF,
                            'set_token': PasswordInstance.token,
                        }
                    }
                    return Response(response, status.HTTP_201_CREATED)
                response = {
                    'success': False,
                    'error': {
                        'message': OTP_INVALID,
                        'code': 409
                    }

                }
                return Response(response, status.HTTP_409_CONFLICT, exception=True)

            response = {
                'success': False,
                'error': {
                    'message': USER_ALREADY_EXISTS,
                    'code': 409
                }

            }
            return Response(response, status.HTTP_409_CONFLICT, exception=True)
        except Exception as e:

            response = {
                'success': False,
                'error': {
                    'message': SOMTHING_WENT_WRONG,
                    'code': 500
                }
            }
            print(e)
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR, exception=True)


class UpdateData(views.APIView):
    """

    Update user data
    parameters

    - firstname as first_name
    - last name as last_name
    - password
    - email
    Note - on email update verification email is sent.

    """
    permission_classes = (AllowAny,)
    ser = UpdateSer
    model = user
    emailModel = EmailToken

    def patch(self, request):
        try:
            data = request.data
            instance_uid = get_uid(get_JWT_token(request=request))
            userinstance = self.model.objects.get(UID=instance_uid)
            response_data = {}
            if 'first_name' in data:
                userinstance.first_name = data['first_name']
                response_data['first_name'] = data['first_name']
            if 'last_name' in data:
                userinstance.last_name = data['last_name']
                response_data['last_name'] = data['last_name']
            if 'age' in data:
                userinstance.age = data['age']
                response_data['age'] = data['age']
            if 'gender' in data:
                userinstance.gender = data['gender']
                response_data['gender'] = data['gender']
            if 'pincode' in data:
                userinstance.pin = data['pincode']
                response_data['pincode'] = data['pincode']
            if 'address' in data:
                userinstance.address = data['address']
                response_data['address'] = data['address']
            if 'email' in data:

                try:
                    if data['email'] != userinstance.email:
                        if self.model.objects.filter(email=data['email']).exists():
                            raise Exception(
                                'an account already is already registred on this email')
                        token = email_token()
                        if self.emailModel.objects.filter(email=data['email']).exists():
                            self.emailModel.objects.filter(
                                email=data['email']).first().delete()
                        if self.emailModel.objects.filter(UID=userinstance.UID).exists():
                            self.emailModel.objects.filter(
                                UID=userinstance.UID).first().delete()
                        self.emailModel.objects.create(
                            UID=userinstance.UID, email=data['email'], Conf_token=token)
                        send_email(
                            email=data['email'], request=request, message=token)
                        response_data['email'] = {
                            'email': data['email'],
                            'success': True,
                            'info': 'verification link has been sent'
                        }
                        userinstance.email = data['email']
                        userinstance.email_stats(False)
                except Exception as e:
                    response_data['email'] = {
                        'email': str(e),
                        'success': False,
                        'code': 409

                    }
                    print(e)
            userinstance.save()
            response = {
                'success': True,
                'data': {
                    'message': UPDATED,
                    'data': response_data
                }
            }
            return Response(response, status.HTTP_200_OK)
        except:

            response = {
                'success': False,
                'error': {
                    'message': SOMTHING_WENT_WRONG,
                    'code': 500
                }
            }
           
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmailConfView(views.APIView):
    permission_classes = (AllowAny,)
    model = user
    token_model = EmailToken

    def is_expired(self, exp):
        if exp > timezone.localtime():
            return False
        return True

    def post(self, request):
        try:
            VERIFICATION_TOKEN = request.data.get('verification_token')

            if self.token_model.objects.filter(Conf_token=VERIFICATION_TOKEN).exists():
                EmailTokenInstance = self.token_model.objects.filter(
                    Conf_token=VERIFICATION_TOKEN).first()
                if not self.is_expired(EmailTokenInstance.expiration):
                    userinstance = self.model.objects.get(
                        UID=EmailTokenInstance.UID)
                    userinstance.email_stats(True)
                    userinstance.save()
                    EmailTokenInstance.delete()
                    response = {
                        'success': True,
                        'data': {
                            'message': EMAIL_CONFIRMED,
                        }
                    }
                    return Response(response, status.HTTP_202_ACCEPTED)
                else:
                    email = EmailTokenInstance.email
                    uid = EmailTokenInstance.UID
                    EmailTokenInstance.delete()
                    token = email_token()
                    EmailToken.objects.create(
                        UID=uid, email=email, Conf_token=token)
                    send_email(
                        email=email, request=request, message=token)
                    response = {
                        'success': False,
                        'error': {
                            'message': EMAIL_TOKEN_EXPIRED,
                            'code': 401,
                            'info': 'new verification token sent at &email&'.replace('&email&', '&&fxxxx@'.replace('&&f', email[:3])+email.split('@')[1]),
                            'email': '&&fxxxx'.replace('&&f', email[:3])+email.split('@')[1]

                        }
                    }
                return Response(response, status.HTTP_401_UNAUTHORIZED)

            else:
                response = {
                    'success': False,
                    'error': {
                        'message': TOKEN_NOT_FOUND,
                        'code': 404
                    }

                }
                return Response(response, status.HTTP_404_NOT_FOUND)

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


# Address views

class AddressView(views.APIView):
    permission_classes = (IsAuthenticated,)
    model = Address
    ser = AddressSer

    def save_addr(self, querry_data, uid):
        if 'phone' in querry_data:
            phone_instance = savephone(querry_data['phone'], uid).PHID
        else:
            phone_instance = None
        if 'pincode' in querry_data:
            pincode_instance = savepin(querry_data['pincode'], uid).PCID
        else:
            pincode_instance = None
        payload = decode_id(uid)
        aid = encode_id(
            p=payload['p'], t='ad', cd=str(timezone.localtime()))

        instance = self.model.objects.create(AID=aid,
                                             address_line_one=querry_data['addr1'], address_line_two=querry_data[
                                                 'addr2'], address_line_three=querry_data['addr3'],
                                             address_line_four=querry_data['addr4'], district=querry_data['district'],
                                             state=querry_data['state'], is_home=querry_data[
                                                 'is_home'], UID=uid, PHID=phone_instance, PCID=pincode_instance
                                             )
        instance.save()
        return instance

    def post(self, request):
        """
        save new user address instance
        """

        try:
            uid = get_uid(get_JWT_token(request=request))
            instance = self.save_addr(querry_data=request.data, uid=uid)
            instance_ser = self.ser(instance)

            response = {
                'success': True,
                'data': {
                    'message': ADDRESS_STORED,
                    'data': instance_ser.data
                }

            }
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = {
                'success': False,
                'error': {
                    'message': SOMTHING_WENT_WRONG,
                    'code': 500
                }

            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        """
        get all user address instance

        """
        try:
            uid = get_uid(get_JWT_token(request=request))
            instance = self.model.objects.filter(UID=uid)
            dataser = self.ser(instance, many=True)
            response = {
                'success': True,
                'data': {
                    'message': SUCCESS,
                    'data': dataser.data
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
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AddressInstance(views.APIView):
    model = Address
    ser = AddressSer

    def getinsatnce(self, id):
        instance = self.model.objects.filter(AID=id).first()
        if instance:
            return instance
        else:
            raise NotFound(detail='address not found',
                           code=status.HTTP_404_NOT_FOUND)

    def get(self, request, AIDINSTANCE):
        try:
            instance = self.getinsatnce(AIDINSTANCE)
            dataser = self.ser(instance,)
            response = {
                'success': True,
                'data': {
                    'message': SUCCESS,
                    'data': dataser.data
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

    def patch(self, request, AIDINSTANCE):
        try:
            instance = self.getinsatnce(AIDINSTANCE)
            instance = update_address(
                instance=instance, querry_data=request.data)
            dataser = self.ser(instance,)
            response = {
                'success': True,
                'data': {
                    'message': SUCCESS,
                    'data': dataser.data
                }
            }
            return Response(response, status.HTTP_200_OK)

        except Exception as e:
            response = {
                'success': False,
                'error': {
                    'message': str(e),
                    'code': 404
                }
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)


"""
phone no and pincode logics

"""


class PhoneNumberView(views.APIView):
    model = PhoneNumber
    ser = PhoneSer

    def get(self, request):
        try:
            uid = get_uid(get_JWT_token(request=request))
            instance = self.model.objects.filter(UID=uid)
            dataser = self.ser(instance, many=True)
            response = {
                'success': True,
                'data': {
                    'message': SUCCESS,
                    'data': dataser.data
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
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:

            uid = get_uid(get_JWT_token(request=request))
            phone_instance = savephone(request.data['phone'], uid).PHID
            response = {
                'success': True,
                'data': {
                    'message': SUCCESS,
                    'data': phone_instance
                }
            }
            return Response(response, status.HTTP_200_OK)
        except Exception as e:
            response = {
                'success': False,
                'error': {
                    'message': SOMTHING_WENT_WRONG,
                    'code': 500
                }
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)


class PincodeNumberView(views.APIView):
    model = Pincode
    ser = PincodeSer

    def get(self, request):
        try:
            uid = get_uid(get_JWT_token(request=request))
            instance = self.model.objects.filter(UID=uid)
            dataser = self.ser(instance, many=True)
            response = {
                'success': True,
                'data': {
                    'message': SUCCESS,
                    'data': dataser.data
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
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:

            uid = get_uid(get_JWT_token(request=request))
            pincode_instance = savepin(request.data['pincode'], uid).PCID
            response = {
                'success': True,
                'data': {
                    'message': SUCCESS,
                    'data': pincode_instance
                }
            }
            return Response(response, status.HTTP_200_OK)
        except Exception as e:
            response = {
                'success': False,
                'error': {
                    'message': SOMTHING_WENT_WRONG,
                    'code': 500
                }
            }
            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR)


class PhoneNumberInstanceView(views.APIView):
    model = PhoneNumber
    ser = PhoneSer

    def getinsatnce(self, id):
        instance = self.model.objects.filter(PHID=id).first()
        if instance:
            return instance
        else:
            raise NotFound(detail='phone number not found',
                           code=status.HTTP_404_NOT_FOUND)

    def get(self, request, PHIDINSTANCE):
        try:
            instance = self.getinsatnce(PHIDINSTANCE)
            dataser = self.ser(instance)
            response = {
                'success': True,
                'data': {
                    'message': SUCCESS,
                    'data': dataser.data
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

    def delete(self, request, PHIDINSTANCE):
        try:
            instance = self.getinsatnce(PHIDINSTANCE)
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


class PincodeNumberInstanceView(views.APIView):
    model = Pincode
    ser = PincodeSer

    def getinsatnce(self, id):
        instance = self.model.objects.filter(PCID=id).first()
        if instance:
            return instance
        else:
            raise NotFound(detail='pincode number not found',
                           code=status.HTTP_404_NOT_FOUND)

    def get(self, request, PCIDINSTANCE):
        try:
            instance = self.getinsatnce(PCIDINSTANCE)
            dataser = self.ser(instance)
            response = {
                'success': True,
                'data': {
                    'message': SUCCESS,
                    'data': dataser.data
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

    def delete(self, request, PCIDINSTANCE):
        try:
            instance = self.getinsatnce(PCIDINSTANCE)
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


"""
Verifying phone for an instance and genrating a JWT
"""


# class VerifyPhoneForInstanceView(views.APIView):
#     model = user

#     def get(self, request):
#         """
#         sends an otp to user
#         """
#         try:
#             uid = get_uid(get_JWT_token(request=request))
#             instance = self.model.objects.filter(UID=uid).first()
#             otp = genrate_otp()
#             request.session['otp'] = otp
#             print(otp)
#             response = {
#                 'success': True,
#                 'message': SUCCESS
#             }
#             return Response(response, status=status.HTTP_200_OK)
#         except Exception as e:
#             print(str(e))
#             response = {
#                 'success': False,
#                 'message': SOMTHING_WENT_WRONG
#             }
#             return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def post(self, request):
#         """
#         verifies otp from user and genrates a jwt verification token valid for 10 minutes
#         """
#         try:
#             uid = get_uid(get_JWT_token(request=request))
#             instance = self.model.objects.filter(UID=uid).first()
#             otp = request.data['otp']
#             if otp == request.session['otp']:
#                 del request.session['otp']
#                 verftoken = verification_jwt(instance)
#                 response = {
#                     'success': True,
#                     'message': SUCCESS,
#                     'data': {'token': verftoken}
#                 }
#                 return Response(response, status=status.HTTP_200_OK)
#             response = {
#                 'success': False,
#                 'message': OTP_INVALID

#             }
#             return Response(response, status=status.HTTP_409_CONFLICT)
#         except Exception as e:
#             print(str(e))
#             response = {
#                 'success': False,
#                 'message': SOMTHING_WENT_WRONG
#             }
#             return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class CheckInstanceTokenView(views.APIView):
#     model = user

#     def get(self, request):
#         try:
#             uid = get_uid(get_JWT_token(request=request))
#             instance = self.model.objects.filter(UID=uid).first()
#             data = request.data['verificationToken']
#             if verification_jwt_decode(token=data, userinstance=instance):
#                 response = {
#                     'success': True,
#                     'message': TOKEN_VALID
#                 }
#                 return Response(response, status=status.HTTP_202_ACCEPTED)
#             response = {
#                 'success': False,
#                 'message': TOKEN_INVALID
#             }
#             return Response(response, status=status.HTTP_401_UNAUTHORIZED)
#         except Exception as e:
#             print(e)
#             response = {
#                 'success': False,
#                 'message': SOMTHING_WENT_WRONG
#             }
#             return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class PasswordChangeView(views.APIView):
#     model = user

#     def post(self, request):
#         try:
#             uid = get_uid(get_JWT_token(request=request))
#             instance = self.model.objects.filter(UID=uid).first()
#             data = request.data
#             if verification_jwt_decode(data['vtoken']):  # verification token
#                 instance.set_password(data['password'])
#                 response = {
#                     'success': True,
#                     'message': PASSWORD_CHANGED
#                 }
#                 return Response(response, status=status.HTTP_202_ACCEPTED)
#         except Exception as e:
#             response = {
#                 'success': False,
#                 'message': SOMTHING_WENT_WRONG
#             }
#             return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


"""
password change request model

this requires user email

"""


class PasswordChangeRequestView(views.APIView):
    model = user
    permission_classes = (AllowAny,)
    passwordModel = PasswordChangeRequestModel

    def post(self, request):

        try:
            data = request.data['credential']

            if self.model.objects.filter(Q(phone_number=data) | Q(email=data)).exists():
                instance = self.model.objects.filter(
                    Q(phone_number=data) | Q(email=data)).first()
                token = PasswodToken()
                if self.passwordModel.objects.filter(UID=instance.UID).exists():
                    self.passwordModel.objects.filter(
                        UID=instance.UID).delete()
                PasswordInstance = self.passwordModel.objects.create(
                    UID=instance.UID, password=request.data['password'], token=token)
                resp = {}
                if instance.email != ' ':
                    print(instance.email)
                    send_email(request=request,
                               email=instance.email, message=token,)
                    resp['message'] = PASSWORD_VERIFICATION_LINK_SENT_EMAIL.replace(
                        '&&email&&', instance.email[:3])+instance.email.split('@')[1]
                else:
                    sms_(message='concric: click to change password &&LINK&&'.replace(
                        '&&LINK&&', FRONT_END_LINK+"change/password/verify/"+token), to='91'+instance.phone_number)
                    resp['message'] = PASSWORD_VERIFICATION_LINK_SENT_PHONE.replace(
                        '&&phone&&', instance.phone_number[6:])
                response = {
                    'success': True,
                    'data': resp
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {
                    'success': False,
                    'data': {
                        'message': USER_NOT_FOUND,
                        'code': 404
                    }

                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print(e)
            response = {
                'success': False,
                'error': {
                    'message': SOMTHING_WENT_WRONG,
                    'code': 500
                }
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PasswordChangeRequestConfirmationView(views.APIView):
    model = user
    passwordModel = PasswordChangeRequestModel
    permission_classes = (AllowAny,)

    def is_expired(self, exp):
        if exp > timezone.now()+timedelta(minutes=1):
            return False
        return True

    def post(self, request, verif_token):
        try:

            if self.passwordModel.objects.filter(token=verif_token).exists():
                passwodInstance = self.passwordModel.objects.filter(
                    token=verif_token).first()
                if not self.is_expired(passwodInstance.expiration):
                    if passwodInstance.password == passwodInstance.UID:
                        response = {
                            'success': False,
                            'message': "access denied",
                            "code": 401
                        }
                        return Response(response, status=status.HTTP_401_UNAUTHORIZED)
                    userinstance = self.model.objects.get(
                        UID=passwodInstance.UID)
                    userinstance.set_password(passwodInstance.password)
                    userinstance.save()
                    passwodInstance.delete()
                    response = {
                        'success': True,
                        'data': {
                            'message': PASSWORD_CHANGED,
                        }
                    }
                    return Response(response, status.HTTP_202_ACCEPTED)
                else:

                    passwodInstance.delete()

                    response = {
                        'success': False,
                        'data': {
                            'message': PASSWORD_TOKEN_INVALID,
                            'code': 401
                        }
                    }

                    return Response(response, status.HTTP_401_UNAUTHORIZED)

            else:
                response = {
                    'success': False,
                    'error': {
                        'message': TOKEN_NOT_FOUND,
                        'code': 404
                    }
                }
                return Response(response, status.HTTP_404_NOT_FOUND)

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


"""
login views
"""


class LoginUsingPassword(views.APIView):
    model = user
    permission_classes = (AllowAny,)

    def getinsatnce(self, data):
        instance = self.model.objects.filter(
            Q(phone_number=data) | Q(email=data)).first()
        if instance:
            return instance
        else:
            raise NotFound(detail='no user found on given credentials',
                           code=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            data = request.data
            credentials = data['credentials']
            password = data['password']
            try:
                instance = self.getinsatnce(credentials)
                is_auth = authenticate(
                    phone_number=instance.phone_number, password=password)
                if is_auth:
                    token = get_tokens_for_user(instance)
                    print('done')
                    response = {
                        'success': True,

                        'data': {
                            'message': "logged in",
                            'tokens': token,
                            'usertype':instance.user_Type
                        }
                    }
                    return Response(response, status.HTTP_202_ACCEPTED)
                else:
                    response = {
                        'success': False,

                        'error': {
                            'message': INCORRECT_PASSWORD,
                            'code': 409
                        }
                    }
                return Response(response, status=status.HTTP_409_CONFLICT)

            except Exception as e:
                response = {
                    'success': False,
                    'error': {
                        'message': str(e),
                        'code': 404
                    }
                }
                return Response(response, status=status.HTTP_404_NOT_FOUND)
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


class LoginUsingOtp(views.APIView):
    model = user
    # get for sending a request

    def get(self, request):
        pass


# logout view
class LogoutView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):

        try:
            if 'refresh_token' in request.data:
                refresh_token = request.data["refresh_token"]
                token = RefreshToken(refresh_token)
                token.blacklist()
                response = {
                    'success': True,
                    'data': {
                        'message': SUCCESS,
                    }
                }
                print("logout")
                return Response(response, status=status.HTTP_205_RESET_CONTENT)
            raise Exception('token not found')
        except Exception as e:
            response = {
                'success': False,
                'error': {
                    'message': str(e),
                    'code': 404
                }
            }
            return Response(response, status.HTTP_404_NOT_FOUND)


class OtpInstanceGenrator(views.APIView):
    permission_classes = (AllowAny,)
    model = user

    def post(self, request):
        try:
            data = request.data.get('phone_number')
            if re.match(r'^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$', data):
                if not self.model.objects.filter(phone_number=data).exists():
                    response = {
                        'success': False,
                        'error': {
                            'message': USER_NOT_FOUND,
                            'code': 409
                        }
                    }
                    return Response(response, status=status.HTTP_409_CONFLICT)
                otp = genrate_otp()
                request.session['otp_instance'] = otp
                request.session['phone_number_instance'] = data
                # if sms_(message='concric: Your otp is &&OTP&&'.replace('&&OTP&&', otp), to='91'+data):
                if 1:

                    response = {
                        'success': True,
                        'data': {
                            'phone_number': data,
                            'message': OTP_SENT,
                            'otp': otp
                        }
                    }
                    return Response(response, status.HTTP_200_OK)
                response = {
                    'success': False,
                    'error': {
                        'message': INVALID_PHONE_NUMBER,
                        'code': 400
                    }

                }
                return Response(response, status.HTTP_400_BAD_REQUEST, exception=True)

            response = {
                'success': False,
                'error': {
                    'message': INVALID_PHONE_NUMBER,
                    'code': 400
                }

            }
            return Response(response, status.HTTP_400_BAD_REQUEST, exception=True)
        except Exception as e:
            response = {
                'success': False,
                'error': {
                    'message': str(e),
                    'code': 500
                }
            }

            return Response(response, status.HTTP_500_INTERNAL_SERVER_ERROR, exception=True)


class SetPasswordChangeRequestConfirmationView(views.APIView):
    """
    - verification_token
    - password
    """
    model = user
    passwordModel = PasswordChangeRequestModel
    permission_classes = (AllowAny,)

    def is_expired(self, exp):
        if exp > timezone.localtime():
            return False
        return True

    def post(self, request):
        print("helo")
        try:
            verif_token = request.data.get('verification_token')
            if self.passwordModel.objects.filter(token=verif_token).exists():
                passwodInstance = self.passwordModel.objects.filter(
                    token=verif_token).first()
                print(timezone.localtime())

                if not self.is_expired(passwodInstance.expiration):
                    print("url")
                    if passwodInstance.password == passwodInstance.UID:
                        instance = self.model.objects.create(
                            phone_number=passwodInstance.UID)
                        instance.save(phone=passwodInstance.UID)
                        instance.set_password(request.data.get('password'))
                        instance.save()
                        token = get_tokens_for_user(instance)
                        passwodInstance.delete()
                        response = {
                            'success': True,
                            'data': {
                                'message': ACCOUNT_CREATED,
                                'tokens': token
                            }
                        }
                        return Response(response, status.HTTP_202_ACCEPTED)
                    else:
                        response = {
                            'success': False,
                            'error': {
                                'message': "access denied",
                                'code': 401
                            }
                        }
                        return Response(response, status.HTTP_401_UNAUTHORIZED)
                else:

                    response = {
                        'success': False,
                        'data': {
                            'message': PASSWORD_TOKEN_INVALID,
                            'code': 401
                        }
                    }

                    return Response(response, status.HTTP_401_UNAUTHORIZED)

            else:
                response = {
                    'success': False,
                    'error': {
                        'message': TOKEN_NOT_FOUND,
                        'code': 404
                    }
                }

                return Response(response, status.HTTP_404_NOT_FOUND)

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


class ProfileData(views.APIView):
    model = user
    ser = UserProfileSer
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        print("sd")
        try:
            uid = get_uid(get_JWT_token(request=request))
            instance = self.model.objects.filter(UID=uid)
            dataser = self.ser(instance, many=True)
            response = {
                'success': True,
                'data': {
                    'message': SUCCESS,
                },
                'data': dataser.data
            }
            return Response(response, status.HTTP_200_OK)
        except Exception as e:
            print(e)
            print("R")
            response = {
                'success': False,
                'error': {
                    'message': SOMTHING_WENT_WRONG,
                    'code': 500
                }
            }
            return Response(response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProfileImage(views.APIView):
    def get(self, request):
        if request.FILES.get('file') != "":
            profile = img()
            profile.image = request.FILES.get('file')
            j = request.POST['cdata']
            data = json.loads(j)
            profile.save(data)
            response = {
                'success': True,
                'data': {
                    'message': SUCCESS,
                },
            }
            return Response(response, status.HTTP_200_OK)
        else:
            response = {
                'success': True,
                'data': {
                    'message': NOT_FOUND,
                },
            }
            return Response(response, status.HTTP_404_NOT_FOUND)


class fmctokenview(views.APIView):
    model = fmctoken
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            if "long" in request.data and "lat" in request.data:
                longitude = request.data.get('long')
                latitude = request.data.get('lat')
                geolocator = Nominatim(user_agent="geoapiExercises")

                location = geolocator.reverse(latitude+","+longitude)
                pin = str(location).split(",")[3][1:]
            else:
                pin = ""

            if 'HTTP_AUTHORIZATION' in request.META and request.META['HTTP_AUTHORIZATION'] != "null":
                if self.model.objects.filter(UID=get_uid(get_JWT_token(request=request))).exists():
                    instance = self.model.objects.filter(
                        UID=get_uid(get_JWT_token(request=request))).first()
                    instance.token = request.data.get('fmc_token')
                    instance.pin = pin
                    instance.save()
                else:
                    uid = get_uid(get_JWT_token(request=request))
                    instance = self.model.objects.create(
                        UID=uid, token=request.data['fmc_token'], pin=pin)
            else:
                if request.data['fmc_uid'] == "":
                    
                    instance = self.model.objects.create(
                        UID="guest" + str(timezone.now()), token=request.data['fmc_token'])
                else:
                    instance = self.model.objects.filter(
                        UID=request.data['fmc_uid']).first()
                    print("pp")
                    instance.token = request.data['fmc_token']

            instance.save()
            response = {

                'success': True,
                'data': {
                    "store": instance.UID,
                    'code': 200,
                    'message': 'tokenstored'

                }
            }
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"message": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
