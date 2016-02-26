
from pytmx.util_pygame import load_pygame
import pygame
from gestorRecursos import *

class mapa:

    def __init__(self,path):
        self.path  = path
        self.layers = self.parse_layer_info()
        self.images = {}
        self.load_layers()



    def __str__(self):
        st = 'Path: '+self.path+'\n'
        st = st+'Layers: \n'
        for layer in self.layers:
            st = st+'\t' +layer[1]+'\n'
        st = st+'Heigth: '+str(self.height)+' tiles\n'
        st = st+'Width: '+str(self.width)+' tiles\n'
        st = st+'Bits: '+str(self.bits)+'\n'
        return st

    def parse_layer_info(self):
        layers = []
        line = '#'
        f=open(self.path + 'museo_1.layers', 'r+')

        while line != '':
            if not(str.startswith(line,'#')):
                info = line.rstrip().split()
                info[0]=int(info[0])
                info[2]=int(info[2])
                info[3]=int(info[3])
                info[4]=int(info[4])
                layers.append(info)
                print info

            line = f.readline()
        return layers

    def load_layers(self):
        for layer in self.layers:
            self.images[layer[1]]= GestorRecursos.CargarImagen(self.path+layer[5])

    def paint_all(self):

        for layer in self.layers:

            if layer[2]:

                pantalla.blit(self.images[layer[1]],(0, 0))


                pygame.display.flip()




    #Comprueba colision en una posicion. se le pasa el id de la capa de colision y devuelve 0 si no hay nada y 1 si hay algo
    #En principiio para usar solo con la capa de colisiones pero se podria usar con cualquiera
    def collision(self,x,y,id):
        layer=self.layers[id];
        image = self.tiled_map.get_tile_image(x*32, y*32, layer[0]);




pygame.init()
pantalla = pygame.display.set_mode((2000, 1800), 0, 32)


m = mapa('../media/maps/museo_1/')

m.paint_all()


raw_input('Presiona tecla para continuar')