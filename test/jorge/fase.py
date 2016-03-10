# -*- coding: utf-8 -*-

import pygame, escena
from escena import *
from personajes import *
import debuger
from mapa import *
from pygame.locals import *
from objetos import *
from Eventos import *


#Carga la fase, controla el scroll y las colisiones con el decorado
#LA idea es que carge la fase a paretir de un script


# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

# Los bordes de la pantalla para hacer scroll horizontal
MINIMO_X_JUGADOR = 150
MAXIMO_X_JUGADOR = ANCHO_PANTALLA - MINIMO_X_JUGADOR


MINIMO_Y_JUGADOR = 150
MAXIMO_Y_JUGADOR = ALTO_PANTALLA - MINIMO_Y_JUGADOR
# -------------------------------------------------
# Clase Fase


class Fase(Escena):
    def __init__(self,archivoFase, director):
        #VARIABLES LOCALES DE LA FASE
        self.scrollx = 0
        self.scrolly = 0
        self.pausa=False
        self.haymensaje=False
        self.actiondropped=True
        self.grupoSpritesDinamicos = pygame.sprite.Group()
        self.grupoColisionables = pygame.sprite.Group()
        self.grupoJugadores =pygame.sprite.Group()
        self.grupoSprites=pygame.sprite.Group()
        self.grupoEnemigos = pygame.sprite.Group()
        self.grupoOpacos=pygame.sprite.Group()
        self.objetos={}
        self.causas={}
        self.consecuencias={}
        self.listaeventos={}
        self.cuadrotexto=CuadroTexto()
        self.finfase=False
        self.nodos=[]
        self.grafo=[]

        Escena.__init__(self, director)

        #CARGA EL ARCHIVO DE FASE
        datos = GestorRecursos.CargarArchivoFaseJSON(archivoFase)
        print(datos)

        # Creamos el decorado
        self.decorado = Mapa(datos['mapa'])

        # Creamos los sprites de los jugadores
        self.jugador1 = Jugador()
        self.jugador1.establecerPosicion((datos['pos_inicial'][0],datos['pos_inicial'][1]))
        self.grupoSprites.add(self.jugador1)
        self.grupoJugadores.add(self.jugador1)


        #Cargamos los objetos
        for nombre,boton in datos["Interruptores"].iteritems():
            self.objetos[nombre]=Interruptor(boton[0], pygame.Rect(boton[1][0], boton[1][1], boton[1][2], boton[1][3]))
            self.grupoSprites.add(self.objetos[nombre]) #(NO SE PORQUE NO)
        for nombre,meta in datos["Metas"].iteritems():
            self.objetos[nombre]=Meta(meta[0],pygame.Rect(meta[1][0],meta[1][1],meta[1][2],meta[1][3]))
        for nombre,puerta in datos["Puertas"].iteritems():
            self.objetos[nombre]=Puerta_pequena(puerta[0], pygame.Rect(puerta[1][0], puerta[1][1], puerta[1][2], puerta[1][3]))
            self.grupoSprites.add(self.objetos[nombre]) #(NO SE PORQUE NO)
            self.grupoSpritesDinamicos.add(self.objetos[nombre])
            self.grupoColisionables.add(self.objetos[nombre])
            self.grupoOpacos.add(self.objetos[nombre])

        for nombre,luz in datos["Luces"].iteritems():
            self.objetos[nombre]=Luz(luz[0],pygame.Rect(luz[1][0],luz[1][1],luz[1][2],luz[1][3]))
            self.grupoSprites.add(self.objetos[nombre])
            self.grupoSpritesDinamicos.add(self.objetos[nombre])
            self.grupoOpacos.add(self.objetos[nombre])

        print self.objetos

        for nombre,causa in datos["Causas"].iteritems():
            self.causas[nombre]=Causa(DiccCausas[causa[0]],self.objetos[causa[1]])

        for nombre,consecuencia in datos["Consecuencias"].iteritems():
            tipo=DiccConsecuencias[consecuencia[0]]
            if tipo==CAMBIAR:
               self.consecuencias[nombre]=Accion(CAMBIAR,self.objetos[consecuencia[1]],"",None)
            elif tipo==MENSAJE:
               self.consecuencias[nombre]=Accion(MENSAJE,None,consecuencia[1],None)
            elif tipo==FIN:
               self.consecuencias[nombre]=Accion(FIN,None,None,None)

        for nombre,evento in datos["Eventos"].iteritems():
            causas=[]
            consecuencias=[]
            for causa in evento[0]:
                causas.append(self.causas[causa])
            for consecuencia in evento[1]:
                consecuencias.append(self.consecuencias[consecuencia])
            self.listaeventos[nombre]=Evento(causas,consecuencias)

        self.grafo=datos['grafo']
        self.nodos=datos['nodos']
        enemigo=[]
        patrulla=[]
        self.grupoEnemigos=pygame.sprite.Group()
        for i in range (0,len(datos['Snipers'])):
          enemigo.append(Guardia(datos['nodos'],datos['grafo'],datos['Snipers'][i]))
          self.grupoEnemigos.add(enemigo[i])
          self.grupoSprites.add(enemigo[i])
        for i in range (0,len(datos['Patrullas'])):
          patrulla.append(Patrulla(datos['nodos'],datos['grafo'],datos['Patrullas'][i]))
          self.grupoEnemigos.add(patrulla[i])
          self.grupoSprites.add(patrulla[i])

        print self.calcular_ruta_anchura(1,32)


        
    # Devuelve True o False según se ha tenido que desplazar el scroll
    def actualizarScrollOrdenados(self, jugador):
        actualizar=False
        # Si el jugador se encuentra más allá del borde izquierdo
        if (jugador.rect.left<MINIMO_X_JUGADOR):
            desplazamiento = MINIMO_X_JUGADOR - jugador.rect.left
            if self.scrollx <= 0:
                self.scrollx = 0
                # En su lugar, colocamos al jugador que esté más a la izquierda a la izquierda de todo
                jugador.establecerPosicion((MINIMO_X_JUGADOR, jugador.posicion[1]))
             # Si no, se puede hacer scroll a la izquierda
            else:
                # Calculamos el nivel de scroll actual: el anterior - desplazamiento
                #  (desplazamos a la izquierda)
                self.scrollx = self.scrollx - desplazamiento;

                actualizar=True; # Se ha actualizado el scroll

        # Si el jugador  se encuentra más allá del borde derecho
        elif (jugador.rect.right>MAXIMO_X_JUGADOR):

            # Se calcula cuantos pixeles esta fuera del borde
            desplazamiento = jugador.rect.right - MAXIMO_X_JUGADOR

            # Si el escenario ya está a la derecha del todo, no lo movemos mas
            if self.scrollx + ANCHO_PANTALLA >= self.decorado.rect.right:
                self.scrollx = self.decorado.rect.right - ANCHO_PANTALLA
                # En su lugar, colocamos al jugador a la derecha de todo
                jugador.establecerPosicion((self.scrollx+MAXIMO_X_JUGADOR-jugador.rect.width, jugador.posicion[1]))
            else:
                 # Calculamos el nivel de scroll actual: el anterior + desplazamiento
                #  (desplazamos a la derecha)
                self.scrollx = self.scrollx + desplazamiento;
                actualizar= True; # Se ha actualizado el scroll

        if (jugador.rect.top<MINIMO_Y_JUGADOR):
            desplazamiento = MINIMO_Y_JUGADOR - jugador.rect.top

            # Si el escenario ya está arriba del todo, no lo movemos mas
            if self.scrolly <= 0:
                self.scrolly = 0
                # En su lugar, colocamos al jugador arriba de todo
                jugador.establecerPosicion((jugador.posicion[0],MINIMO_Y_JUGADOR+jugador.rect.height))
             # Si no, se puede hacer scroll a la arriba
            else:
                # Calculamos el nivel de scroll actual: el anterior - desplazamiento
                #  (desplazamos ariba)
                self.scrolly = self.scrolly - desplazamiento;
                actualizar= True; # Se ha actualizado el scroll
        elif (jugador.rect.bottom>MAXIMO_Y_JUGADOR):
            desplazamiento = jugador.rect.bottom - MAXIMO_Y_JUGADOR

            # Si el escenario ya está abajo del todo, no lo movemos mas
            if self.scrolly + ALTO_PANTALLA >= self.decorado.rect.bottom:
                self.scrolly = self.decorado.rect.bottom-ALTO_PANTALLA
                # En su lugar, colocamos al jugador abajo de todo
                jugador.establecerPosicion((jugador.posicion[0],self.scrolly+MAXIMO_Y_JUGADOR))
             # Si no, se puede hacer scroll abajo
            else:
                # Calculamos el nivel de scroll actual: el anterior - desplazamiento
                #  (desplazamos aabajo)
                self.scrolly = self.scrolly + desplazamiento;
                actualizar=True # Se ha actualizado el scroll
        # Si el jugador están entre los dos límites de la pantalla, no se hace nada
        return actualizar


    def actualizarScroll(self, jugador1):
        # se mira si hay que actualizar el scroll
        cambioScroll = self.actualizarScrollOrdenados(jugador1)
        # Si se cambio el scroll, se desplazan todos los Sprites y el decorado
        if cambioScroll:
            # Actualizamos la posición en pantalla de todos los Sprites según el scroll actual
            for sprite in iter(self.grupoSprites):
                sprite.establecerPosicionPantalla(self.scrollx, self.scrolly)
        # Ademas, actualizamos el decorado para que se muestre una parte distinta
            self.decorado.update(self.scrollx,self.scrolly)


    # Se actualiza el decorado, realizando las siguientes acciones:
    #  Se indica para los personajes no jugadores qué movimiento desean realizar según su IA
    #  Se mueven los sprites dinámicos, todos a la vez
    #  Se comprueba si hay colision entre algun jugador y algun enemigo
    #  Se comprueba si algún jugador ha salido de la pantalla, y se actualiza el scroll en consecuencia
    #     Actualizar el scroll implica tener que desplazar todos los sprites por pantalla
    #  Se actualiza la posicion del sol y el color del cielo
    def update(self, tiempo):
        if(not self.pausa):
            Debuger.anadirTextoDebug("FPS: "+str(int(1000/tiempo)))
        # Primero, se indican las acciones que van a hacer los enemigos segun como esten los jugadores
            for enemigo in iter(self.grupoEnemigos):
                enemigo.mover_cpu(self.jugador1,self)
            #self.grupoJugadores.update(self,tiempo)
            self.jugador1.update(self,tiempo)
            #self.grupoEnemigos.update(self,tiempo) provisionalmente 1 a 1
            for enemigo in self.grupoEnemigos.sprites():
                enemigo.update(self,tiempo)
            self.grupoSpritesDinamicos.update(tiempo)
            if pygame.sprite.groupcollide(self.grupoJugadores, self.grupoEnemigos, False, False)!={}:
                self.director.salirEscena()

            # Actualizamos el scroll
            self.actualizarScroll(self.jugador1)
  

        
    def dibujar(self, pantalla):
        #Primero las capas que no tapan a los sprites
        self.decorado.dibujar_pre(pantalla)
        # Luego los Sprites
        self.grupoSprites.draw(pantalla)
        #Luego las capas que tapan a los sprites
        self.decorado.dibujar_post(pantalla)

        Debuger.anadirRectangulo(self.objetos["boton1"].area)
        Debuger.anadirRectangulo(self.objetos["puerta1"].area)
        Debuger.anadirRectangulo(self.objetos["meta"].area)



        Debuger.dibujarTexto(pantalla)
        Debuger.dibujarLineas(pantalla,(self.scrollx,self.scrolly))
        if(self.haymensaje):
            self.cuadrotexto.draw(pantalla)

    def colision(self,rect):
       rectlist=self.listaRectangulosColisionables()
       collidesprite=rect.collidelist(rectlist)
       return self.decorado.colision(rect) or collidesprite>-1


    def listaRectangulosColisionables(self):
       rectlist=[]
       for sprite in self.grupoColisionables.sprites():
           if not sprite.estado:
               rectlist.append(sprite.pos_inicial)
       return rectlist

    def listaRectangulosOpacos(self):
       rectlist=[]
       for sprite in self.grupoOpacos.sprites():
           if not sprite.estado:
               rectlist.append(sprite.pos_inicial)
       return rectlist


    def colisionLinea(self,origen,destino,step,offset=(0,0)):
        dif=(destino[0]-origen[0],destino[1]-origen[1])
        distancia=dist(origen,destino)
        rectlist=self.listaRectangulosOpacos()
        pointlist=[]
        for i in range(0,int(distancia),step):
            punto=(int(origen[0]+offset[0]+dif[0]*i/distancia),int(origen[1]+offset[1]+dif[1]*i/distancia))
            Debuger.anadirLinea(punto,(punto[0],punto[1]+2))
            pointlist.append(punto)
            if self.decorado.colisionPunto(punto):
                return True
            else:
                for rect in rectlist:
                    if rect.collidepoint(punto):
                        return True
        return False

    def nodo_mas_cercano(self,pos,nodos):
        mindist=dist(pos,nodos.values()[0])
        minindex=0
        for clave,valor in nodos.iteritems():
            nodedist=dist(pos,valor)
            if nodedist<mindist:
                mindist=nodedist
                minindex=clave
        return minindex


    def nodo_visible_mas_cercano(self,pos):
        nodos={}
        for i in range(0,len(self.nodos)):
            nodos[i]=self.nodos[i]
        nodo_mas_cercano=self.nodo_mas_cercano(pos,nodos)
        while len(nodos)>1:
            if not self.colisionLinea(pos,nodos[nodo_mas_cercano],7,OFFSET):
                return nodo_mas_cercano
            else:
                del(nodos[nodo_mas_cercano])
                nodo_mas_cercano=self.nodo_mas_cercano(pos,nodos)
        return 0

    def calcular_ruta_anchura(self,origen,destino):#La mas sencilla a saco sin distancias ni ostias??
        visitados=[origen]
        frontera=[origen]
        ruta=[destino]
        padre={}
        padre[origen]=None
        while len(frontera)>0:
            abrir=frontera.pop()#El ultimo por defecto(profundidad?)
            print("abriendo"+str(self.nodos[abrir]))
            if abrir==destino:
                anterior=padre[abrir]
                while anterior is not None:
                    ruta.append(anterior)
                    anterior=padre[anterior]
                return ruta
            else:
                for nodo in self.grafo[abrir]:
                    if not visitados.__contains__(nodo):
                        padre[nodo]=abrir
                        visitados.append(nodo)
                        frontera.append(nodo)#Añadimos los adyacentes
        return ruta




    def eventos(self, lista_eventos):
        # Miramos a ver si hay algun evento de salir del programa
        for evento in lista_eventos:
            # Si se quiere salir, se le indica al director
            if evento.type == pygame.QUIT:
                self.director.salirPrograma()

        # Indicamos la acción a realizar segun la tecla pulsada para cada jugador
        teclasPulsadas = pygame.key.get_pressed()

        if(not self.pausa):
             self.jugador1.mover(teclasPulsadas, K_UP, K_DOWN, K_LEFT, K_RIGHT,K_RCTRL,K_RSHIFT)
             action=False
             if  not teclasPulsadas[K_RETURN]:
                self.actiondropped=True
             elif self.actiondropped:
                action=True
             for evento in self.listaeventos.itervalues():
                 if evento.comprobar(self.jugador1,action):
                     evento.lanzar(self)
        else:
            if not teclasPulsadas[K_RETURN]:
                self.actiondropped=True
            elif self.actiondropped:
                self.pausa=False
                self.haymensaje=False
                self.actiondropped=False
                if(self.finfase):
                    nuevafase = Fase('fase2.json',self.director)
                    self.director.apilarEscena(nuevafase)


        #AQUI SE DEBERIAN COMROBAR LOS EVENTOS DEL JUEGO

    def mostrarMensaje(self,texto):
        self.cuadrotexto.establecerTexto(texto)
        self.pausa=True
        self.haymensaje=True
        self.actiondropped=False