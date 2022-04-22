from .models import Vendor, Equipment, Project, Customer, Staff, Stage, Phone
from rest_framework import serializers


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ('id', 'vendor_name')


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        vendor = VendorSerializer()
        fields = ('vendor',
                  'equipment_name_ua',
                  'equipment_name_ru',
                  'direction',
                  'jsname',
                  'price_out',
                  'install_price')


class PhoneSerializer(serializers.ModelSerializer):
    model = Phone
    fields =(
        'id',
        'phone'
    )


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        phone = PhoneSerializer()
        fields = (
            'first_name',
            'second_name',
            'email',
            'phone'

        )


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        exclude = ('salary_rate', 'fulltimer' )


class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        customer = CustomerSerializer()
        supervisor = StaffSerializer()
        stage = StageSerializer()
        fields = ('customer',
                  'draft_draw',
                  'supervisor'  
                  'stage'
                  )