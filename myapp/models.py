from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Create your models here.

class User(AbstractUser):
    phone = models.CharField(max_length=15)
    usertype = models.IntegerField()

class Appointment(models.Model):
    device=models.CharField(max_length=40,null=True)
    brand=models.CharField(max_length=40,null=True)
    option=models.CharField(max_length=40,null=True)
    description=models.TextField(null=True)
    file=models.FileField(upload_to='static/uploads',null=True)
    uid=models.IntegerField(null=True)
    appointment_progress=models.IntegerField(null=True,default=0)



class Estimation(models.Model):    
    observation=models.TextField(null=True)
    remarks=models.TextField(null=True)
    deliverydate=models.DateTimeField(null=True)
    price=models.CharField(max_length=50,null=True)
    eid=models.IntegerField(null=True)