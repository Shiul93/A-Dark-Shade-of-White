# -*- coding: utf-8 -*-
import pygame
from pygame.locals import *
from escena import *
from gestorRecursos import *
from fase import *
#Causas

#Entrar en un area
AREA=0
#Pulsar accion estando en el area de un accionable
ACCION_AREA=1
VISTO_CAMARA=2
DiccCausas={
    "area":0,
    "accion":1,
    "visto_camara":2
}


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
DiccConsecuencias={
    "cambiar":2,
    "mensaje":3,
    "fin":5
}

class Evento:
    def __init__(self,listaCausas,listaAcciones):
        self.causas=listaCausas
        self.acciones=listaAcciones

    def comprobar(self,personaje,fase,action):
        for causa in self.causas:
            if not causa.comprobar(personaje,fase,action):
                return False
        return True

    def lanzar(self,fase):
        for accion in self.acciones:
            accion.lanzar(fase)

class Causa:
    def __init__(self,tipo,objeto):
        self.tipo=tipo
        self.objeto=objeto

    def comprobar(self,personaje,fase,action):
        if self.objeto.objetoEnArea(personaje.newposrect):
            if self.tipo==AREA or action:
                return True
        if(self.tipo==VISTO_CAMARA):
            return self.objeto.estaViendo(fase,personaje.posicion)
        return False



class Accion:
    def __init__(self,tipo,objeto,mensaje,sonido):
        self.tipo=tipo
        if self.tipo==ACTIVAR or self.tipo==DESACTIVAR or self.tipo==CAMBIAR:
            self.objeto=objeto
        elif self.tipo==MENSAJE:
            self.mensaje=mensaje
        elif self.tipo==SONIDO:
            self.sonido=sonido

    def lanzar(self,fase):  #Recibe fasre para los mensajes si tuvoeramos un objeto en cargado de los mensajes sepasaria solo ese objeto
        if self.tipo==ACTIVAR :
            self.objeto.activar()
        elif self.tipo==DESACTIVAR :
            self.objeto.desactivar()
        elif self.tipo==CAMBIAR :
            self.objeto.cambiarEstado()
        elif self.tipo==MENSAJE :
            fase.mostrarMensaje(self.mensaje)
        elif self.tipo==SONIDO :
            fase.reproducirSonido(self.sonido
                                 )
        elif self.tipo==FIN:
            fase.finfase=True
            fase.mostrarMensaje("Fase terminada, enhorabuena")


