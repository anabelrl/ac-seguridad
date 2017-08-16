from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

import datetime
from django.utils import timezone

#MODELO DE LA BASE DE DATOS. 
#conjunto de tablas, junto con sus atributos y propiedades. 
#las clases son las tablas
#los atributos son las columnas

marcasDisponibles = ['Toyota','Chery','Ford']

# https://docs.djangoproject.com/en/1.10/ref/models/fields/#django.db.models 
# Referencia de todos los tipos.
#migracion: actualizas las bases de datos, la forma o atributos, hasta nombres
#usuarios(cédula, nombre, apellido, teléfono, email, contraseña)
class Persona(models.Model):     #crea tabla
    usuario = models.OneToOneField(User, on_delete=models.CASCADE) # Permite el login con usuario/password.
    nombre = models.CharField(max_length=20) #crea las columnas
    apellido = models.CharField(max_length=25)
    cedula = models.CharField(max_length=20, primary_key=True, verbose_name='cedula', unique=True) #es char porque no voy a hacer operaciones con ese valor
    telefono = models.CharField(max_length=25)
    email = models.EmailField(verbose_name='email address', max_length=255)
    
    def __str__(self):
        return self.nombre + " " +  self.apellido + " cedula: "+ self.cedula
        
    def usuario_con_telefono(self):
        return self.nombre + " " + self.telefono
        
        
#Estacionamiento(RIF, nombre, Numero_de_puestos)        
class Estacionamiento(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE) # Permite el login con usuario/password
    rif = models.CharField(max_length=20, primary_key=True, verbose_name='rif', unique=True)
    nombre = models.CharField(max_length=200)
    numero_de_puestos = models.IntegerField(default=1000)
    acceso_restringido = models.BooleanField(default=True)
    email = models.EmailField(verbose_name='email address', max_length=255)

    def __str__(self):
        return self.rif + " " + self.nombre
        
#vehiculo(Placa,CEDULA,)   
class Vehiculo(models.Model):
    fecha_actual = datetime.datetime.now()
    anos_vehiculos = zip(range(1950,fecha_actual.year+1),range(1950,fecha_actual.year+1))
    
    dueno = models.ForeignKey(Persona, on_delete=models.CASCADE) 
    placa = models.CharField(max_length=25, primary_key = True)
    marca = models.CharField(max_length=25)
    modelo = models.CharField(max_length=25)
    year = models.PositiveSmallIntegerField(choices=anos_vehiculos, default=2000) 
    
    def __str__(self):
        return str(self.placa) + " " + str(self.marca) + " " + str(self.modelo) + " " + str(self.year) + " " + str(self.dueno.cedula)

#Ticket( Placa, RIF,numero,hora_entrada, hora salida)
class Ticket(models.Model):
    placa = models.ForeignKey(Vehiculo, on_delete=models.CASCADE) 
    rif = models.ForeignKey(Estacionamiento, on_delete=models.CASCADE)
    numero_ticket = models.IntegerField(default=0)
    hora_entrada =  models.DateTimeField('Hora de entrada')
    hora_salida =  models.DateTimeField('Hora de salida')
    pagado = models.BooleanField(default=False) # Tiene que añadirse un valor por defecto cuandohay campos booleanos.
    
    def __str__(self):
        return str(self.placa) + " " + str(self.rif) + " " + str(self.numero_ticket) + " " + str(self.hora_entrada) + " " + str(self.hora_salida) + " " + str(self.pagado)

# alertas(numero,tipo)
class Alerta(models.Model):
    numero_alertas = models.AutoField(primary_key = True) # Deberiamos quitar esto o cambiarlo a IntegerField porque aunque se borre la BD igual queda el contador.
    usuario = models.ForeignKey(Persona, on_delete=models.CASCADE, null=True)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, null=True)
    estacionamiento = models.ForeignKey(Estacionamiento, on_delete=models.CASCADE, null=True) #TODO: set null=False
    tipo = models.CharField(max_length=200)
    fecha = models.DateTimeField('fecha de alerta', default=timezone.now)
    
    def __str__(self):
        return self.tipo + " " + str(self.usuario) + " " + str(self.vehiculo) + " " + str(self.estacionamiento) + " " + str(self.fecha)
    
# #Ocurre_a(Cedula,numero,fecha)
# class OcurreA(models.Model):
#     cedula_usuario = models.ForeignKey(Persona, on_delete=models.CASCADE) 
#     numero_alertas = models.ForeignKey(Alerta, on_delete=models.CASCADE )
#     fecha_alertas    = models.DateTimeField('fecha de alerta')
    
#     def __str__(self):
#         return str(self.cedula_usuario) + " " + str(self.numero_alertas) + " " + str(self.fecha_alertas)
        
# #Ocurre_en(RIF,numero,fecha)
# class OcurreEn(models.Model):
#     rif = models.ForeignKey( Estacionamiento, on_delete=models.CASCADE) 
#     numero_alertas = models.ForeignKey(Alerta, on_delete=models.CASCADE)
#     fecha_alertas    = models.DateTimeField('fecha de alerta')
    
#     def __str__(self):
#         return str(self.rif) + " " + str(self.numero_alertas) + " " + str(self.Fecha_alertas)


# # GUSTOS(cédula, gusto_entrada, gusto_sal)
# class Gustos(models.Model):
#     cedula = models.ForeignKey(Usuarios, on_delete=models.CASCADE) 
#     gusto_entrada = models.CharField(max_length=200)
#     gusto_salida = models.CharField(max_length=200)


