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
        """Obtiene el path a partir del cual se cargaran los recursos <ruta_equipo_local>/A-Dark-Shade-of-White/
        debe ejecutarse antes de utilizar la clase"""

        if getattr(sys, 'frozen', False):
            cls.application_path = os.path.dirname(sys.executable)
        elif __file__:
            # cls.application_path = os.path.dirname(__file__)
            # Ya que esta en source, obtiene el path de la raiz
            cls.application_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

    @classmethod
    def CargarImagen(cls, nombre, colorkey=None):

        # Si el nombre de archivo está entre los recursos ya cargados
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga la imagen indicando la carpeta en la que está
            # Asume que la imagen esta contenida en media, hay que indicar la ruta a partir de alli
            # todo Igual seria buena idea hacer un cargar imagen para cada tipo de recurso, mapa, personajes, etc...
            fullname = os.path.join(cls.application_path, 'media', nombre)
            try:
                imagen = pygame.image.load(fullname)
            except pygame.error, message:
                print 'Cannot load image:', fullname
                raise SystemExit, message
            imagen = imagen.convert()
            if colorkey is not None:
                if colorkey is -1:
                    colorkey = imagen.get_at((0, 0))
                imagen.set_colorkey(colorkey, RLEACCEL)
            # Se almacena
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
            fullname = os.path.join(cls.application_path, 'media', nombre)
            pfile = open(fullname, 'r')
            datos = pfile.read()
            pfile.close()
            # Se almacena
            cls.recursos[nombre] = datos
            # Se devuelve
            return datos

    @classmethod
    def CargarArchivoFase(cls, nombre):
        # todo Hay que decidir donde vamos a colocar los archivos de Fase
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
        # Si no ha sido cargado anteriormente
        else:
            datos = {}
            fullname = os.path.join(cls.application_path, 'fases', nombre)
            f = open(fullname, 'r')
            line = f.readline()
            while line != '':
                if not (str.startswith(line, '#')):
                    info = line.rstrip().split()
                    key = info[0]
                    if len(info) > 2:
                        value = []
                        for i in range(1, len(info)):
                            value.append(int(info[i]))
                        datos[key] = value
                    elif len(info) == 2:
                        if info[0].startswith("$"):
                            value = info[1]
                            datos[key] = value
                        else:
                            value = int(info[1])
                            datos[key] = value
                line = f.readline()
            cls.recursos[nombre] = datos
            return datos
