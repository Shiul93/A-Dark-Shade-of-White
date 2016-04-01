# -*- encoding: utf-8 -*-
from escena import *
from personajes import *
import pygame
from gestorRecursos import *

class Mapa:

    def __init__(self,path):
        """Constructor de la clase, recibe el nombre del archivo que contiene la informacion"""
        #Deberia recibir el archivo
        self.path  = path
        self.layers = GestorRecursos.CargarArchivoCapas(path)
        self.images = {}
        self.load_layers()
        self.rect = self.images[self.layers[0][1]].get_rect() #deberia coger la primera
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
                self.images[layer[1]]= GestorRecursos.CargarImagen(layer[5]).convert()
            else:
                self.images[layer[1]]= GestorRecursos.CargarImagen(layer[5],-1).convert()

    def update(self, scrollx,scrolly):
        #Cuando cambia el scroll cambiamos la posicion del rectangulo que define el trozo de fondo que se muestra
         self.rectSubimagen.left = scrollx
         self.rectSubimagen.top = scrolly

    def paint_all(self,pantalla):
        """Dibuja secuencialmente todas las capas marcadas como visibles"""
        #todo Cambiar nombre del metodo
        for layer in self.layers:

            if layer[2]:
                #Layer[2] es el atributo de visibilidad
                #Layer[1] es el nombre de la capa
                pantalla.blit(self.images[layer[1]],self.rect,self.rectSubimagen)


       #pygame.display.flip()


    def dibujar_pre(self,pantalla):
        """Dibuja secuencialmente todas las capas marcadas como visibles"""
        #todo Cambiar nombre del metodo
        for layer in self.layers:

            if layer[2] and (layer[6]==0):
                #Layer[2] es el atributo de visibilidad
                #Layer[1] es el nombre de la capa
                pantalla.blit(self.images[layer[1]],self.rect,self.rectSubimagen)


        #pygame.display.flip()

    def dibujar_post(self,pantalla):
        """Dibuja secuencialmente todas las capas marcadas como visibles"""
        #todo Cambiar nombre del metodo
        for layer in self.layers:

            if layer[2] and (layer[6]==1):
                #Layer[2] es el atributo de visibilidad
                #Layer[1] es el nombre de la capa
                pantalla.blit(self.images[layer[1]],self.rect,self.rectSubimagen)


    #Comprueba colision en una posicion. se le pasa el id de la capa de colision y devuelve 0 si no hay nada y 1 si hay algo
    #En principiio para usar solo con la capa de colisiones pero se podria usar con cualquiera
    def colisionPunto(self,punto,layer):
        color=self.images[layer].get_at(punto)
        return color.r>0

    def colision(self,rect,layer):
        #Comprueba si hay colision en cualquiera de las 4 esquinas del rectángulo recibido
        #Lo que comprueba es el color del pixel del mapa de colisiones en el punto deseado
        #En este caso se comprueba que el rojo no valga 0
        #Si vale 0 en las 4 esquinas no hay colision
        #Se podria usar tambien el alfa ( seria mas lógico)
        #pygame.Color.r = rojo .g = verde .b = azul .a = alfa

       # for layer in self.layers:
        col1=self.colisionPunto(rect.topleft,layer)
        col2=self.colisionPunto(rect.topright,layer)
        col3=self.colisionPunto(rect.bottomleft,layer)
        col4=self.colisionPunto(rect.bottomright,layer)
        return col1 or col2 or col3 or col4

    def colisionOculta(self,rect,layer):
        #Comprueba si hay colision en cualquiera de las 4 esquinas del rectángulo recibido
        #Lo que comprueba es el color del pixel del mapa de colisiones en el punto deseado
        #En este caso se comprueba que el rojo no valga 0
        #Si vale 0 en las 4 esquinas no hay colision
        #Se podria usar tambien el alfa ( seria mas lógico)
        #pygame.Color.r = rojo .g = verde .b = azul .a = alfa

       # for layer in self.layers:
        col1=self.colisionPunto(rect.topleft,layer)
        col2=self.colisionPunto(rect.topright,layer)
        col3=self.colisionPunto(rect.bottomleft,layer)
        col4=self.colisionPunto(rect.bottomright,layer)
        return col1 or col2 or col3 or col4

