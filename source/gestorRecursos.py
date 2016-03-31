# -*- coding: utf-8 -*-

import pygame, sys, os
from pygame.locals import *
import json

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
        """FUNCIONA, pero no se usa"""
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
    def CargarImagenSprite(cls, nombre, colorkey=None):
        """FUNCIONA"""
        # Si el nombre de archivo está entre los recursos ya cargados
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga la imagen indicando la carpeta en la que está
            # Asume que la imagen esta contenida en media, hay que indicar la ruta a partir de alli
            # todo Igual seria buena idea hacer un cargar iself.magen para cada tipo de recurso, mapa, personajes, etc...
            fullname = os.path.join(cls.application_path, 'media'+os.path.sep+'sprites', nombre,nombre+'.png')
            print  fullname
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
    def CargarImagenMenu(cls, nombre, colorkey=None):
        """FUNCIONA"""
        # Si el nombre de archivo está entre los recursos ya cargados
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga la imagen indicando la carpeta en la que está
            # Asume que la imagen esta contenida en media, hay que indicar la ruta a partir de alli
            # todo Igual seria buena idea hacer un cargar iself.magen para cada tipo de recurso, mapa, personajes, etc...
            fullname = os.path.join(cls.application_path, 'media'+os.path.sep+'menu',nombre)
            print  fullname
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
    def CargarImagenMapa(cls, nombre,layer, colorkey=None):
        """FUNCIONA"""
        # Si el nombre de archivo está entre los recursos ya cargados
        key = nombre+layer
        print 'Intentando cargar '+nombre+' capa '+layer
        if key in cls.recursos:
            # Se devuelve ese recurso
            print 'ya cargada'
            return cls.recursos[key]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga la imagen indicando la carpeta en la que está
            # Asume que la imagen esta contenida en media, hay que indicar la ruta a partir de alli
            # todo Igual seria buena idea hacer un cargar iself.magen para cada tipo de recurso, mapa, personajes, etc...
            fullname = os.path.join(cls.application_path, 'media'+os.path.sep+'maps',nombre,layer)
            print  fullname
            try:
                imagen = pygame.image.load(fullname)
                print 'Cargando: '+fullname
            except pygame.error, message:
                print 'Cannot load image:', fullname
                raise SystemExit, message
            imagen = imagen.convert()
            if colorkey is not None:
                if colorkey is -1:
                    colorkey = imagen.get_at((0, 0))
                imagen.set_colorkey(colorkey, RLEACCEL)
            # Se almacena
            cls.recursos[key] = imagen
            # Se devuelve
            return imagen

    @classmethod
    def CargarArchivoCoordenadas(cls, nombre):
        """FUNCIONA"""
        nom_spr = nombre
        nombre = 'coord_'+nombre
        # Si el nombre de archivo está entre los recursos ya cargados
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
        # Si no ha sido cargado anteriormente
        else:
            # Se carga el recurso indicando el nombre de su carpeta
            fullname = os.path.join(cls.application_path, 'media'+os.path.sep+'sprites', nom_spr,nombre+'.txt')
            print fullname
            pfile = open(fullname, 'r')
            datos = pfile.read()
            pfile.close()
            # Se almacena
            cls.recursos[nombre] = datos
            # Se devuelve
            return datos

    @classmethod
    def CargarArchivoFase(cls, nombre):
        """FUNCIONA, pero no se usa"""
        # todo Hay que decidir donde vamos a colocar los archivos de Fase
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
        # Si no ha sido cargado anteriormente
        else:
            datos = {}
            fullname = os.path.join(cls.application_path,'source','fases',nombre, nombre+'.txt')
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
            print("Cargando fase "+nombre)
            cls.recursos[nombre]=datos
            return datos

    @classmethod
    def CargarArchivoFaseJSON(cls,nombre):
        """FUNCIONA"""
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
        # Si no ha sido cargado anteriormente
        else:
            fullname = os.path.join(cls.application_path,'source','fases',nombre, nombre+'.json')
            f=open(fullname, 'r')
            datos=json.load(f)
            print("Cargando fase "+nombre)
            cls.recursos[nombre]=datos
            return datos


    @classmethod
    def CargarArchivoCapas(cls,nombre):
        """FUNCIONA"""
        """Obtiene los datos a partir del fichero de configuracion de capas"""
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]
        # Si no ha sido cargado anteriormente
        else:
            layers = []
            line = '#'
            fullname = os.path.join(cls.application_path,'media','maps', nombre,nombre+'.layers')
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
            print("Cargando mapa "+nombre)
            return layers

    @classmethod
    def CargarSonido(cls, nombre):


        # Si el nombre de archivo está entre los recursos ya cargados
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]

        # Si no ha sido cargado anteriormente
        else:
            # Se carga el recurso indicando el nombre de su carpeta
            fullname = os.path.join(cls.application_path,'media','audio','sounds', nombre+'.ogg') #Deberia estar en sup propia carpeta
            sonido = sonido = pygame.mixer.Sound(fullname)

            print fullname
            print("Cargando archivo de sonido"+nombre)

            # Se almacena
            cls.recursos[nombre] = sonido
            # Se devuelve
            return sonido

    @classmethod
    def CargarMusica(cls, nombre):


        # Si el nombre de archivo está entre los recursos ya cargados
        if nombre in cls.recursos:
            # Se devuelve ese recurso
            return cls.recursos[nombre]

        # Si no ha sido cargado anteriormente
        else:
            # Se carga el recurso indicando el nombre de su carpeta
            fullname = os.path.join(cls.application_path,'media','audio','music', nombre+'.ogg') #Deberia estar en sup propia carpeta

            sonido = pygame.mixer.music.load(fullname)

            print fullname
            print("Cargando Musica"+nombre)

            # Se almacena
            cls.recursos[nombre] = sonido
            # Se devuelve
            return sonido