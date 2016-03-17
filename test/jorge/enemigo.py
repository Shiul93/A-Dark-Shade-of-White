# -*- encoding: utf-8 -*-

from personajes import *

class Enemigo(NoJugador):
    "El  guardia que da vueltas por un grafo de nodos y sabe llegar a un destino"
    def __init__(self,nodos,grafo,recorrido):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        NoJugador.__init__(self,'Guardias.png','coordguardia.txt',  VELOCIDAD_SNIPER,  RETARDO_ANIMACION_SNIPER)
        self.visto=False
        self.estado=PATRULLANDO
        self.tiempobusqueda=0
        self.tiempopersecucion=0
        self.rutalocal=[]
        # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion de la inteligencia segun este personaje particular
    def mover_cpu(self, jugador1, fase):
            self.movimiento = NORMAL
            '''
            Debuger.anadirTextoDebug("Ruta : "+ str(self.ruta))
            Debuger.anadirTextoDebug("Estado : " + str(self.estado))
            Debuger.anadirTextoDebug(("Destino : "+ str(self.destino)))
            Debuger.anadirTextoDebug(("Siguiente : "+ str(self.siguiente)))
            Debuger.anadirTextoDebug(("PosSiguiente : "+ str(self.nodos[self.siguiente])))
            Debuger.anadirTextoDebug(("posicion : "+ str(self.posicion)))
            '''
             #Si ve al personaje...


            if self.estaViendo(fase,jugador1.posicion,PI*3/4):
                if not self.visto:
                    self.visto=True
                    self.estado=PERSIGUIENDO
                    self.rutalocal=fase.calcular_ruta_local(self.posicion,jugador1.posicion)
                    if len(self.rutalocal)>0:
                        self.destinolocal=self.rutalocal[-1]
            else: #te ha perdido de vista
                if self.visto:
                    self.visto=False
                    self.tiempopersecucion=5000

            if self.estado==PERSIGUIENDO:
                self.dest=self.rutalocal[-1].pos
                self.distancia=(self.dest[0]-self.posicion[0],self.dest[1]-self.posicion[1])
                if abs(self.distancia[0]+self.distancia[1])<2 : #Si llega a un destino (eligira el siguiente segun lo qu este haciendo)
                    self.rutalocal=fase.calcular_ruta_local(self.posicion,jugador1.posicion)
                    if len(self.rutalocal)>0:
                        self.destinolocal=self.rutalocal[-1]
                        self.rutalocal.pop()
                        self.dest=self.rutalocal[-1].pos#asegurarlo
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
                 self.tiempobusqueda=1000
         Personaje.update(self,fase,tiempo)
