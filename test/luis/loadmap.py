
from pytmx.util_pygame import load_pygame
import pygame
from gestorRecursos import *
ANCHO_PANTALLA =1600
ALTO_PANTALLA =1280
class mapa:

    def __init__(self,path):
        """Constructor de la clase, recibe la ruta del directorio que contiene las capas y ficheros de configuracion"""
        self.path  = path
        self.layers = self.parse_layer_info()
        self.images = {}
        self.load_layers()

        #todo Manejar el scroll
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

    def parse_layer_info(self):
        """Obtiene los datos a partir del fichero de configuracion de capas"""
        layers = []
        line = '#'
        f=open(self.path + 'museo_1.layers', 'r+')

        while line != '':
            if (str.startswith(line,'W')):
                #Anchura del mapa (EN TILES)
                self.width = int(line.rstrip().split()[1])
            elif (str.startswith(line,'H')):
                #Altura del mapa (EN TILES)
                self.height = int(line.rstrip().split()[1])
            elif (str.startswith(line,'P')):
                #Lado del tile [EN PIXELS)
                self.pixels = int(line.rstrip().split()[1])

            elif not(str.startswith(line,'#')):
                #Se obtienen el resto de caracteristicas del fichero de configuracion
                info = line.rstrip().split()
                info[0]=int(info[0])
                info[2]=int(info[2])
                info[3]=int(info[3])
                info[4]=int(info[4])
                layers.append(info)


            line = f.readline()
        return layers

    def load_layers(self):
        """Utiliza el gestor de recursos para cargar las imagenes correspondientes a las capas del mapa"""
        for layer in self.layers:
            #Carga las imagenes en un diccionario usando como clave el nombre de la capa
            self.images[layer[1]]= GestorRecursos.CargarImagen(self.path+layer[5],-1).convert()

    def update(self, scrollx,scrolly):
        #Cuando cambia el scroll cambiamos la posicion del rectangulo que define el trozo de fondo que se muestra
        #todo ESTA COPIADO DIRECTAMENTE DEL DE FASE AUN NO SE MANEJA SCROLL
        self.rectSubimagen.left = scrollx
        self.rectSubimagen.top = scrolly

    def paint_all(self):
        """Dibuja secuencialmente todas las capas marcadas como visibles"""
        #todo Cambiar nombre del metodo
        for layer in self.layers:

            if layer[2]:
                #Layer[2] es el atributo de visibilidad
                #Layer[1] es el nombre de la capa
                pantalla.blit(self.images[layer[1]],(0, 0))


        pygame.display.flip()






    #Comprueba colision en una posicion. se le pasa el id de la capa de colision y devuelve 0 si no hay nada y 1 si hay algo
    #En principiio para usar solo con la capa de colisiones pero se podria usar con cualquiera
    def collision(self,x,y,id):
        #todo Detectar colisiones con las capas marcadas como colisionables
        layer=self.layers[id];
        image = self.tiled_map.get_tile_image(x*32, y*32, layer[0]);




pygame.init()
pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA), 0, 32)


m = mapa('../../media/maps/museo_1/')

m.paint_all()


raw_input('Presiona tecla para continuar')