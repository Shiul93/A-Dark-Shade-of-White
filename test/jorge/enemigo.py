# -*- encoding: utf-8 -*-

from personajes import *

#Estados de la IA
QUIETO=0
PATRULLANDO=1
DEAMBULANDO=2
LLENDO_A_ALARMA=3
VOLVIENDO_A_PATRULLA=4
PERSIGUIENDO=5

TIEMPO_CALCULO_RUTA=1000
TIEMPO_BUSCAR=10000
TIEMPO_PERSEGUIR=10000
TIEMPO_GIRAR=1000

DISTANIA_MAXIMA_CALCULO_RUTA=4000

RAY_STEP=23

class Enemigo(NoJugador):
    "El  guardia que da vueltas por un grafo de nodos y sabe llegar a un destino"
    def __init__(self,nodos,grafo,recorrido):
        # Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
        NoJugador.__init__(self,'Guardias.png','coordguardia.txt',  VELOCIDAD_SNIPER,  RETARDO_ANIMACION_SNIPER)
        self.visto=False
        self.estado=PATRULLANDO
        self.tiempocalculoruta=0
        self.tiempobusqueda=0
        self.tiempopersecucion=0
        self.tiempogirar=0

        self.recorrido=recorrido #recorrido de la patrulla (lista de pares)
        self.movimiento=NORMAL
        self.destino=None
        self.siguiente=None
        self.rutapatrulla=list(self.recorrido)
        self.posicion=self.rutapatrulla.pop()
        self.dest=self.posicion
        self.ruta=[]
        #self.ruta=fase.calcular_ruta_local(self.posicion,self.rutapatrulla.pop() )
        self.distancia=(0,0)
        self.movimiento = NORMAL
        # Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
    # La implementacion de la inteligencia segun este personaje particular
    def mover_cpu(self, jugador1, fase):


             #Si ve al personaje...
            if self.estaViendo(fase,jugador1.posicion,PI*3/4):
                if not self.visto: #EN EL MOMENTO EN EL QUE TE VE
                    self.visto=True
                    self.estado=PERSIGUIENDO
                    self.movimiento=CARRERA
                    self.ruta=fase.calcular_ruta_local(self.posicion,jugador1.posicion)
                    if len(self.ruta)>0:
                        self.destino=self.ruta[0]
                        self.siguiente=self.ruta[-1]
                    fase.dispararAlarma()
            else: #te ha perdido de vista
                if self.visto:
                    self.visto=False
                    self.tiempopersecucion=TIEMPO_PERSEGUIR

            if abs(self.distancia[0]+self.distancia[1])<5 : #Si llega a un nodo (eligira el siguiente segun lo que este haciendo)
                self.posicion=self.dest
                if self.siguiente==self.destino: #Si es el final de la ruta
                    if self.estado==PATRULLANDO:
                        if len(self.rutapatrulla)==0:#si le quedan puntos por visitar
                            self.rutapatrulla=list(self.recorrido)
                        self.ruta=fase.calcular_ruta_local(self.posicion,self.rutapatrulla.pop())
                        if len(self.ruta)>0:
                            self.destino=self.ruta[0]
                            self.siguiente=self.ruta[-1]
                            self.dest=self.siguiente.pos
                    elif self.estado==LLENDO_A_ALARMA:
                         self.estado=DEAMBULANDO #provisionalisimo
                         self.tiempobusqueda=TIEMPO_BUSCAR
                         self.movimiento=QUIETO
                    elif self.estado==PERSIGUIENDO:
                         self.ruta=fase.calcular_ruta_local(self.posicion,jugador1.posicion)
                         if len(self.ruta)>0:
                             self.destino=self.ruta[0]
                             self.siguiente=self.ruta.pop()
                             self.dest=self.siguiente.pos#asegurarlo
                         else:
                             self.dest=jugador1.posicion

                    elif self.estado==VOLVIENDO_A_PATRULLA:
                        self.rutapatrulla=list(self.recorrido)
                        self.ruta=fase.calcular_ruta_local(self.posicion,self.rutapatrulla.pop())
                        self.estado=PATRULLANDO
                        if len(self.ruta)>0:
                            self.destino=self.ruta[0]
                            self.siguiente=self.ruta[-1]
                            self.dest=self.siguiente.pos
                else: #Es un nodo cualquiera, coge el siguiente
                    if len(self.ruta)>0:
                        self.siguiente=self.ruta.pop()
                        self.dest=self.siguiente.pos

            self.distancia=(self.dest[0]-self.posicion[0],self.dest[1]-self.posicion[1])

            #En cualquier cas se mueve hacia el dest
            Debuger.anadirLinea(self.posicion,self.dest)
            if  self.estado==DEAMBULANDO:
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

    def alarma(self,fase,posicion):
        if self.estado!=PERSIGUIENDO and (self.estado!=LLENDO_A_ALARMA or  dist(posicion,self.destino.pos)>200):
            ruta=fase.calcular_ruta_local(self.posicion,posicion)
            if len(ruta)>0:
                self.ruta=ruta
                self.destino=self.ruta[0]
                self.siguiente=self.ruta[-1]
                self.estado=LLENDO_A_ALARMA



    def update(self,fase,tiempo):
         if self.estado==DEAMBULANDO:
             self.tiempogirar-=tiempo
             if self.tiempogirar<0:
                 self.mirando+=1
                 if(self.mirando>ARRIBA):
                     self.mirando=ABAJO
                 self.tiempogirar=TIEMPO_GIRAR
             self.tiempobusqueda-=tiempo
             if(self.tiempobusqueda<0):
                 self.estado=VOLVIENDO_A_PATRULLA
                 self.movimiento=NORMAL
                 self.ruta=fase.calcular_ruta_local(self.posicion,self.recorrido[-1])
                 if len(self.ruta)>0:
                     self.siguiente=self.ruta[-1]
                     self.destino=self.ruta[0]
         elif self.estado==PERSIGUIENDO:
             self.tiempocalculoruta-=tiempo
             if self.tiempocalculoruta<0:
                 self.ruta=fase.calcular_ruta_local(self.posicion,fase.jugador1.posicion)
                 self.tiempocalculoruta=TIEMPO_CALCULO_RUTA
                 if len(self.ruta)>0:
                     self.siguiente=self.ruta[-1]
                     self.destino=self.ruta[0]
             if not self.visto:
                self.tiempopersecucion-=tiempo
                if self.tiempopersecucion<0 :
                   self.estado=DEAMBULANDO
                   self.tiempogirar=TIEMPO_GIRAR
                   self.tiempobusqueda=TIEMPO_BUSCAR
                   self.movimiento=QUIETO


         Personaje.update(self,fase,tiempo)

         for i in range(1,len(self.ruta)) :
             hijo=self.ruta[i-1]
             padre=self.ruta[i]
             Debuger.anadirLinea(hijo.pos,padre.pos)