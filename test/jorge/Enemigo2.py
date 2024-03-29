# -*- coding: utf-8 -*-
from personajes import *

#Estados de la IA
QUIETO=0
PATRULLANDO=1
DEAMBULANDO=2
LLENDO_A_ALARMA=3
VOLVIENDO_A_PATRULLA=4
PERSIGUIENDO=5
VOLVIENDO_A_UN_NODO=6

TIEMPO_CALCULO_RUTA=1000
TIEMPO_BUSCAR=10000
TIEMPO_PERSEGUIR=10000
TIEMPO_GIRAR=1000

DISTANIA_MAXIMA_CALCULO_RUTA=1000

RAY_STEP=23



class Enemigo2(NoJugador):
    "El  guardia que da vueltas por un grafo de nodos y sabe llegar a un destino"
    def __init__(self,nodos,grafo,recorrido):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        NoJugador.__init__(self,'Guardias.png','coordguardia.txt',  VELOCIDAD_SNIPER,  RETARDO_ANIMACION_SNIPER)
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
        self.tiempocalculoruta=0
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

            Debuger.anadirTextoDebug("Ruta : "+ str(self.rutalocal))
            Debuger.anadirTextoDebug("Estado : " + str(self.estado))
            Debuger.anadirTextoDebug(("Destino : "+ str(self.destinolocal)))
            Debuger.anadirTextoDebug(("Siguiente : "+ str(self.siguientelocal)))
            Debuger.anadirTextoDebug(("posicion : "+ str(self.posicion)))

            #ENCUENTRA AL PERSONAJE:
            if self.estaViendo(fase,jugador1.posicion,PI*3/4):
                if not self.visto:
                    self.visto=True
                    self.estado=PERSIGUIENDO
                    self.tiempocalculoruta=TIEMPO_CALCULO_RUTA
                    self.rutalocal=fase.calcular_ruta_local(self.posicion,jugador1.posicion)
                    if len(self.rutalocal)>0:
                        self.siguientelocal=self.rutalocal[-1]
                        self.destinolocal=self.rutalocal[0]
                    else :
                        print "sin ruta"
            else: #te ha perdido de vista
                if self.visto:
                    self.visto=False
                    self.tiempopersecucion=5000


            #BUSQUEDA LOCAL
            if self.estado==PERSIGUIENDO or self.estado==VOLVIENDO_A_UN_NODO:
                if self.siguientelocal is not None : #apaño provisional
                     self.dest=self.siguientelocal.pos
                else:
                    print "sin ruta"
                self.distancia=(self.dest[0]-self.posicion[0],self.dest[1]-self.posicion[1])
                if abs(self.distancia[0]+self.distancia[1])<2 : #Si llega a un destino (eligira el siguiente segun lo qu este haciendo)
                    if self.siguientelocal==self.destinolocal: #Si es el final de la ruta
                        if(self.estado==PERSIGUIENDO): #Si esta persiguiendo recalcula y si hay nodos sigue y si no ataca directamente
                            self.rutalocal=fase.calcular_ruta_local(self.posicion,jugador1.posicion)
                            if len(self.rutalocal)>0:
                                self.destinolocal=self.rutalocal[0]
                                self.siguientelocal=self.rutalocal.pop()
                                self.dest=self.siguientelocal.pos#asegurarlo
                            else:
                                self.dest=jugador1.posicion
                        else: #SI ESTA VOLVIENDOA UN NODO (pasa a deambular)
                            self.estado=DEAMBULANDO
                            self.tiempobusqueda=TIEMPO_BUSCAR
                    else: #SI no es el nodo destino
                        if len(self.rutalocal)>0: #Si quedan nodos en la ruta
                            self.destinolocal=self.rutalocal[0]
                            self.siguientelocal=self.rutalocal.pop()
                            self.dest=self.siguientelocal.pos#asegurarlo
                            self.distancia=(self.dest[0]-self.posicion[0],self.dest[1]-self.posicion[1])
                        else: #Si no hay mas nodos pero no era el destino  ( NO ESTA BIEN DIRIA YO)
                            self.dest=jugador1.posicion
                            self.distancia=(self.dest[0]-self.posicion[0],self.dest[1]-self.posicion[1])
            #BUSQUEDA EN EL GRAFO
            else:

                self.dest=self.nodos[self.siguiente]
                self.distancia=(self.dest[0]-self.posicion[0],self.dest[1]-self.posicion[1])

                if abs(self.distancia[0]+self.distancia[1])<2 : #Si llega a un destino (eligira el siguiente segun lo qu este haciendo)
                    destinos=list(self.grafo[self.siguiente])
                    for destino in destinos:
                        if(fase.colisionLinea(self.posicion,self.nodos[destino],RAY_STEP,"colisiones")):
                            destinos.remove(destino)
                    if(self.estado==DEAMBULANDO):
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
                            if len(self.ruta)==0:
                                #self.estado=VOLVIENDO_A_UN_NODO
                                print "sin ruta"
                            else:
                                self.siguiente=self.ruta[-1]
                            #     self.rutalocal=fase.calcular_ruta_local(self.posicion,fase.nodo_mas_cercano(self.posicion,self.nodos))
                            #     if len(self.rutalocal)>0:
                            #        self.siguientelocal=self.rutalocal[-1]
                            #        self.destinolocal=self.rutalocal[0]

                        else:
                            if(self.estado==LLENDO_A_ALARMA):
                                self.estado=DEAMBULANDO
                                self.tiempobusqueda=TIEMPO_BUSCAR
                            elif self.estado==VOLVIENDO_A_PATRULLA:
                                self.estado=PATRULLANDO
                                self.ruta=list(self.recorrido)
                                self.siguiente=self.ruta[-1]
                                self.destino=self.ruta[0]
                            else:
                                self.ruta=list(self.recorrido)
                                self.siguiente=self.ruta[-1]
                                self.destino=self.ruta[0]

                #E cualquier caso se desplaza hacia su objeticvo actal(BIEN)

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
             return  not fase.colisionLinea(self.posicion,pos,RAY_STEP,"opacidad")
         return False

    def alarma(self,fase,nodo):
        if self.estado==PERSIGUIENDO or self.estado==VOLVIENDO_A_UN_NODO:
            self.alarmapendiente=True
            self.nodoalarmapendiente=nodo
        elif self.estado==PATRULLANDO or self.estado==VOLVIENDO_A_PATRULLA:
            self.estado=LLENDO_A_ALARMA
            if(self.destino!=nodo):
                self.destino=nodo
                #siguiente sigue siendo el mismo
                #tambien puoedo usar la alarma pendiente
                self.ruta=fase.calcular_ruta_anchura(self.siguiente,self.destino)


    def update(self,fase,tiempo):
         if self.estado==DEAMBULANDO:
             self.tiempobusqueda-=tiempo
             if(self.tiempobusqueda<0):
                 self.estado=VOLVIENDO_A_PATRULLA
                 self.siguiente=fase.nodo_mas_cercano(self.posicion,self.nodos)
                 self.destino=self.recorrido[-1]
                 self.ruta=fase.calcular_ruta_anchura(self.siguiente,self.destino)
         if self.estado==PERSIGUIENDO:
             self.tiempocalculoruta-=tiempo
             if self.tiempocalculoruta<0:
                 self.rutalocal=fase.calcular_ruta_local(self.posicion,fase.jugador1.posicion)
                 self.tiempocalculoruta=TIEMPO_CALCULO_RUTA
                 if len(self.rutalocal)>0:
                     self.siguientelocal=self.rutalocal[-1]
                     self.destinolocal=self.rutalocal[0]
             if not self.visto:
                 self.tiempopersecucion-=tiempo
                 if self.tiempopersecucion<0 :
                     self.estado=VOLVIENDO_A_UN_NODO
                     self.rutalocal=fase.calcular_ruta_local(self.posicion,self.nodos[fase.nodo_mas_cercano(self.posicion,self.nodos)])
                     if len(self.rutalocal)>0:
                            self.siguientelocal=self.rutalocal[-1]
                            self.destinolocal=self.rutalocal[0]
                     else:
                         print sin
         Debuger.anadirTextoDebug("ruta: "+ str(self.ruta))
         Debuger.anadirTextoDebug("rutalocal: "+ str(self.rutalocal))

         #DIbujo de ruta local (BORRAR)
         if len(self.rutalocal)>1 :
             hijo=self.rutalocal[1]
             padre=hijo.padre
             while padre is not None:
                 Debuger.anadirLinea(hijo.pos,padre.pos)
                 hijo=padre
                 padre=hijo.padre

         Personaje.update(self,fase,tiempo)
