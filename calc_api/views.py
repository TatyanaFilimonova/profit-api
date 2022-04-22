from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from rest_framework.generics import ListAPIView, mixins, CreateAPIView
from .serializers import VendorSerializer, EquipmentSerializer, ProjectSerializer
from .models import Vendor, Equipment, Direction, Project, Customer, Phone, Stage, Staff, ProjectFiles
from django.contrib.auth.decorators import login_required
import json
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from decimal import *
from datetime import datetime, timedelta
from rest_framework.exceptions import NotFound, APIException
from django.core.exceptions import BadRequest
#from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.db.models import Sum
from rest_framework.authtoken.views import ObtainAuthToken


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
            for direction in direction_list:
                if direction in request.data.keys():
                    for key in request.data.keys():
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
                                lambda res: res['jsname'] == key and res['vendor_id'] == 1, result_lst))
                            if len(knx_element)>0:
                                knx_element = knx_element[0]
                                install_cost_knx += float(request.data[key]) * float(knx_element['install_price'])
                                equipment_cost_knx += float(request.data[key]) * float(knx_element['price_out'])
                            larnitech_element = list(filter(
                                lambda res: res['jsname'] == key and res['vendor_id'] == 2, result_lst))
                            if len(larnitech_element)>0:
                                larnitech_element = larnitech_element[0]
                                install_cost_larnitech += float(request.data[key]) * float(larnitech_element['install_price'])
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

        return Response(res_json)

@login_required(login_url='/login')
def EditEquipment(request):
    queryset = Equipment.objects.select_related('vendor', 'direction').all().order_by('vendor_id',
                                                                                      'direction_id',
                                                                                      'equipment_name_ua')

    return render(  request,
                    'equipment.html',
                    context={'equipment': queryset},
                 )


def getLists():
    directions = Direction.objects.all()
    vendors = Vendor.objects.all()
    return directions, vendors

@login_required(login_url='/login')
def EditRow(request, id=None):
    directions, vendors = getLists()
    if request.method == "GET":
        row = Equipment.objects.select_related('vendor', 'direction').filter(id=int(id)).all()
        return render(request,
                    'editrow.html',
                    context={'row': row[0], 'directions': directions, 'vendors': vendors},
                 )
    else:
        print("request.POST['id'] ", request.POST['id'])
        row = Equipment.objects.filter(id=request.POST['id']).all()[0]
        direction = Direction.objects.filter(id=request.POST['direction']).all()[0].direction
        row.vendor_id = request.POST['vendor']
        row.direction_id = request.POST['direction']
        row.jsname = direction+request.POST['jsname']
        row.equipment_name_ua = request.POST['equipment_name_ua']
        row.equipment_name_ru = request.POST['equipment_name_ru']
        row.price_inc = request.POST['price_inc'] if request.POST['price_inc'] else None
        row.price_out = request.POST['price_out'] if request.POST['price_out']  else None
        row.install_price = request.POST['install_price'] if request.POST['install_price'] else None
        row.project_price = request.POST['project_price'] if request.POST['project_price'] else None
        row.install_time = request.POST['install_time'] if request.POST['install_time'] else None
        vendor = Vendor.objects.filter(id=request.POST['vendor']).all()[0].vendor_name
        try:
            row.save()
            return redirect('/calc_api/editor/')
        except Exception as e:
            if 'duplicate' in str(e):
                messages.add_message(request, messages.WARNING, 'Пара "Код для расчетов" + "Вендор" должна быть уникальной')
                return render(request,
                              'addrow.html',
                              context={'row': request.POST,
                                       'direction': direction,
                                       'vendor': vendor,
                                       'directions': directions,
                                       'vendors': vendors},
                              )

@login_required(login_url='/login')
def DeleteRow(request, id=None):
    if request.method == "GET":
        Equipment.objects.select_related('vendor', 'direction').filter(id=int(id)).delete()
        return redirect('/calc_api/editor/')


