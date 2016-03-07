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
        return self.area.contains(rect_objeto)


    def establecerPosicionPantalla(self,scrollx, scrolly):
        self.scroll=(scrollx,scrolly)
        self.areaPos.left=self.area.left-scrollx
        self.areaPos.bottom=self.area.bottom-scrolly
        MiSprite.establecerPosicionPantalla(self,scrollx,scrolly)



class activable(accionable):#Dos estados, animable para pasar de un estado a otro,colisionable segun su estado
    def __init__(self,archivoImagen,archivoCoord,pos,area,estadoInicial,tiempoCambio):
        accionable.__init__(self,archivoImagen,pos,area)


        self.hoja=GestorRecursos.CargarImagen(archivoImagen,-1)
        self.hoja=self.hoja.convert_alpha()
        datos=GestorRecursos.CargarArchivoCoordenadas(archivoCoord)
        datos=datos.split()
        self.coordenadas=[]
        for i in range(0,len(datos)/4):
                rect=pygame.Rect(int(datos[i*4]),int(datos[i*4+1]),int(datos[i*4+2]),int(datos[i*4+3]))
                print(rect)
                self.coordenadas.append(rect)
        self.rect=pygame.Rect(self.coordenadas[0])
        self.pos=pos
        self.rect.bottomleft=pos
        MiSprite.establecerPosicion(self,pos)
        self.pos_inicial=self.rect.copy()
        self.numImagenes=len(self.coordenadas)
        self.estado=estadoInicial #en principio es boolean pero se podria cambiar facilmente
        self.tiempoCambio=tiempoCambio

        self.encendiendo=False
        self.apagando=False
        self.numImagen=0
        if(self.estado):
            self.image=self.hoja.subsurface(self.coordenadas[self.numImagenes-1])
            self.instanteAnimacion=tiempoCambio-1
        else:
            self.image=self.hoja.subsurface(self.coordenadas[0])
            self.instanteAnimacion=0
        self.image.set_colorkey((0,0,0))


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

    def activar(self):
       self.apagando=False
       self.encendiendo=True

    def desactivar(self):
       self.apagando=True
       self.encendiendo=False


    def update(self,tiempo):
          if(self.apagando):
              self.instanteAnimacion-=tiempo
              if(self.instanteAnimacion<=0):
                  self.instanteAnimacion=0
                  self.estado=False
                  self.apagando=False
          elif self.encendiendo:
              self.instanteAnimacion+=tiempo
              if(self.instanteAnimacion>=self.tiempoCambio-1):
                  self.instanteAnimacion=self.tiempoCambio-1
                  self.estado=True
                  self.encendiendo=False
          numImagen=int(self.numImagenes*self.instanteAnimacion/self.tiempoCambio)
          if not numImagen==self.numImagen :
              self.numImagen=numImagen
              self.image=self.hoja.subsurface(self.coordenadas[self.numImagen])
          #MiSprite.establecerPosicion(self,self.pos)
          MiSprite.update(self,tiempo)
          Debuger.anadirRectangulo(self.pos_inicial)

'''
def establecerPosicionPantalla(self,scrollx, scrolly):
        self.scroll=(scrollx,scrolly)
        Debuger.anadirRectangulo(self.rect)
        #self.rect.left=self.rect.left-scrollx
        #self.rect.bottom=self.rect.bottom-scrolly
        MiSprite.establecerPosicionPantalla(self,0,0)
        Debuger.anadirRectangulo(self.rect)
        self.rect.left=self.rect.left+scrollx
        self.rect.bottom=self.rect.bottom+scrolly
        Debuger.anadirRectangulo(self.rect)
'''
