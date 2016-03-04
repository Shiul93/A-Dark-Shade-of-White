# -*- coding: utf-8 -*-

import pygame, sys, os

# -------------------------------------------------
# Clase MiSprite
# Clase base de la que derivaran las demas clases de sprite
class MiSprite(pygame.sprite.Sprite):
    "Los Sprites que tendra este juego"

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.posicion = (0, 0)
        self.velocidad = (0, 0)
        self.scroll   = (0, 0)


    def establecerPosicion(self, posicion):
        #Establece la posicion y coloca el sprite en su posicion en pantalla restandole el scroll
        self.posicion = posicion
        self.rect.left = self.posicion[0] - self.scroll[0]
        self.rect.bottom = self.posicion[1] - self.scroll[1]

    def establecerPosicionPantalla(self, scrollx,scrolly):
        #Actualiza el scroll y establece la posicion y coloca el sprite en su posicion en pantalla restandole el scroll
        self.scroll = (scrollx,scrolly)
        (posx, posy) = self.posicion
        self.rect.left = posx - scrollx
        self.rect.bottom = posy - scrolly

    def incrementarPosicion(self, incremento):
        (posx, posy) = self.posicion
        (incrementox, incrementoy) = incremento
        self.establecerPosicion((posx+incrementox, posy+incrementoy))

    def update(self, tiempo):
        #Actualiza la posicion segun la velocidad y el tiempo
        incrementox = self.velocidad[0]*tiempo
        incrementoy = self.velocidad[1]*tiempo
        self.incrementarPosicion((incrementox, incrementoy))