@login_required(login_url='/login')
def AddRow(request, data=None):
    directions, vendors = getLists()
    if request.method == "GET":
        return render(request,
                    'addrow.html',
                    context={'row': data, 'directions': directions, 'vendors': vendors},
                 )
    else:
        direction = Direction.objects.filter(id=request.POST['direction']).all()[0].direction
        vendor = Vendor.objects.filter(id=request.POST['vendor']).all()[0].vendor_name
        row = Equipment(
            vendor_id=request.POST['vendor'],
            direction_id=request.POST['direction'],
            jsname=direction+request.POST['jsname'],
            equipment_name_ua=request.POST['equipment_name_ua'],
            equipment_name_ru=request.POST['equipment_name_ru'],
            price_inc=request.POST['price_inc'] if request.POST['price_inc'] else None,
            price_out=request.POST['price_out'] if request.POST['price_out']  else None,
            install_price=request.POST['install_price'] if request.POST['install_price'] else None,
            project_price=request.POST['project_price'] if request.POST['project_price'] else None,
            install_time=request.POST['install_time'] if request.POST['install_time'] else None)
        try:
            row.save()
            return redirect('/calc_api/editor/')
        except Exception as e:
            if 'duplicate' in str(e):
                messages.add_message(request, messages.WARNING, 'Пара "Код для расчетов" + "Вендор" должна быть уникальной')
                return render(request,
                              'addrow.html',
                              context={'row': request.POST,
                                       'direction': direction,
                                       'vendor': vendor,
                                       'directions': directions,
                                       'vendors': vendors},
                              )


@api_view(('GET', 'POST'))
@renderer_classes((JSONRenderer,))
@login_required(login_url='/login')
def AddDirection(request, id=None):
    if request.method == 'POST':
        body_dict = request.data
        direction = Direction(direction=body_dict['direction'],
                              direction_name_ua=body_dict['direction_name_ua'],
                              direction_name_ru=body_dict['direction_name_ru'])
        try:
            direction.save()
            return Response({'result': 'ok',
                             'id': direction.id,
                             'direction': direction.direction,
                             'direction_name_ua': direction.direction_name_ua,
                             'direction_name_ru': direction.direction_name_ru
                             })
        except Exception as e:
            if 'duplicate' in str(e):
                return Response({'result': str(e)}, status=400)

@api_view(('POST',))
@renderer_classes((JSONRenderer,))
@login_required(login_url='/login')
def DelDirection(request, id=None):
    if request.method == 'POST':
        body_dict = request.data
        direction = Direction.objects.get(id=body_dict['direction'])
        try:
            direction.delete()
            return Response({'result': 'ok'})
        except Exception as e:
            error_text = str(e)
        return Response({'result': error_text}, status=400)

@api_view(('POST',))
@transaction.atomic
def CreateProject(request):
    message = ''
    if request.method == 'POST':
        with transaction.atomic():
            try:
                assert '' not in [request.data['firstName'], request.data['secondName'], request.data['e-mail']], \
                        'Validation error - some mandatory field in user data is blank'
                phone_list = dict(request.data)['phone']
                print(phone_list)
                assert len([ph for ph in phone_list if ph != '']) > 0, \
                    'Validation error - at least one phone number should be present'
                customer = Customer(
                                     first_name=request.data['firstName'],
                                     second_name=request.data['secondName'],
                                     email=request.data['e-mail']
                                    )
                customer.save()
                supervisor = Staff.objects.filter(id=1).get()
                stage = Stage.objects.get(id=1)
                project = Project(   customer=customer,
                                     supervisor=supervisor,
                                     stage=stage
                                  )
                project.save()
                for ph in phone_list:
                    if ph:
                        phone = Phone(phone=ph, customer=customer)
                        phone.save()
                file_list = dict(request.data)['project_files']
                for item in file_list:
                    if item:
                        file = ProjectFiles(project_name=project, name=item.name, body=item.read())
                        file.save()

            except Exception as e:
                print(e)
                message = 'Error: '
                if 'unique_customer' in str(e):
                    message += 'User with this credentials already registered in the system'
                if 'Validation' in str(e):
                    message += str(e)
        return Response({'result': message}, status=(200 if message == '' else 400))
