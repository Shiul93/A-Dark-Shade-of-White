# -*- coding: utf-8 -*-

import pygame
import os
from os import path
from gestorRecursos import *
ANCHO_PANTALLA =800
ALTO_PANTALLA =720
class Mapa:

    def __init__(self,nombre):
        """Constructor de la clase, recibe la ruta del directorio que contiene las capas y ficheros de configuracion"""
        self.path  = 'maps'+os.path.sep+nombre+os.path.sep

        self.nombre = nombre
        self.layers = GestorRecursos.CargarArchivoCapas(path.join(nombre,nombre+".layers"),self)
        self.images = {}
        self.load_layers()


        self.rect = self.images[(self.layers[0])[1]].get_rect()
        self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
        self.rectSubimagen.left = 0 # El scroll horizontal empieza en la posicion 0 por defecto
        self.rectSubimagen.top = 0 # El scroll vertical empieza en la posicion 0 por defecto


    def __str__(self):
        """Metodo ToString"""
        st = 'Path: '+self.path+'\n'
        st = st+'Layers: \n'
        for layer in self.layers:
            st = st+'\t' +layer[1]+'\n'
        st = st+'Heigth: '+str(self.height)+' tiles\n'
        st = st+'Width: '+str(self.width)+' tiles\n'
        st = st+'Pixels: '+str(self.pixels)+'\n'
        return st



    def load_layers(self):
        """Utiliza el gestor de recursos para cargar las imagenes correspondientes a las capas del mapa"""
        for layer in self.layers:
            #Carga las imagenes en un diccionario usando como clave el nombre de la capa

            if layer[0]==0 :
                self.images[layer[1]]= GestorRecursos.CargarImagen(path.join(self.path,layer[5])).convert()
            else:
                self.images[layer[1]]= GestorRecursos.CargarImagen(path.join(self.path,layer[5]),-1).convert()

    def update(self, scrollx,scrolly):
        #Cuando cambia el scroll cambiamos la posicion del rectangulo que define el trozo de fondo que se muestra
        self.rectSubimagen.left = scrollx
        self.rectSubimagen.top = scrolly

    def dibujar(self):
        """Dibuja secuencialmente todas las capas marcadas como visibles"""

        for layer in self.layers:

            if layer[2]:
                #Layer[2] es el atributo de visibilidad
                #Layer[1] es el nombre de la capa
                pantalla.blit(self.images[layer[1]], self.rect, self.rectSubimagen)


        pygame.display.flip()


    def dibujar_pre(self):
        """Dibuja secuencialmente todas las capas marcadas como visibles"""

        for layer in self.layers:

            if layer[2] and (layer[6]==0):
                #Layer[2] es el atributo de visibilidad
                #Layer[1] es el nombre de la capa
                pantalla.blit(self.images[layer[1]], self.rect, self.rectSubimagen)


        #pygame.display.flip()

    def dibujar_post(self):
        """Dibuja secuencialmente todas las capas marcadas como visibles"""

        for layer in self.layers:

            if layer[2] and (layer[6]==1):
                #Layer[2] es el atributo de visibilidad
                #Layer[1] es el nombre de la capa
                pantalla.blit(self.images[layer[1]], self.rect, self.rectSubimagen)


        #pygame.display.flip()

    #Comprueba colision en una posicion. se le pasa el id de la capa de colision y devuelve 0 si no hay nada y 1 si hay algo
    #En principiio para usar solo con la capa de colisiones pero se podria usar con cualquiera
    def colisionPunto(self,punto):
        color=self.images["colisiones"].get_at(punto)
        return color.r>0

    def colision(self,rect):
        #Comprueba si hay colision en cualquiera de las 4 esquinas del rectángulo recibido
        #Lo que comprueba es el color del pixel del mapa de colisiones en el punto deseado
        #En este caso se comprueba que el rojo no valga 0
        #Si vale 0 en las 4 esquinas no hay colision
        #Se podria usar tambien el alfa ( seria mas lógico)
        #pygame.Color.r = rojo .g = verde .b = azul .a = alfa
        col1=self.colisionPunto(rect.topleft)
        col2=self.colisionPunto(rect.topright)
        col3=self.colisionPunto(rect.bottomleft)
        col4=self.colisionPunto(rect.bottomright)
        return col1 or col2 or col3 or col4





pygame.init()
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA), 0, 32)
GestorRecursos.getPath()

m = Mapa('museo_1')
m.update(0,0)
m.dibujar_pre()
m.dibujar_post()
pygame.display.flip()
raw_input("PULSE")