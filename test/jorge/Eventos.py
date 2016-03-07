# -*- coding: utf-8 -*-
from objetos import *

#Causas

#Entrar en un area
AREA=0
#Pulsar accion estando en el area de un accionable
ACCION_AREA=1

#Consecuencias
#Activar un objeto activable, desactivar o cambiar su estado (si esta encendid apagar ys i esta apagado encender
ACTIVAR=0
DESACTIVAR=1
CAMBIAR=2
#Imprimir un mensaje
MENSAJE=3
#Emite un sonido
SONIDO=4
#Termina la escena
FIN=5

class evento:
    def __init__(self,listaCausas,listaAcciones):
        self.causas=listaCausas
        self.acciones=listaAcciones

    def comprobar(self,personaje,action):
        for causa in self.causas:
            if not causa.comprobar(personaje,action):
                return False
        return True

    def lanzar(self,fase):
        for accion in self.acciones:
            accion.lanzar(fase)

class causa:
    def __init__(self,tipo,objeto):
        self.tipo=tipo
        self.objeto=objeto

    def comprobar(self,personaje,action):
        if self.objeto.objetoEnArea(personaje.newposrect):
            if self.tipo==AREA or action:
                return True
        return False



class accion:
    def __init__(self,tipo,objeto,mensaje,sonido):
        self.tipo=tipo
        if self.tipo==ACTIVAR or self.tipo==DESACTIVAR or self.tipo==CAMBIAR:
            self.objeto=objeto
        elif self.tipo==MENSAJE:
            self.mensaje=mensaje
        #todo sonido

    def lanzar(self,fase):  #Recibe fasre para los mensajes si tuvoeramos un objeto en cargado de los mensajes sepasaria solo ese objeto
        if self.tipo==ACTIVAR :
            self.objeto.activar()
        elif self.tipo==DESACTIVAR :
            self.objeto.desactivar()
        elif self.tipo==CAMBIAR :
            self.objeto.cambiarEstado()
        elif self.tipo==MENSAJE :
            fase.mostrarMensaje(self.mensaje)
        elif self.tipo==FIN:
            fase.director.salirEscena()
