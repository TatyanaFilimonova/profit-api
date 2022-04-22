
from django.db import models
from django.db.models import UniqueConstraint, CheckConstraint, Q


class Vendor(models.Model):
    vendor_name = models.CharField(max_length=50)

class Direction(models.Model):
    direction = models.CharField(max_length=15, default="")
    direction_name_ua = models.CharField(max_length=100, default="")
    direction_name_ru = models.CharField(max_length=100, default="")
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['direction'], name="unique_direction"
            )
        ]

class Equipment(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,  related_name='equipments',)
    equipment_name_ua = models.CharField(max_length=70, default="")
    equipment_name_ru = models.CharField(max_length=70, default="")
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE,  related_name='directions',)
    jsname = models.CharField(max_length=30, default="")
    price_inc = models.DecimalField ( max_digits=10, decimal_places=2)
    price_out = models.DecimalField(max_digits=10, decimal_places=2)
    install_price = models.DecimalField(max_digits=10, decimal_places=2)
    install_time = models.DecimalField(max_digits=10, decimal_places=2)
    project_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['jsname', 'vendor_id'], name="unique_jsname"
            )
        ]


class Customer(models.Model):
    first_name = models.CharField(max_length=20, null=False, blank=False)
    second_name = models.CharField(max_length=20, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)

    class Meta:
        constraints = [
           models.UniqueConstraint(
                fields=['first_name', 'second_name', 'email'], name="unique_customer"
            )
        ]


class Competence(models.Model):
    name = models.CharField(max_length=20, default="")


class Competences(models.Model):
    staff = models.ForeignKey(Customer, on_delete=models.CASCADE,  related_name='staff_data',)
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE,  related_name='staff_competence',)


class Staff(models.Model):
    first_name = models.CharField(max_length=20, null=False)
    second_name = models.CharField(max_length=20, null=False)
    email = models.EmailField(null=False)
    salary_rate = models.DecimalField(max_digits=10, decimal_places=2)
    supervisor = models.BooleanField(default=False)
    fulltimer = models.BooleanField(default=False)


class Phone(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,  related_name='customer_detail', null=True)
    stuff = models.ForeignKey(Staff, on_delete=models.CASCADE,  related_name='staff_detail', null=True)
    phone = models.CharField(max_length=20, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['phone'], name="unique_phone"
            )
        ]


class Stage(models.Model):
    stage = models.CharField(max_length=30, default="")


class Project(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE,  related_name='project_customer',)
    supervisor = models.ForeignKey(Staff, on_delete=models.DO_NOTHING, related_name='project_supervisor',)
    stage = models.ForeignKey(Stage, on_delete=models.DO_NOTHING, related_name='project_supervisor',)


class ProjectFiles(models.Model):
    project_name = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='related_project',)
    name = models.CharField(max_length=100, default="")
    body = models.BinaryField(null=False)