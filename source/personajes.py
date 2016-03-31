# -*- coding: utf-8 -*-

import pygame, sys, os
from pygame.locals import *
from escena import *
from gestorRecursos import *
from debuger import *
from mysprite import *
from random import *
import math
from auxiliares import *
# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------
OFFSET=(16,-24)
PI=math.pi

#Estados de la IA
QUIETO=0
PATRULLANDO=1
DEAMBULANDO=2
LLENDO_A_ALARMA=3
VOLVIENDO_A_PATRULLA=4
PERSIGUIENDO=5

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

VELOCIDAD_SNIPER = 0.10 # Pixeles por milisegundo
RETARDO_ANIMACION_SNIPER = 5 # updates que durará cada imagen del personaje
                             # debería de ser un valor distinto para cada postura
# El Sniper camina un poco más lento que el jugador, y salta menos




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

        self.hoja = GestorRecursos.CargarImagenSprite(archivoImagen,-1)
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
        self.colision=False



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
        self.colision=False
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
        newposrect=pygame.Rect(0,0,self.rect.width/3,self.rect.height/6)
        newposrect.center=(self.posicion[0],self.posicion[1])
        newposrect.left=newposrect.left+velocidadx*tiempo
        newposrect.bottom=newposrect.bottom+velocidady*tiempo
        self.newposrect=newposrect
        if(fase.colision(self.newposrect.copy())):
            self.velocidad=(0,0)
            self.colision=True
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
        Personaje.__init__(self,'oak','oak', VELOCIDAD_JUGADOR,  RETARDO_ANIMACION_JUGADOR);


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
        Debuger.anadirObjeto("posicion",self.posicion)
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
    def mover_cpu(self, jugador1, fase):
        # Por defecto un enemigo no hace nada
        #  (se podria programar, por ejemplo, que disparase al jugador por defecto)
        return



