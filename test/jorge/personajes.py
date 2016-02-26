# -*- coding: utf-8 -*-

import pygame, sys, os
from pygame.locals import *
from escena import *
from gestorRecursos import *
import math
# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

PI=math.pi

#Movimiento
QUIETO=0
SIGILO=1
NORMAL=2
CARRERA=3

# Direccion

DERECHA = 0
ABAJODER = 315
ABAJO = 270
ABAJOIZQ = 225
IZQUIERDA = 180
ARRIBAIZQ = 135
ARRIBA = 90
ARRIBADER = 45

#Posturas
SPRITE_QUIETO = 0
SPRITE_ANDANDO = 1


# Velocidades de los distintos personajes
VELOCIDAD_JUGADOR = 0.2 # Pixeles por milisegundo
RETARDO_ANIMACION_JUGADOR = 5 # updates que durará cada imagen del personaje
                              # debería de ser un valor distinto para cada postura

VELOCIDAD_SNIPER = 0.12 # Pixeles por milisegundo
RETARDO_ANIMACION_SNIPER = 5 # updates que durará cada imagen del personaje
                             # debería de ser un valor distinto para cada postura
# El Sniper camina un poco más lento que el jugador, y salta menos

GRAVEDAD = 0.0003 # Píxeles / ms2

# -------------------------------------------------
# -------------------------------------------------
# Clases de los objetos del juego
# -------------------------------------------------
# -------------------------------------------------


# -------------------------------------------------
# Clase MiSprite
class MiSprite(pygame.sprite.Sprite):
    "Los Sprites que tendra este juego"
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.posicion = (0, 0)
        self.velocidad = (0, 0)
        self.scroll   = (0, 0)

    def establecerPosicion(self, posicion):
        self.posicion = posicion
        self.rect.left = self.posicion[0] - self.scroll[0]
        self.rect.bottom = self.posicion[1] - self.scroll[1]

    def establecerPosicionPantalla(self, scrollx,scrolly):
        self.scroll = (scrollx,scrolly)
        #(scrollx, scrolly) = self.scroll;
        (posx, posy) = self.posicion
        self.rect.left = posx - scrollx
        self.rect.bottom = posy - scrolly

    def incrementarPosicion(self, incremento):
        (posx, posy) = self.posicion
        (incrementox, incrementoy) = incremento
        self.establecerPosicion((posx+incrementox, posy+incrementoy))

    def update(self, tiempo):
        incrementox = self.velocidad[0]*tiempo
        incrementoy = self.velocidad[1]*tiempo
        self.incrementarPosicion((incrementox, incrementoy))



# -------------------------------------------------
# Clases Personaje

#class Personaje(pygame.sprite.Sprite):
class Personaje(MiSprite):
    "Cualquier personaje del juego"

    # Parametros pasados al constructor de esta clase:
    #  Archivo con la hoja de Sprites
    #  Archivo con las coordenadoas dentro de la hoja
    #  Numero de imagenes en cada postura
    #  Velocidad de caminar y de salto
    #  Retardo para mostrar la animacion del personaje
    def __init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidadCarrera, retardoAnimacion):

        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self);

        # Se carga la hoja (por ahora no se usa sino que cojo nu sprite normal y lo giro
        self.hoja = GestorRecursos.CargarImagen(archivoImagen,-1)
        self.hoja = self.hoja.convert_alpha()

        self.imagen = GestorRecursos.CargarImagen("hitman1_stand.png",-1)
        self.image = GestorRecursos.CargarImagen("hitman1_stand.png",-1)
        # El movimiento que esta realizando
        self.movimiento = QUIETO
        # Lado hacia el que esta mirando
        self.mirando = ABAJO

        # El retardo a la hora de cambiar la imagen del Sprite (para que no se mueva demasiado rápido)
        self.retardoMovimiento = 0;
        # El rectangulo del Sprite
        self.rect = pygame.Rect(0,0,24,24)
        # Las velocidades de caminar y salto
        self.velocidadCarrera = velocidadCarrera
        # El retardo en la animacion del personaje (podria y deberia ser distinto para cada postura)
        self.retardoAnimacion = retardoAnimacion
        # Y actualizamos la postura del Sprite inicial, llamando al metodo correspondiente
        self.actualizarPostura()


    # Metodo base para realizar el movimiento: simplemente se le indica cual va a hacer, y lo almacena
    def mover(self, movimiento,direccion):
        self.movimiento=movimiento
        self.mirando=direccion
        self.velocidadMovimiento=self.velocidadCarrera*self.movimiento/4



    def actualizarPostura(self):
        #El código está pensado para cambiar entre varias animaciones y flipearlas segun si va a la izquierda o a la derecha
        #Rotamos la imagen segun hacia donde esté mirando
        self.image= pygame.transform.rotate(self.imagen,self.mirando)


    def update(self, decorado, tiempo):

        # Esta mirando hacia donde vayamos
        velocidadx=self.velocidadMovimiento*math.cos(self.mirando*PI/180)
        velocidady=-self.velocidadMovimiento*math.sin(self.mirando*PI/180)

        self.actualizarPostura()

        # Aplicamos la velocidad en cada eje      
        self.velocidad = (velocidadx, velocidady)
        #Comprobamos las colisiones primero en el eje x
        #Si se mueve a la derecha sumamos el anchod el personaje
        #Si colisiona en el eje x ponemos la velocidad x a 0
        self.rect.bottomleft=self.posicion
        newposrect=self.rect
        newposrect.left=self.posicion[0]+velocidadx*tiempo
        if(decorado.colision(newposrect)):
            self.velocidad=(0,self.velocidad[1])
            newposrect.left=self.posicion[0]
        #colisiones verticales
        newposrect.bottom=self.posicion[1]+velocidady*tiempo
        if(decorado.colision(newposrect)):
            self.velocidad=(self.velocidad[0],0)
        MiSprite.update(self, tiempo)
        # Y llamamos al método de la superclase para que, según la velocidad y el tiempo
        #  calcule la nueva posición del Sprite

        
        return



