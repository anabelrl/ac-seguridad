import socketserver
import socket
import threading
import os
import json
import sys

# Para cargar django ref1: https://stackoverflow.com/questions/8047204/django-script-to-access-model-objects-without-using-manage-py-shell
# Respuesta de: Alkindus
# ref2: https://stackoverflow.com/questions/41518910/how-to-make-a-script-to-insert-data-in-my-default-sqlite3-database-django
# Respuesta de: skoll
import django
sys.path.append('/home/ubuntu/workspace/project')
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
django.setup()

from ac_seguridad.models import *
import manejador.mysocket as mysocket
from django.utils import timezone

class MalformedMessage(Exception): pass
class ConnectionClosed(Exception): pass

def manejar_mensaje(mensaje):
    '''
        args:
            mensaje: es un diccionario que contiene las claves definidas en keys.
        keys:
            estacionamiento: es el rif del estacionamiento, con formato J-XXXXXXXX.
            placa: refiere a la placa del vehículo con formato venezolano.
            puerta: refiere a la puerta de entrada del estacionamiento.
            tipo: tipo de mensaje y sus valores están dentro de tipos.
            ticket: 
            accion: entrada o salida.
        tipos:
            ambos:
                placa_leida.
            entrada:
                entrada_estacionamiento,
            salida:
                salida_estacionamiento
            
            ticket_pagado,
            
            
        returns: devuelve al cliente un mensaje diciendo 'OK_entrada' o 'NO_entrada'
        
            
    '''
    tipo = mensaje['tipo']
    rif = mensaje['estacionamiento']
    placa = mensaje['placa']
    puerta = mensaje['puerta']
    accion = mensaje['accion']
    
    respuesta = mensaje.copy()
    vehiculo = None
    permite_entrada = False
    estacionamiento = Estacionamiento.objects.get(rif=rif)
    if (tipo == 'placa_leida'):
        # Como nos aseguramos que SIEMPRE vamos a recibir una placa válida,
        # no tenemos que hacer esas verificaciones.
        try:
            vehiculo = Vehiculo.objects.get(placa=placa)
        
        except Vehiculo.DoesNotExist:
            # TODO: ver si el estacionamiento permite entrada o no.
            print("el Vehiculo {} no existe en la base de datos".format(placa))
            
        #vehiculo registrado
        if (vehiculo is not None):
            respuesta['tipo'] = "OK_entrada_estacionamiento"
            ticket = generar_ticket_registrados(vehiculo,estacionamiento)
            respuesta['ticket'] = ticket.numero_ticket
            generar_actividad(estacionamiento=estacionamiento,
                              ticket=ticket,
                              vehiculo=vehiculo,
                              persona = vehiculo.dueno,
                              tipo="entrada_estacionamiento")
            
        #genera un ticket de los no registrados pero si hay           
        if ((vehiculo is None) and (not estacionamiento.acceso_restringido)):
            respuesta['tipo'] = "OK_entrada_estacionamiento"
            respuesta['ticket'] = generar_ticket_no_registrados(placa,estacionamiento)
            
        #No permite entrada por no estar registrado y tener acceso rest.
        if ((vehiculo is None) and (estacionamiento.acceso_restringido)):
            respuesta['tipo'] = "NO_entrada_estacionamiento"
            respuesta['ticket'] = None
            
    return respuesta

def generar_ticket_registrados(vehiculo,estacionamiento): 
    ticket = Ticket(placa =  vehiculo,
                    rif = estacionamiento,
                    hora_entrada =  timezone.now(),
                    hora_salida =  None,
                    pagado = False 
                   )
    ticket.save()
    return ticket

def generar_ticket_no_registrados(placa,estacionamiento): 
    ticket = TicketNoRegistrado(placa =  placa,
                    rif = estacionamiento,
                    hora_entrada =  timezone.now(),
                    hora_salida =  None,
                    pagado = False 
                   )
    ticket.save()
    return ticket.numero_ticket
    
def generar_actividad(estacionamiento, vehiculo, persona, tipo, ticket=None):
    actividad = Actividad(estacionamiento=estacionamiento, 
                          vehiculo=vehiculo,
                          usuario=persona,
                          tipo=tipo,
                          ticket=ticket,
                          fecha=timezone.now())
    actividad.save()
    
##############################################################################
############################## TCP y FILES ###################################
##############################################################################
class FilesTCPHandler(socketserver.StreamRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.data = self.rfile.readline().strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        self.wfile.write(self.data.upper())


##############################################################################
############################## HILOS Y TCP ###################################
##############################################################################
class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        sock = mysocket.MySocket(self.request)
        mensaje = sock.receive()
        respuesta = manejar_mensaje(mensaje)
        sock.sendall_json(respuesta)
        print("Mensaje recibido: {}".format(mensaje))
        print("Mensaje enviado: {}".format(respuesta))
        
        # cur_thread = threading.current_thread()
        # response = bytes("{}: {}".format(cur_thread.name, respuesta), 'ascii')
        # self.request.sendall(response)
        
class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


##############################################################################
############################## Forks Y TCP ###################################
##############################################################################
class ForkedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        sock = mysocket.MySocket(self.request)
        mensaje = sock.receive()
        respuesta = manejar_mensaje(mensaje)
        sock.sendall_json(respuesta)
        print("Mensaje recibido: {}".format(mensaje))
        print("Mensaje enviado: {}".format(respuesta))
        # response = bytes("{}: {}".format(os.getpid(), mensaje), 'ascii')
        # self.request.sendall(response)

class ForkedTCPServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass