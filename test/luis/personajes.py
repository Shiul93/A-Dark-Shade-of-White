# -*- coding: utf-8 -*-

import pygame, sys, os
from pygame.locals import *
from escena import *
from gestorRecursos import *
from debuger import *
from mysprite import *
from random import *
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

ABAJO=0
IZQUIERDA=1
DERECHA=2
ARRIBA=3

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

def pardeclave(string):
    values=string.split()
    return (int(values[0]),int(values[1]))

def dist(punto1,punto2):
    return math.hypot(punto1[0]-punto2[0],punto1[1]-punto2[1])

# -------------------------------------------------
# -------------------------------------------------
# Clases de los objetos del juego
# -------------------------------------------------
# -------------------------------------------------



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
    def __init__(self, archivoImagen, archivoCoordenadas, velocidadCarrera, retardoAnimacion):

        # Primero invocamos al constructor de la clase padre
        MiSprite.__init__(self);

        # Se carga la hoja (por ahora no se usa sino que cojo nu sprite normal y lo giro

        self.hoja = GestorRecursos.CargarImagen(archivoImagen,-1)
        self.hoja = self.hoja.convert_alpha()

        datos = GestorRecursos.CargarArchivoCoordenadas(archivoCoordenadas)
        datos = datos.split()
        cont=0

        #
        #CARGAMOS LOS DATOS DE LA ANIMACION
        #

        #Valores para la imagen de la animacion. las posturas en este caso son las direcciones y las imagenes los distintos frames
        self.numPostura=0;
        self.numImagenPostura = 0;
        self.coordenadasHoja=[]
        for linea in range(0, 4):
            self.coordenadasHoja.append([])
            tmp = self.coordenadasHoja[linea]
            for postura in range(1, 5):
                tmp.append(pygame.Rect((int(datos[cont]), int(datos[cont+1])), (int(datos[cont+2]), int(datos[cont+3]))))
                cont += 4

        # El movimiento que esta realizando
        self.movimiento = QUIETO
        # Lado hacia el que esta mirando
        self.mirando = ABAJO
        self.velocidadMovimiento=0




        # El retardo a la hora de cambiar la imagen del Sprite (para que no se mueva demasiado rápido)
        self.retardoMovimiento = 0;
        # El rectangulo del Sprite
        self.rect = pygame.Rect(0,0,self.coordenadasHoja[0][0].width,self.coordenadasHoja[0][0].height)
        self.newposrect=pygame.Rect(800,600,32,54)
        # Las velocidades de caminar , correr, etc
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
        # Coloca al personaje mirando hacia la direccion correcta y en el punto adecuado de la animacion
        # self.image= pygame.transform.rotate(self.imagen,self.mirando)
        self.numPostura=self.mirando
        if self.movimiento!=QUIETO:
            self.retardoMovimiento -= 1
        # Miramos si ha pasado el retardo para dibujar una nueva postura
        if (self.retardoMovimiento < 0):
            self.retardoMovimiento = self.retardoAnimacion
            # Si ha pasado, actualizamos la postura
            self.numImagenPostura += 1
            #Si llega al final vuelve al principio
            if self.numImagenPostura >= len(self.coordenadasHoja[self.numPostura]):
                self.numImagenPostura = 0;

            if self.numImagenPostura < 0:
                self.numImagenPostura = len(self.coordenadasHoja[self.numPostura])-1

        self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])


    def update(self, fase, tiempo):
        #if tiempo>1000 :tiempo=1000
        velocidadx=0
        velocidady=0
        # Esta mirando hacia donde vayamos
        if(self.mirando==ARRIBA):
            velocidady=self.velocidadMovimiento*-1
        elif(self.mirando==ABAJO):
            velocidady=self.velocidadMovimiento
        elif(self.mirando==DERECHA):
            velocidadx=self.velocidadMovimiento
        elif(self.mirando==IZQUIERDA):
            velocidadx=self.velocidadMovimiento*-1
        self.actualizarPostura()

        # Aplicamos la velocidad en cada eje      
        self.velocidad = (velocidadx, velocidady)
        #Comprobamos las colisiones primero en el eje x
        #Si colisiona en el eje x ponemos la velocidad x a 0
        #print self.posicion
        newposrect=pygame.Rect(0,0,self.rect.width*2/3,self.rect.height/3)
        newposrect.bottomleft=(self.posicion[0]+self.rect.width/6,self.posicion[1])
        newposrect.left=newposrect.left+velocidadx*tiempo
        newposrect.bottom=newposrect.bottom+velocidady*tiempo
        self.newposrect=newposrect
        if(fase.colision(self.newposrect.copy()) and self.movimiento!=CARRERA):
            self.velocidad=(0,0)
        Debuger.anadirRectangulo(newposrect)
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
        Personaje.__init__(self,'oak.png','coord_oak.txt', VELOCIDAD_JUGADOR,  RETARDO_ANIMACION_JUGADOR);


    def mover(self, teclasPulsadas, arriba, abajo, izquierda, derecha,sigilo,correr):
        # Indicamos la acción a realizar segun la tecla pulsada para el jugador
        direccion=self.mirando
        movimiento=NORMAL
        if teclasPulsadas[arriba]:
            direccion=ARRIBA
        elif teclasPulsadas[abajo]:
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
            else:
                movimiento=NORMAL
        Personaje.mover(self,movimiento,direccion)


    def update(self,fase,tiempo):
        "Acciones especificas del jugador(activar objetos etc)"

        Personaje.update(self,fase,tiempo)
# -------------------------------------------------
# Clase NoJugador

class NoJugador(Personaje):
    "El resto de personajes no jugadores"
    #Interfaz para las clases de los no jugadores que implementa mover_cpu para la IA
    def __init__(self, archivoImagen, archivoCoordenadas,  velocidad,  retardoAnimacion):
        # Primero invocamos al constructor de la clase padre con los parametros pasados
        Personaje.__init__(self, archivoImagen, archivoCoordenadas,  velocidad,  retardoAnimacion);

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
    "El  guardia que te persigue por un grafo de nodos"
    def __init__(self,nodos,grafo,nodoinicial):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        NoJugador.__init__(self,'Guardias.png','coordguardia.txt',  VELOCIDAD_SNIPER,  RETARDO_ANIMACION_SNIPER);
        self.nodos=nodos
        self.grafo=grafo
        self.inicio=nodoinicial #la primera del
        self.destino=nodoinicial
        self.posicion=nodos[nodoinicial]
        # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion de la inteligencia segun este personaje particular
    def mover_cpu(self, jugador1):

        # Movemos solo a los enemigos que esten en la pantalla
            #Calcula la distancia enambos ejes
            dest=self.nodos[self.destino]
            distancia=(dest[0]-self.posicion[0],dest[1]-self.posicion[1])
            #Dibujar el grafo
            for i in range(0,len(self.grafo)):
                ldestinos=self.grafo[i]
                for destino in ldestinos:
                    Debuger.anadirLinea(self.nodos[i],self.nodos[destino])
            Debuger.anadirLinea(self.posicion,dest)
            if abs(distancia[0]+distancia[1])<2 : #Si llega a un destino
                listaDestinos=self.grafo[self.destino]
                mindist=dist(jugador1.posicion,self.nodos[listaDestinos[0]])
                mindistindex=0
                for i in range(0,len(listaDestinos)):#De todos los destinos calcula cual esta mas cerca de personaje
                    newdist=dist(jugador1.posicion,self.nodos[listaDestinos[i]])
                    if newdist<mindist:
                        mindist=newdist
                        mindistindex=i
                self.destino=listaDestinos[mindistindex]
            else: #Si aun no llego
                if(abs(distancia[0])>abs(distancia[1])):
                    if(distancia[0]>0):
                        Personaje.mover(self,NORMAL,DERECHA)
                    else:
                        Personaje.mover(self,NORMAL,IZQUIERDA)
                else:
                    if(distancia[1]>0):
                        Personaje.mover(self,NORMAL,ABAJO)
                    else:
                        Personaje.mover(self,NORMAL,ARRIBA)



class Patrulla(NoJugador):
    "El  guardia que da vueltas por un grafo de nodos"
    def __init__(self,nodos,grafo,nodoinicial):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        NoJugador.__init__(self,'Guardias.png','coordguardia.txt',  VELOCIDAD_SNIPER,  RETARDO_ANIMACION_SNIPER);
        self.nodos=nodos
        self.grafo=grafo
        self.inicio=nodoinicial #la primera del
        self.destino=nodoinicial
        self.posicion=nodos[nodoinicial]
        # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion de la inteligencia segun este personaje particular
    def mover_cpu(self, jugador1):

        # Movemos solo a los enemigos que esten en la pantalla
            #Calcula la distancia enambos ejes
            dest=self.nodos[self.destino]
            distancia=(dest[0]-self.posicion[0],dest[1]-self.posicion[1])
            #Dibujar el grafo
            for i in range(0,len(self.grafo)):
                ldestinos=self.grafo[i]
                for destino in ldestinos:
                    Debuger.anadirLinea(self.nodos[i],self.nodos[destino])
            Debuger.anadirLinea(self.posicion,dest)
            if abs(distancia[0]+distancia[1])<2 : #Si llega a un destino
                self.destino=self.grafo[self.destino][randint(0,len(self.grafo[self.destino])-1)]
            else: #Si aun no llego
                if(abs(distancia[0])>abs(distancia[1])):
                    if(distancia[0]>0):
                        Personaje.mover(self,NORMAL,DERECHA)
                    else:
                        Personaje.mover(self,NORMAL,IZQUIERDA)
                else:
                    if(distancia[1]>0):
                        Personaje.mover(self,NORMAL,ABAJO)
                    else:
                        Personaje.mover(self,NORMAL,ARRIBA)
