from .models import Vendor, Equipment
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