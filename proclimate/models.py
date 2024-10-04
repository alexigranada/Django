from django.db import models
from django.conf import settings
import os

# Create your models here.

class TemperatureData(models.Model):
    file = models.FileField(upload_to='netcdf_files/')
    upload_date = models.DateTimeField(auto_now_add=True)