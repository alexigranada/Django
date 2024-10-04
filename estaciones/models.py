from django.db import models

''' Create your models here. 
Creación de tablas
'''

class Estacion(models.Model):
    nombre = models.CharField(max_length=50)
    municipio = models.CharField(max_length=50)
    altura = models.DecimalField(decimal_places=3, max_digits=20)

    def __str__(self):
        return self.nombre 

class Niebla (models.Model):
    fecha = models.DateTimeField()
    temperatura = models.FloatField()
    niebla = models.FloatField()
    estacion = models.ForeignKey(Estacion, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.fecha) + ' - Temperatura: ' +  str(self.temperatura) + ' - Niebla: ' + str(self.niebla)