class Guardia(NoJugador):
    "El  guardia que da vueltas por un grafo de nodos y sabe llegar a un destino"
    def __init__(self,nodos,grafo,recorrido):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        NoJugador.__init__(self,'guardia','guardia',  VELOCIDAD_SNIPER,  RETARDO_ANIMACION_SNIPER)
        self.nodos=nodos
        self.grafo=grafo
        self.recorrido=recorrido #la primera del
        self.destino=self.recorrido[0]
        self.posicion=nodos[self.recorrido[-1]]
        self.visto=False
        self.ruta=list(self.recorrido)
        self.siguiente=self.recorrido[-1]
        self.estado=PATRULLANDO
        self.tiempobusqueda=0
        self.tiempopersecucion=0
        self.rutalocal=[]
        self.destinolocal=None
        self.siguientelocal=None
        # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion de la inteligencia segun este personaje particular
    def mover_cpu(self, jugador1, fase):
            self.movimiento = NORMAL
            for i in range(0,len(self.grafo)):
                ldestinos=self.grafo[i]
                for destino in ldestinos:
                    Debuger.anadirLinea(self.nodos[i],self.nodos[destino])
            '''
            Debuger.anadirTextoDebug("Ruta : "+ str(self.rutalocal))
            Debuger.anadirTextoDebug("Estado : " + str(self.estado))
            Debuger.anadirTextoDebug(("Destino : "+ str(self.destinolocal)))
            Debuger.anadirTextoDebug(("Siguiente : "+ str(self.siguientelocal)))
            Debuger.anadirTextoDebug(("posicion : "+ str(self.posicion)))
'''
             #Si ve al personaje...


            if self.estaViendo(fase,jugador1.posicion,PI*3/4):
                if not self.visto:
                    self.visto=True
                    self.estado=PERSIGUIENDO
                    self.rutalocal=fase.calcular_ruta_local(self.posicion,jugador1.posicion)
                    if len(self.rutalocal)>0:
                        self.siguientelocal=self.rutalocal[-1]
                        self.destinolocal=self.rutalocal[0]
            else: #te ha perdido de vista
                if self.visto:
                    self.visto=False
                    self.tiempopersecucion=5000

            if self.estado==PERSIGUIENDO:
                self.dest=self.siguientelocal.pos
                self.distancia=(self.dest[0]-self.posicion[0],self.dest[1]-self.posicion[1])
                if abs(self.distancia[0]+self.distancia[1])<2 : #Si llega a un destino (eligira el siguiente segun lo qu este haciendo)
                    self.rutalocal=fase.calcular_ruta_local(self.posicion,jugador1.posicion)
                    if len(self.rutalocal)>0:
                        self.destinolocal=self.rutalocal[0]
                        self.siguientelocal=self.rutalocal.pop()
                        self.dest=self.siguientelocal.pos#asegurarlo
                        self.distancia=(self.dest[0]-self.posicion[0],self.dest[1]-self.posicion[1])
                    else:
                        self.dest=jugador1.posicion
                        self.distancia=(self.dest[0]-self.posicion[0],self.dest[1]-self.posicion[1])
            else:

                self.dest=self.nodos[self.siguiente]
                self.distancia=(self.dest[0]-self.posicion[0],self.dest[1]-self.posicion[1])

                if abs(self.distancia[0]+self.distancia[1])<2 : #Si llega a un destino (eligira el siguiente segun lo qu este haciendo)
                    destinos=list(self.grafo[self.siguiente])
                    for destino in destinos:
                        if(fase.colisionLinea(self.posicion,self.nodos[destino],7)):
                            destinos.remove(destino)
                    if(self.estado==DEAMBULANDO)  :
                        self.siguiente=destinos[randint(0,len(destinos)-1)]
                    elif(self.estado==LLENDO_A_ALARMA or self.estado==PATRULLANDO or self.estado==VOLVIENDO_A_PATRULLA):
                        if self.destino!=self.siguiente:
                            if len(self.ruta)>0 and self.ruta[len(self.ruta)-1]==self.siguiente:
                                    print(self.ruta.pop())

                            else:
                                if(self.estado==PATRULLANDO):
                                    self.ruta=list(self.recorrido)
                                else:
                                    self.ruta=fase.calcular_ruta_anchura(self.siguiente,self.destino)
                            #if len(self.ruta)==0:
                            #    self.estado=PATRULLANDO
                            #else:
                            self.siguiente=self.ruta[-1] #FALLA LA OSTIA DE VECES
                        else:
                            if(self.estado==LLENDO_A_ALARMA):
                                self.estado=DEAMBULANDO
                                self.tiempobusqueda=10000
                            elif self.estado==VOLVIENDO_A_PATRULLA:
                                self.estado=PATRULLANDO
                                self.ruta=list(self.recorrido)
                                self.siguiente=self.ruta[-1]
                                self.destino=self.ruta[0]
                            else:
                                self.ruta=list(self.recorrido)
                                self.siguiente=self.ruta[-1]
                                self.destino=self.ruta[0]
                #E cualquier caso se desplaza hacia su objeticvo actal
            Debuger.anadirLinea(self.posicion,self.dest)
            self.distancia=(self.distancia[0],self.distancia[1])
            if(self.distancia)==(0,0):
                Personaje.mover(self,self.movimiento,QUIETO)
            else:
                if(abs(self.distancia[0])>abs(self.distancia[1])):
                    if(self.distancia[0]>0):
                        Personaje.mover(self,self.movimiento,DERECHA)
                    else:
                        Personaje.mover(self,self.movimiento,IZQUIERDA)
                else:
                    if(self.distancia[1]>0):
                        Personaje.mover(self,self.movimiento,ABAJO)
                    else:
                        Personaje.mover(self,self.movimiento,ARRIBA)

    def estaViendo(self,fase,pos,rango):
         direccion=0
         angulo=math.atan2(pos[0]-self.posicion[0],pos[1]-self.posicion[1])
         if(self.mirando==IZQUIERDA):
            direccion=-PI/2
         elif(self.mirando==ARRIBA):
             direccion=PI
         elif(self.mirando==DERECHA):
             direccion=PI/2
         elif(self.mirando==ABAJO):
             direccion=0
         Debuger.anadirRadio(self.posicion,direccion-rango/2,40)
         Debuger.anadirRadio(self.posicion,direccion+rango/2,40)
         if anguloEnRango(angulo,direccion,rango):#Mira si un angulo esta dentro del campo de vision con direccion direccion y rango rango (radianes todo
             return  not fase.colisionLinea(self.posicion,pos,7)
         return False

    def alarma(self,fase,nodo):
        if self.estado!=LLENDO_A_ALARMA:
            self.estado=LLENDO_A_ALARMA
        if(self.destino!=nodo):
            self.destino=nodo
            self.siguiente=fase.nodo_visible_mas_cercano(self.posicion)
            self.ruta=fase.calcular_ruta_anchura(self.siguiente,self.destino)

    def update(self,fase,tiempo):
         if self.estado==DEAMBULANDO:
             self.tiempobusqueda-=tiempo
             if(self.tiempobusqueda<0):
                 self.estado=VOLVIENDO_A_PATRULLA
                 self.siguiente=fase.nodo_visible_mas_cercano(self.posicion)
                 self.destino=self.recorrido[-1]
                 self.ruta=fase.calcular_ruta_anchura(self.siguiente,self.destino)
         if self.estado==PERSIGUIENDO and not self.visto:
             self.tiempopersecucion-=tiempo
             if self.tiempopersecucion<0 :
                 self.estado=DEAMBULANDO
                 self.tiempobusqueda=10000
         if len(self.rutalocal)>1 :
             hijo=self.rutalocal[1]
             padre=hijo.padre
             while padre is not None:
                 Debuger.anadirLinea(hijo.pos,padre.pos)
                 hijo=padre
                 padre=hijo.padre

         Personaje.update(self,fase,tiempo)
