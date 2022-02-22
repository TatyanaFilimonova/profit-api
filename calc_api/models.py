
from django.db import models


class Vendor(models.Model):
    vendor_name = models.CharField(max_length=50)

class Equipment(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,  related_name='equipments',)
    equipment_name_ua = models.CharField(max_length=70, default="")
    equipment_name_ru = models.CharField(max_length=70, default="")
    direction = models.CharField(max_length=15, default="")
    jsname = models.CharField(max_length=30, default="")
    price_inc = models.DecimalField ( max_digits=10, decimal_places=2)
    price_out = models.DecimalField(max_digits=10, decimal_places=2)
    install_price = models.DecimalField(max_digits=10, decimal_places=2)
    install_time = models.DecimalField(max_digits=10, decimal_places=2)
    project_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)