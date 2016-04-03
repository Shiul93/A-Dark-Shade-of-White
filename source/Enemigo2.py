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
TIEMPO_PERSEGUIR=2000
TIEMPO_GIRAR=1000
TIEMPO_COLISIONANDO=1200



RAY_STEP=10



class Enemigo2(NoJugador):
    "El  guardia que da vueltas por un grafo de nodos y sabe llegar a un destino"
    def __init__(self,nodos,grafo,recorrido):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        NoJugador.__init__(self,'guardia','guardia', VELOCIDAD_ENEMIGO, RETARDO_ANIMACION_ENEMIGO)
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
        self.tiempocolisionando=0
        self.rutalocal=[]
        self.destinolocal=None
        self.siguientelocal=None
        self.nododestino=0
        self.alarmapendiente=False
        self.nodoalarmapendiente=0
        self.estadoanterior=QUIETO
        self.soundflag = True
        # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion de la inteligencia segun este personaje particular
    def mover_cpu(self, jugador1, fase):
            self.movimiento = NORMAL
            '''
            for i in range(0,len(self.grafo)):
                ldestinos=self.grafo[i]
                for destino in ldestinos:
                    Debuger.anadirLinea(self.nodos[i],self.nodos[destino])
'''



            #ENCUENTRA AL PERSONAJE:
            if self.estaViendo(fase,jugador1.posicion,PI*3/4):

                if self.soundflag:
                    son = GestorRecursos.CargarSonido('alerta-metal-gear')
                    canal = son.play(1)
                    print canal
                    self.soundflag= False

                if not self.visto:
                    self.visto=True
                    self.estado=PERSIGUIENDO
                    self.tiempocalculoruta=TIEMPO_CALCULO_RUTA
                    self.rutalocal=fase.calcular_ruta_local(self.posicion,jugador1.posicion)
                    if len(self.rutalocal)>0:
                        self.siguientelocal=self.rutalocal[-1]
                        self.destinolocal=self.rutalocal[0]

            else: #te ha perdido de vista
                self.soundflag = True
                if self.visto:
                    self.visto=False
                    self.tiempopersecucion=5000
                    #self.rutalocal=fase.calcular_ruta_local(self.posicion,jugador1.posicion)
                    if len(self.rutalocal)>0:
                        self.siguientelocal=self.rutalocal[-1]
                        self.destinolocal=self.rutalocal[0]

            #BUSQUEDA LOCAL
            if self.estado==PERSIGUIENDO or self.estado==VOLVIENDO_A_UN_NODO:
                if self.siguientelocal is not None : #apaño provisional
                     self.dest=self.siguientelocal.pos
                     self.distancia=(self.dest[0]-self.posicion[0],self.dest[1]-self.posicion[1])
                else:
                    if self.estado==PERSIGUIENDO  :#self.distancia=(self.dest[0]-self.posicion[0],self.dest[1]-self.posicion[1])
                        self.dest=fase.jugador1.posicion
                    elif self.estado==VOLVIENDO_A_UN_NODO:
                        self.dest=self.nodos[self.nododestino]
                if abs(self.distancia[0])+abs(self.distancia[1])<5 : #Si llega a un destino (eligira el siguiente segun lo qu este haciendo)
                    if self.siguientelocal==self.destinolocal: #Si es el final de la ruta
                        if self.estado==PERSIGUIENDO : #Si esta persiguiendo recalcula y si hay nodos sigue y si no ataca directament
                                self.rutalocal=fase.calcular_ruta_local(self.posicion,jugador1.posicion)
                                if len(self.rutalocal)>0:
                                    self.destinolocal=self.rutalocal[0]
                                    self.siguientelocal=self.rutalocal.pop()
                                    self.dest=self.siguientelocal.pos#asegurarlo
                                else:
                                    self.dest=jugador1.posicion
                                    self.siguientelocal=None


                        elif self.estado==VOLVIENDO_A_UN_NODO : #SI ESTA VOLVIENDOA UN NODO (pasa a deambular)
                             if self.estadoanterior==PERSIGUIENDO or self.estadoanterior==LLENDO_A_ALARMA:
                                self.ruta=[]
                                #print "llego al nodo y ya esta lo bastante cerca del objetivo"
                                self.tiempobusqueda=TIEMPO_BUSCAR
                                self.siguiente=self.nododestino
                                self.estado=DEAMBULANDO
                             else:
                                self.siguiente=self.nododestino
                                destino=self.recorrido[-1]
                                ruta=fase.calcular_ruta_anchura(self.siguiente,self.destino)
                                if len(ruta)>0 :
                                    self.estado=VOLVIENDO_A_PATRULLA
                                    self.ruta=ruta
                                    self.destino=destino
                                else:
                                    self.ruta=[]
                                #print "llego al nodo y ya esta lo bastante cerca del objetivo"
                                    self.tiempobusqueda=TIEMPO_BUSCAR
                                    self.siguiente=self.nododestino
                                    self.estado=DEAMBULANDO
                            #self.dest=self.nodos[fase.nodo_mas_cercano(self.posicion,self.nodos)]
                            #self.distancia=(self.dest[0]-self.posicion[0],self.dest[1]-self.posicion[1])

                    else: #SI no es el nodo destino
                        if len(self.rutalocal)>0: #Si quedan nodos en la ruta
                            self.destinolocal=self.rutalocal[0]
                            self.siguientelocal=self.rutalocal.pop()
                            self.dest=self.siguientelocal.pos#asegurarlo
                            self.distancia=(self.dest[0]-self.posicion[0],self.dest[1]-self.posicion[1])
                        else: #Si no hay mas nodos pero no era el destino  ( NO ESTA BIEN DIRIA YO)
                            #self.rutalocal=fase.calcular_ruta_local(self.posicion,self.nodos[self.nododestino])
                            if len(self.rutalocal)>0:
                                self.destinolocal=self.rutalocal[0]
                                self.siguientelocal=self.rutalocal.pop()
                                self.dest=self.siguientelocal.pos#asegurarlo
                            else:
                                self.dest=self.nodos[self.nododestino]
                                self.siguientelocal=None
                                if dist(self.posicion,self.nodos[self.nododestino]) < 3:
                                     self.estado=DEAMBULANDO
                                     self.tiempobusqueda=TIEMPO_BUSCAR
                                     self.siguiente=self.nododestino
                                     if self.alarmapendiente:
                                         self.alarma(fase,self.nodoalarmapendiente)
                                         self.alarmapendiente=False
            #BUSQUEDA EN EL GRAFO

                self.distancia=(self.dest[0]-self.posicion[0],self.dest[1]-self.posicion[1])
            else:

                self.dest=self.nodos[self.siguiente]
                self.distancia=(self.dest[0]-self.posicion[0],self.dest[1]-self.posicion[1])

                if abs(self.distancia[0])+abs(self.distancia[1])<5 : #Si llega a un destino (eligira el siguiente segun lo qu este haciendo)
                    destinos=list(self.grafo[self.siguiente])
                    for destino in destinos:
                        if(fase.colisionLinea(self.posicion,self.nodos[destino],RAY_STEP,"colisiones")):
                            destinos.remove(destino)
                    if(self.estado==DEAMBULANDO):
                        self.siguiente=destinos[randint(0,len(destinos)-1)]
                    elif(self.estado==LLENDO_A_ALARMA or self.estado==PATRULLANDO or self.estado==VOLVIENDO_A_PATRULLA):
                        if self.destino!=self.siguiente or len(self.ruta)>1:
                            if len(self.ruta)>0 and self.ruta[len(self.ruta)-1]==self.siguiente:
                                    self.ruta.pop()
                            else:
                                if(self.estado==PATRULLANDO):
                                    self.ruta=list(self.recorrido)
                                else:
                                    self.ruta=fase.calcular_ruta_anchura(self.siguiente,self.destino)
                            if len(self.ruta)>0:
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
            if self.estado==LLENDO_A_ALARMA or self.estado==PERSIGUIENDO:
                self.movimiento=CARRERA
            else:
                self.movimiento=NORMAL

            #Debuger.anadirLinea(self.posicion,self.dest)
            self.distancia=(self.distancia[0],self.distancia[1])
            if abs(self.distancia[0])+abs(self.distancia[1])<4:
                Personaje.mover(self,QUIETO,self.mirando)
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

            '''
            Debuger.anadirTextoDebug("Estado : " + str(self.estado))
            Debuger.anadirTextoDebug("Colision : " + str(self.colision))
            Debuger.anadirTextoDebug("Visto : " + str(self.visto))


            Debuger.anadirTextoDebug(("Destino : "+ str(self.destino)))
            Debuger.anadirTextoDebug(("posicion : "+ str(self.posicion)))
            Debuger.anadirTextoDebug(("dest : "+ str(self.dest)))
            Debuger.anadirTextoDebug(("dist : "+ str(self.distancia)))

            Debuger.anadirTextoDebug(("Siguiente : "+ str(self.siguiente)))
            Debuger.anadirTextoDebug(("nododestino : "+ str(self.nododestino)))
            Debuger.anadirTextoDebug(("ruta : "+ str(self.ruta)))
'''


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
         #Debuger.anadirRadio(self.posicion,direccion-rango/2,40)
         #Debuger.anadirRadio(self.posicion,direccion+rango/2,40)
         if anguloEnRango(angulo,direccion,rango):#Mira si un angulo esta dentro del campo de vision con direccion direccion y rango rango (radianes todo
             return  not fase.colisionLinea(self.posicion,pos,RAY_STEP,"opacidad")
         return False

    def alarma(self,fase,nodo):
        if self.estado==PERSIGUIENDO or self.estado==VOLVIENDO_A_UN_NODO:
            self.alarmapendiente=True
            self.nodoalarmapendiente=nodo
        else:
            if(self.nodoalarmapendiente!=nodo):
                self.nodoalarmapendiente=nodo
                #siguiente sigue siendo el mismo
                #tambien puoedo usar la alarma pendiente
                rutaalarma=fase.calcular_ruta_anchura(self.siguiente,self.nodoalarmapendiente)
                if len(rutaalarma)>0:
                    self.destino=self.nodoalarmapendiente
                    self.ruta=rutaalarma
                    self.estado=LLENDO_A_ALARMA


    def update(self,fase,tiempo):
         if self.estado==DEAMBULANDO:
             self.tiempobusqueda-=tiempo
             if(self.tiempobusqueda<0):
                 #self.siguiente=fase.nodo_mas_cercano(self.posicion,self.nodos)
                 destino=self.recorrido[-1]
                 ruta=fase.calcular_ruta_anchura(self.siguiente,self.destino)
                 if len(ruta)>0:
                    self.estado=VOLVIENDO_A_PATRULLA
                    self.ruta=ruta
                    self.destino=destino
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
                     (self.nododestino,self.rutalocal)=fase.buscar_nodo_mas_cercano(self.posicion,self.nodos)
                     if len(self.rutalocal)>0:
                        self.siguientelocal=self.rutalocal[-1]
                        self.destinolocal=self.rutalocal[0]

                     self.estadoanterior=self.estado
                     self.estado=VOLVIENDO_A_UN_NODO
                     #self.rutalocal=fase.calcular_ruta_local(self.posicion,self.nodos[self.nododestino])


         if self.colision:
             self.tiempocolisionando-=tiempo
             if self.tiempocolisionando<0:
                 self.tiempocolisionando=TIEMPO_COLISIONANDO
                 self.estadoanterior=self.estado
                 self.estado=VOLVIENDO_A_UN_NODO
                 (self.nododestino,self.rutalocal)=fase.buscar_nodo_mas_cercano(self.posicion,self.nodos)
                 #self.nododestino=fase.nodo_mas_cercano(self.posicion,self.nodos)
                 #self.rutalocal=fase.calcular_ruta_local(self.posicion,self.nodos[self.nododestino])
                 if len(self.rutalocal)>0:
                        self.siguientelocal=self.rutalocal[-1]
                        self.destinolocal=self.rutalocal[0]

         else:
             self.tiempocolisionando=TIEMPO_COLISIONANDO
         '''
         if len(self.rutalocal)>1 :
             hijo=self.rutalocal[1]
             padre=hijo.padre
             while padre is not None:
                 Debuger.anadirLinea(hijo.pos,padre.pos)
                 hijo=padre
                 padre=hijo.padre
'''
         Personaje.update(self,fase,tiempo)
