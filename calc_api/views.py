from django.shortcuts import render

from django.http import HttpResponse
from rest_framework.generics import ListAPIView, mixins, CreateAPIView
from .serializers import VendorSerializer, EquipmentSerializer
from .models import Vendor, Equipment, Direction
from decimal import *
from datetime import datetime, timedelta
#from .services import BadRequest, NoContent, PaginationGrossBook, TransactionClassFilter
from rest_framework.exceptions import NotFound, APIException
from django.core.exceptions import BadRequest
#from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.db.models import Sum
from rest_framework.authtoken.views import ObtainAuthToken

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class Equipments(ListAPIView):

    """GrossBook list with backend filter by transaction class"""

    serializer_class = EquipmentSerializer
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Equipment.objects.select_related().all()
        return queryset


class CalculateBudget(CreateAPIView):

    """GrossBook list with backend filter by transaction class"""

    serializer_class = EquipmentSerializer
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Equipment.objects.select_related().all()
        return queryset

    def post(self, request, *args, **kwargs):
        #print("REQUEST DATA: ", request.data)
        queryset = Equipment.objects.select_related().all().values()
        result_lst =[res for res in queryset]
        #print(result_lst)
        project_cost = 0.
        directions = Direction.objects.all()
        direction_list = [d.direction for d in directions]
        if 'Project' in request.data.keys():
          #  print('There would be project cost')
            for direction in direction_list:
                if direction in request.data.keys():
                    for key in request.data.keys():
         #               print(direction, " ", key)
                        if key.find(direction) != -1 and request.data[key] != 'on':
                            project_price = list(filter(
                                lambda res: res['jsname'] == key and res['vendor_id'] == 1, result_lst))[0]['project_price']
                            project_cost += float(int(request.data[key]) * project_price)
          #  print(f"Project cost  = {project_cost}")

        install_cost_knx = 0.
        install_cost_larnitech = 0.
        equipment_cost_knx = 0.
        equipment_cost_larnitech = 0.

        if 'Install' in request.data.keys():
           # print ('There would be install cost')
            for direction in direction_list:
                if direction in request.data.keys():
                    for key in request.data.keys():
                        if key.find(direction) != -1 and request.data[key] != 'on':
                            knx_element = list(filter(
                                lambda res: res['jsname'] == key and res['vendor_id'] == 1, result_lst))[0]
                            larnitech_element = list(filter(
                                lambda res: res['jsname'] == key and res['vendor_id'] == 2, result_lst))[0]
                            install_cost_knx += float(request.data[key]) * float(knx_element['install_price'])
                            install_cost_larnitech += float(request.data[key]) * float(larnitech_element['install_price'])
                            equipment_cost_knx += float(request.data[key]) * float(knx_element['price_out'])
                            equipment_cost_larnitech += float(request.data[key]) * float(larnitech_element['price_out'])
           

        result_json = {
            'Install_cost_knx': install_cost_knx,
            'Install_cost_larnitech':  install_cost_larnitech,
            'Equipment_cost_knx':  equipment_cost_knx,
            'Equipment_cost_larnitech': equipment_cost_larnitech,
            'Project_cost':  project_cost,
                 }

        return Response(result_json)

class GetFormBody(ListAPIView):

    def get(self, request, *args, **kwargs):
        directions = Direction.objects.all()
        direction_list = [d for d in directions]
        res_json = []
        for dir in direction_list:

            queryset = Equipment.objects.filter(
                vendor_id=1).filter(direction_id=dir.id).select_related('vendor', 'direction').all()
            row_list = []
            for res in queryset:
                row = {
                    'equipment_name_ua': res.equipment_name_ua,
                    'equipment_name_ru': res.equipment_name_ru,
                    'jsname': res.jsname
                }
                row_list.append(row)
            res_json.append({
                dir.direction:{'name_ru': dir.direction_name_ru,
                               'name_ua': dir.direction_name_ua,
                               'equipment': row_list,
                               }
                            })

        print(res_json)
        return Response(res_json)