# -*- coding: utf-8 -*-

import pygame
from escena import *
from fase import *
from gestorRecursos import *
from menu import *

class Debuger(object):
    textos=[]
    puntos=[]
    lineas=[]
    objetos={}
    imagenTexto=pygame.Surface((ANCHO_PANTALLA,95))

    imagenLineas=pygame.Surface((ANCHO_PANTALLA,ALTO_PANTALLA))
    imagenLineas.set_colorkey((0,0,0))


    debugcolor=(255,255,64)

    @classmethod
    def anadirTextoDebug(cls,texto):
        cls.textos.append(texto)

    @classmethod
    def anadirObjeto(cls,clave,valor):#si funciona el name con 0bjetos solo se pasaria el objeto
        cls.objetos[clave]=valor


    @classmethod
    def anadirPunto(cls,(x,y)):
        cls.puntos.append((x,y))

    @classmethod
    def anadirPuntos(cls,list):
        for punto in list:
            if isinstance(punto,tuple) and len(punto)==2:
                cls.puntos.append(punto)

    @classmethod
    def anadirLinea(cls,(x1,y1),(x2,y2)):
        cls.lineas.append(((x1,y1),(x2,y2)))

    @classmethod
    def anadirLineas(cls,list):
        for linea in list:
            if isinstance(linea,tuple)and len(linea)==2:
                if isinstance(linea[0],tuple) and isinstance(linea[1],tuple) and len(linea[0])==2 and len(linea[1])==2:
                    cls.puntos.append(linea)
    @classmethod
    def anadirRectangulo(cls,rect):
        cls.anadirLinea(rect.topleft,rect.topright)
        cls.anadirLinea(rect.topleft,rect.bottomleft)
        cls.anadirLinea(rect.topright,rect.bottomright)
        cls.anadirLinea(rect.bottomleft,rect.bottomright)


    @classmethod
    def dibujarTexto(cls,pantalla):
        i=0
        #Si hay objetos los añade
        if len(cls.objetos)>0:
            for key,value in cls.objetos.items():
                cls.textos.append(key + " : " + str(value) )
        #carga la fuente
        fuente = pygame.font.SysFont('arial', 16);
        # Se crea la imagen del texto
        for texto in cls.textos:
            i+=1
            cls.imagenTexto = fuente.render(texto, True, cls.debugcolor)
            pantalla.blit(cls.imagenTexto, pygame.Rect(5,5+i*20,ANCHO_PANTALLA-5,100))
        cls.textos=[]
        cls.objetos={}

    @classmethod
    def dibujarLineas(cls,pantalla,scroll):
        for linea in cls.lineas:
            screenline=((linea[0][0]-scroll[0],linea[0][1]-scroll[1]),(linea[1][0]-scroll[0],linea[1][1]-scroll[1]))
    #        if cls.enPantalla(screenline[0]) and cls.enPantalla(screenline[1]):
            pygame.draw.line(cls.imagenLineas,cls.debugcolor,screenline[0],screenline[1])
        pantalla.blit(cls.imagenLineas,(0,0))
        cls.imagenLineas.fill((0,0,0))
        #cls.imagenLineas.set_colorkey((0,0,0))
        cls.lineas=[]

    @classmethod
    def enRectangulo(cls,rect,punto):
        if (punto[0]>=rect.left) and (punto[0]<=rect.right) and (punto[1]>=rect.top) and (punto[1]<=rect.bottom):
            return True
        else:
            return False

    @classmethod
    def enPantalla(cls,punto):
        rect=pygame.Rect(0,0,ANCHO_PANTALLA,ALTO_PANTALLA)
        return cls.enRectangulo(rect,punto)