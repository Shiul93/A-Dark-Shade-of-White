# -*- coding: utf-8 -*-

import pygame, sys, os
from pygame.locals import *


# -------------------------------------------------
# Clase GestorRecursos

# En este caso se implementa como una clase vacía, solo con métodos de clase
class GestorRecursos(object):
    recursos = {}

    @classmethod
    def getPath(cls):
      if getattr(sys, 'frozen', False):
            cls.application_path = os.path.dirname(sys.executable)
      elif __file__:
            cls.application_path = os.path.dirname(__file__)


    @classmethod
    def CargarImagen(cls, nombre, colorkey=None):

        # Si el nombre de archivo está entre los recursos ya cargados
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga la imagen indicando la carpeta en la que está
            fullname = os.path.join(cls.application_path,'imagenes', nombre)
            try:
                imagen = pygame.image.load(fullname)
            except pygame.error, message:
                print 'Cannot load image:', fullname
                raise SystemExit, message
            imagen = imagen.convert()
            if colorkey is not None:
                if colorkey is -1:
                    colorkey = imagen.get_at((0,0))
                imagen.set_colorkey(colorkey, RLEACCEL)
            # Se almacena
            print("Cargando imagen "+ fullname)
            cls.recursos[nombre] = imagen
            # Se devuelve
            return imagen

    @classmethod
    def CargarArchivoCoordenadas(cls, nombre):


        # Si el nombre de archivo está entre los recursos ya cargados
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]

        # Si no ha sido cargado anteriormente
        else:
            # Se carga el recurso indicando el nombre de su carpeta
            fullname = os.path.join(cls.application_path,'imagenes', nombre) #Deberia estar en sup propia carpeta
            pfile=open(fullname,'r')
            datos=pfile.read()
            pfile.close()
            print("Cargando archivo de coordenadas"+nombre)
            # Se almacena
            cls.recursos[nombre] = datos
            # Se devuelve
            return datos

    @classmethod
    def CargarArchivoFase(cls,nombre):

        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
        # Si no ha sido cargado anteriormente
        else:
            datos = {}
            fullname = os.path.join(cls.application_path,'fases', nombre)
            f=open(fullname, 'r')
            line = f.readline()
            while line != '':
                if not(str.startswith(line,'#')):
                    info = line.rstrip().split()
                    key=info[0]
                    if len(info)>2:
                        value=[]
                        for i in range (1, len(info)):
                            value.append(int(info[i]))
                        datos[key]=value
                    elif len(info)==2:
                        if info[0].startswith("$"):
                            value=info[1]
                            datos[key]=value
                        else :
                            value=int(info[1])
                            datos[key]=value
                line = f.readline()
            print("Cargando fase"+nombre)
            cls.recursos[nombre]=datos
            return datos
    @classmethod
    def CargarArchivoCapas(cls,nombre):
        """Obtiene los datos a partir del fichero de configuracion de capas"""
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
        # Si no ha sido cargado anteriormente
        else:
            layers = []
            line = '#'
            fullname = os.path.join(cls.application_path,'mapas', nombre)
            f=open(fullname, 'r+')

            while line != '':
                if not(str.startswith(line,'#')):
                    #Se obtienen el resto de caracteristicas del fichero de configuracion
                    info = line.rstrip().split()
                    info[0]=int(info[0])
                    info[2]=int(info[2])
                    info[3]=int(info[3])
                    info[4]=int(info[4])
                    info[5]=info[5]
                    info[6]=int(info[6])
                    layers.append(info)


                line = f.readline()
            print("Cargando mapa"+nombre)
            return layers