from datetime import datetime, date, timedelta, time
import json
from django.db.models import indexes
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import views
from appointments.utils import check__avail, slot_ava, statusgen
from cv001.utils.utils import get_JWT_token, get_uid
from user.models import user
from doctors.models import doctor, office
from .models import Appointment, batch
from .ser import AppointmentSerializer, BatchSerializer
from rest_framework.response import Response
from rest_framework import status
from cv001.messages import *
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from cv001.utils.utils import rettime
from appointments import models


class AppointmentView(views.APIView):
    model = Appointment
    ser = AppointmentSerializer

    def post(self, request):
        try:
            data = request.data
            response = {
                'success': False,
                'data': {
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


class genrateBatches(views.APIView):
    permission_classes = (IsAuthenticated,)
    model = batch
    ofmodel = office
    ser = BatchSerializer

    def post(self, request):
        try:
            days = ['monday', 'tuesday', 'wednesday',
                    'thursday', 'friday', 'saturday', 'sunday']
            today = date.today()
            officedata = self.ofmodel.objects.all()
            for office in officedata:
                batches = self.model.objects.filter(OFID=office.OFID)
                if batches.count() == 0:
                    for i in range(0, 7):
                        d = statusgen(
                            int((today + timedelta(days=i)).weekday()), office)

                        self.model.objects.create(OFID=office.OFID,
                                                  date=today +
                                                  timedelta(days=i),
                                                  name=days[(today +
                                                             timedelta(days=i)).weekday()],
                                                  start=office.start,
                                                  end=office.end,
                                                  min=office.min_time_slot,
                                                  status="active",
                                                  active=d)
                elif batches.count() == 7:
                    exp = batches.filter(
                        date=today - timedelta(days=1)).first()
                    if exp:
                        exp.delete()
                        d = statusgen(
                            int((today + timedelta(days=6)).weekday()), office)

                        new = self.model.objects.create(OFID=office.OFID,
                                                        date=today +
                                                        timedelta(days=6),
                                                        name=days[(today +
                                                                   timedelta(days=6)).weekday()],
                                                        start=office.start,
                                                        end=office.end,
                                                        min=office.min_time_slot,
                                                        status="active",
                                                        active=d)

            response = {
                'success': True,
                'data': {
                    'message': "batches created for all offices",
                    'code': 200
                }

            }
            return Response(response, status.HTTP_200_OK, exception=False)
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
            batches = self.model.objects.all()
            batch = self.ser(batches, many=True)
            response = {
                'success': True,
                'data': {
                    'message': SUCCESS,
                    'code': 200,
                    'data': batch.data
                }

            }
            return Response(response, status.HTTP_200_OK, exception=False)
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


class GetBatches(views.APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    model = batch
    ofmodel = office
    ser = BatchSerializer

    def get(self, request, OFID):
        try:
            batches = self.model.objects.filter(OFID=OFID)
            batch = self.ser(batches, many=True)
            response = {
                'success': True,
                'data': {
                    'message': SUCCESS,
                    'code': 200,
                    'data': batch.data
                }

            }
            return Response(response, status.HTTP_200_OK, exception=False)
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


class GetBatchesTimings(views.APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    model = batch
    ofmodel = office
    ser = BatchSerializer

    def get(self, request, BID):
        try:
            response = {
                'success': True,
                'data': {}
            }
            batches = self.model.objects.filter(BATCHID=BID)
            Date = batches.first().date
            response['date'] = Date
            start = str(batches.first().start).split(":")[0]
            end = str(batches.first().end).split(":")[0]
            for i in range(int(start), int(end)):
                response['data'][i] = {}
                response['data'][i]['time'] = str(i) + ":00"
                response['data'][i]['ava'] = check__avail(i)
                response['data'][i]['slots'] = slot_ava(i)

            return Response(response, status.HTTP_200_OK, )
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


class createAppoin(views.APIView):
    model = Appointment
    doc = doctor
    user = user
    office = office
    batch = batch
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            """
            slug
            batchid
            time
            """
            print(request.data)
            data = request.data
            Docid = self.doc.objects.filter(slug=data['slug']).first()
            ofid = self.office.objects.filter(DOCID=Docid.DOCID).first()
            uid = get_uid(get_JWT_token(request=request))
            batchinstance = self.batch.objects.filter(
                BATCHID=data['batchid']).first()
            appoin_instance = self.model.objects.create(UID=uid, OFID=ofid.OFID,
                                                        PST=time(
                                                            int(data['time']), 00, 00),
                                                        status="Active",
                                                        date=batchinstance.date,
                                                        BATCH=batchinstance.BATCHID)
            appoin_instance.save()
            response = {
                'success': True,
                'data': {
                    'message': "Appointment created",
                    'code': 200,

                }
            }
            return Response(response, status.HTTP_200_OK, exception=False)
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
