# -*- coding: utf-8 -*-

import pygame, sys, os
from mysprite import *
from gestorRecursos import *
from debuger import *


class CuadroTexto(MiSprite):
    def __init__(self,):
        MiSprite.__init__(self)
        self.imagenCuadro=GestorRecursos.CargarImagen("CuadroTexto.png",0)
        self.rect=pygame.Rect(self.imagenCuadro.get_rect())
        self.rect.bottomleft=(100,580)
        MiSprite.establecerPosicion(self,self.rect.bottomleft)
        self.texto=""
        self.image=pygame.Surface((600,200))
        #self.imagenTexto=pygame.Surface((600,200))

    def establecerTexto(self,texto):
        self.texto=texto
        fuente = pygame.font.SysFont('arial', 22);
        # Se crea la imagen del texto
        imagenTexto = fuente.render(texto, True, (255,255,0))
        self.image=pygame.Surface((600,200))
        #self.image.set_colorkey((0,0,0))
        self.image.blit(self.imagenCuadro,pygame.Rect(0,0,600,200))
        self.image.blit(imagenTexto, pygame.Rect(150,80,500,40))

    def draw(self,pantalla):
        pantalla.blit(self.image,self.rect)


class accionable(MiSprite):

    def __init__(self,archivoImagen,pos,area):
        MiSprite.__init__(self)
        self.image = GestorRecursos.CargarImagen(archivoImagen,-1)
        self.rect=pygame.Rect(self.image.get_rect())
        self.rect.bottomleft=pos
        MiSprite.establecerPosicion(self,pos)
        self.area=area
        self.areaPos=pygame.Rect(0,0,area.width,area.height)
    '''
    def establecerOrientacion(self,angulo):
        self.orientacion=angulo
        self.image=self.image.transform.rotate(angulo)
    '''
    def objetoEnArea(self,rect_objeto):
        return self.areaPos.contains(rect_objeto)


    def establecerPosicionPantalla(self,scrollx, scrolly):
        self.scroll=(scrollx,scrolly)
        self.areaPos.left=self.area.left-scrollx
        self.areaPos.bottom=self.area.bottom-scrolly
        MiSprite.establecerPosicionPantalla(self,scrollx,scrolly)


class activable(accionable):#Dos estados, animable para pasar de un estado a otro,colisionable segun su estado
    def __init__(self,archivoImagen,archivoCoord,pos,area,estadoInicial,tiempoCambio):
        accionable.__init__(self,archivoImagen,pos,area)
        hoja=GestorRecursos.CargarImagen(archivoImagen,-1)
        datos=GestorRecursos.CargarArchivoCoordenadas(archivoCoord)
        datos.split()
        self.coordenadas=[]
        for i in range(0,len(datos)/4):
                self.coordenadas.append(pygame.Rect(datos[i*4],datos[i*4+1],datos[i*4+2],datos[i*4+3]))
        self.numImagenes=len(self.coordenadas)
        self.estado=estadoInicial #en principio es boolean pero se podria cambiar facilmente
        self.tiempoCambio=tiempoCambio
        self.instanteAnimacion=0
        self.encendiendo=False
        self.apagando=False
        self.numImagen=0
        if(estadoInicial):
            self.image=self.hoja.subsurface(coordenadas[self.numImagenes])
        else:
            self.image=self.hoja.subsurface(coordenadas[0])


    def cambiarEstado(self):
        if self.apagando:
            self.apagando=False
            self.encendiendo=True
        elif self.encendiendo:
            self.apagando=True
            self.encendiendo=False
        else:
            if self.estado:
                self.apagando=True
            else:
                self.encendiendo=True
        #self.estado=not self.estado

    #def establecerEstado(self,estado):
    #    self.estado=estado

    def update(self,tiempo):
          if(self.apagando):
              if(self.instanteAnimacion<=0):
                  self.instanteAnimacion=0
                  self.estado=False
                  self.apagando=False
                  #self.image=
              else:
                  self.instanteAnimacion-=tiempo
          elif self.encendiendo:
              if(self.instanteAnimacion>=self.tiempoCambio):
                  self.instanteAnimacion=self.tiempoCambio
                  self.estado=True
                  self.encendiendo=False
                  #self.image=
              else:
                  self.instanteAnimacion+=tiempo
          numImagen=int(self.numImagenes*self.instanteAnimacion/self.tiempoCambio)
          if not numImagen==self.numImagen :
              self.numImagen=numImagen
              self.image=self.hoja.subsurface(self.coordenadas[self.numImagen])