# -------------------------------------------------
# Clase Jugador

class Jugador(Personaje):
    "Cualquier personaje del juego"
    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        Personaje.__init__(self,'Jugador.png','coordJugador.txt', [6, 12, 6], VELOCIDAD_JUGADOR,  RETARDO_ANIMACION_JUGADOR);


    def mover(self, teclasPulsadas, arriba, abajo, izquierda, derecha,sigilo,correr):
        # Indicamos la acción a realizar segun la tecla pulsada para el jugador
        direccion=ARRIBA
        movimiento=NORMAL
        if teclasPulsadas[arriba]:
            if(teclasPulsadas[izquierda]):
                direccion=ARRIBAIZQ
            elif(teclasPulsadas[derecha]):
                direccion=ARRIBADER
            else:
                direccion=ARRIBA
        elif teclasPulsadas[abajo]:
            if(teclasPulsadas[izquierda]):
                direccion=ABAJOIZQ
            elif(teclasPulsadas[derecha]):
                direccion=ABAJODER
            else:
                direccion=ABAJO
        elif teclasPulsadas[izquierda]:
            direccion=IZQUIERDA
        elif teclasPulsadas[derecha]:
           direccion=DERECHA
        else:
            movimiento=QUIETO

        if movimiento!=QUIETO:
            if teclasPulsadas[sigilo]:
                movimiento=SIGILO
            elif teclasPulsadas[correr]:
                movimiento=CARRERA

        Personaje.mover(self,movimiento,direccion)

# -------------------------------------------------
# Clase NoJugador

class NoJugador(Personaje):
    "El resto de personajes no jugadores"
    def __init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidad,  retardoAnimacion):
        # Primero invocamos al constructor de la clase padre con los parametros pasados
        Personaje.__init__(self, archivoImagen, archivoCoordenadas, numImagenes, velocidad,  retardoAnimacion);

    # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion por defecto, este metodo deberia de ser implementado en las clases inferiores
    #  mostrando la personalidad de cada enemigo
    def mover_cpu(self, jugador1, jugador2):
        # Por defecto un enemigo no hace nada
        #  (se podria programar, por ejemplo, que disparase al jugador por defecto)
        return

# -------------------------------------------------
# Clase Sniper

class Sniper(NoJugador):
    "El enemigo 'Sniper'"
    def __init__(self):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        NoJugador.__init__(self,'Sniper.png','coordSniper.txt', [5, 10, 6], VELOCIDAD_SNIPER,  RETARDO_ANIMACION_SNIPER);

    # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion de la inteligencia segun este personaje particular
    def mover_cpu(self, jugador1):

        # Movemos solo a los enemigos que esten en la pantalla
        if self.rect.left>0 and self.rect.right<ANCHO_PANTALLA and self.rect.bottom>0 and self.rect.top<ALTO_PANTALLA:
            #Calcula la distancia enambos ejes
            difx=jugador1.posicion[0]-self.posicion[0];
            dify=jugador1.posicion[1]-self.posicion[1];
            ang=math.atan2(-dify,difx)
            direccion=ang*180/PI
            Personaje.mover(self,CARRERA,direccion)
        # Si este personaje no esta en pantalla, no hara nada
        else:
            Personaje.mover(self,QUIETO,ARRIBA)

