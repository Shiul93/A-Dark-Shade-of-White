
from pytmx.util_pygame import load_pygame
import pygame

class tmxmap:

    def __init__(self,path):
        self.path  = path
        self.tiled_map = load_pygame(path+'.tmx')
        self.layers = self.parse_layer_info()
        self.height = self.tiled_map.height
        self.width = self.tiled_map.width
        self.bits = self.tiled_map.tileheight
        self.colisionlayer = self.tiled_map.get_layer_by_name('COLISIONES')


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
        f=open(self.path + '.layers', 'r+')

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

    def paint_all(self):

        for layer in self.layers:

            if layer[2]:
                images = []
                for y in range(self.height):
                    for x in range(self.width):

                        image = self.tiled_map.get_tile_image(x,y,layer[0])
                        if image!=None:
                            image.set_alpha(layer[4])
                        images.append(image)

                i=0
                for y in range(self.height):
                    for x in range(self.width):
                        if images[i]!=None:
                            pantalla.blit(images[i],(x * 32, y * 32))
                        i += 1

            pygame.display.flip()

    def paint_layer_id(self,id):
        layer = self.layers[id]
        images = []
        for y in range(self.height):
            for x in range(self.width):

                image = self.tiled_map.get_tile_image(x, y, layer[0])
                if image!=None:
                    image.set_alpha(layer[4])
                images.append(image)

        i=0
        for y in range(self.height):
            for x in range(self.width):
                if images[i]!=None:
                    pantalla.blit(images[i],(x * 32, y * 32))
                i += 1

        pygame.display.flip()

    #Comprueba colision en una posicion. se le pasa el id de la capa de colision y devuelve 0 si no hay nada y 1 si hay algo
    #En principiio para usar solo con la capa de colisiones pero se podria usar con cualquiera
    def collision(self,x,y,id):
        layer=self.layers[id];
        image = self.tiled_map.get_tile_image(x*32, y*32, layer[0]);




pygame.init()
pantalla = pygame.display.set_mode((2000, 1800), 0, 32)


mapa = tmxmap('../media/maps/museo_1')

mapa.paint_layer_id(1)


raw_input('Presiona tecla para continuar')