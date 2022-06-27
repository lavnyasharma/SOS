import code
from email import message
from rest_framework import views
from sqlalchemy import true
from cv001.utils.utils import get_JWT_token, get_uid
from sos.ser import serrr
from user.models import user
from doctors.models import doctor, office
from rest_framework.response import Response
from rest_framework import status
from cv001.messages import *
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from cv001.utils.utils import rettime
from sos.models import *
from user.utils.jwt import *
from urllib.request import urlopen
import json
from geopy.geocoders import Nominatim
from user.models import *
from .fmc import send_fmc_sms


class sosView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            geolocator = Nominatim(user_agent="geoapiExercises")

            Latitude = str(request.data["lat"])
            Longitude = str(request.data["long"])

            location = geolocator.reverse(Latitude+","+Longitude)

            phone = request.data["pno"]
            lon = request.data["long"]
            lat = request.data["lat"]
            jwt = sos_jwt(phone)
            instance = guest_sos.objects.create(
                pno=phone, long=lon, lat=lat, token=jwt, pin=str(location).split(",")[3])
            hinstance = user.objects.filter(
                pin=str(location).split(",")[3][1:]).all()
           
            if hinstance:
                for i in hinstance:
                    fmcinstance = fmctoken.objects.filter(
                        UID=i.UID).all()
                    if fmcinstance:
                        for j in fmcinstance:
                            send_fmc_sms(
                                j.token, "SOS Alert! Your friend is in danger. Please contact him/her ASAP.")
            response = {
                'success': True,
                'data': {
                    'token': jwt,
                    'code': 200,
                    'message': 'SOS request sent successfully'

                }
            }
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"message": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
    
class updateView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            token = request.data["token"]
            lon = request.data["long"]
            lat = request.data["lat"]
            uid = sos_decode(token)
            if uid:
                instance = update_quads.objects.create(
                    long=lon, lat=lat, token=token)
                response = {
                    'success': True,
                    'data': {
                        'code': 200,
                        'message': 'coordinates updated successfully'

                    }
                }
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(e)
            return Response({"message": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)



class freeView(views.APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            geolocator = Nominatim(user_agent="geoapiExercises")

            Latitude = str(request.data["lat"])
            Longitude = str(request.data["long"])

            location = geolocator.reverse(Latitude+","+Longitude)

            phone = request.data["pno"]
            lon = request.data["long"]
            lat = request.data["lat"]
            jwt = sos_jwt(phone)
            instance = freeway.objects.create(
                pno=phone, long=lon, lat=lat, token=jwt, pin=str(location).split(",")[3])
            fmcinstance  = fmctoken.objects.all()
            for j in fmcinstance:
                send_fmc_sms(
                    j.token, "Auser is requesting to clear the free way")
            response = {
                'success': True,
                'data': {
                    'token': jwt,
                    'code': 200,
                    'message': 'SOS request sent successfully'

                }
            }
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"message": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)



class sosgetView(views.APIView):
    permission_classes = (AllowAny,)
    def post(self,request):
        try:
            print(request.data)
            data = request.data['token']
            print(data)
            instance = guest_sos.objects.filter(token=data).first()

            response = {
                'pno': instance.pno,
                'long': instance.long,
                'lat': instance.lat,
                'time': instance.time,
                'status': instance.status,
                'pin': instance.pin,
                'ip': instance.ip,
                'token': instance.token,
                'success': True,
                'data': {
                    
                    'code': 200,
                    'message': 'SOS request sent successfully'

                }
            }
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"message": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
   


class sosgetallView(views.APIView):
    permission_classes = (AllowAny,)
    def post(self,request):
        try:
            
            instance = guest_sos.objects.all()
            instanceser = serrr(instance, many=True)
            data = instanceser.data

            response = {
                "hh": data,
                'data': {
                    
                    'code': 200,
                    'message': 'SOS request sent successfully'

                }
            }
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"message": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
   

