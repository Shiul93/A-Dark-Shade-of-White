
from pytmx.util_pygame import load_pygame
import pytmx,pygame,time
import fileinput
pygame.init()
pantalla = pygame.display.set_mode((2000, 1800), 0, 32)

class tmxmap:
    def __init__(self,path):
        self.path  = path
        self.tiled_map = load_pygame(path)
        self.layers = self.tiled_map.layernames
        self.height = self.tiled_map.height
        self.width = self.tiled_map.width
        self.bits = self.tiled_map.tileheight
        self.colisionlayer = self.tiled_map.get_layer_by_name('COLISIONES')
    def __str__(self):
        st = 'Path: '+self.path+'\n'
        st = st+'Layers: \n'
        for layer in self.layers:
            st = st+'\t' +layer+'\n'
        st = st+'Heigth: '+str(self.height)+' tiles\n'
        st = st+'Width: '+str(self.width)+' tiles\n'
        st = st+'Bits: '+str(self.bits)+'\n'
        return st
    def paint_all(self):

        for j in range(0,9):

            images = []
            for y in range(mapa.height):
                for x in range(mapa.width):

                    image = mapa.tiled_map.get_tile_image(x,y,j)
                    images.append(image)

            i=0
            for y in range(mapa.height):
                for x in range(mapa.width):
                    if images[i]!=None:
                        pantalla.blit(images[i],(x * 32, y * 32))
                    i += 1

        pygame.display.flip()




mapa = tmxmap('../media/maps/museo_1.tmx')
print mapa
mapa.paint_all()


print("something")
wait = input("PRESS ENTER TO CONTINUE.")
print("something")