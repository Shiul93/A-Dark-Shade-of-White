# -*- coding: utf-8 -*-

import pygame, escena
from escena import *
from personajes import *
import debuger
from mapa import *
from pygame.locals import *
from objetos import *
from Eventos import *
from nodo import *
from enemigo import *
from Enemigo2 import *
from time import *
import random

#Carga la fase, controla el scroll y las colisiones con el decorado
#LA idea es que carge la fase a paretir de un script


# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

# Los bordes de la pa15ntalla para hacer scroll horizontal
MINIMO_X_JUGADOR = 350
MAXIMO_X_JUGADOR = ANCHO_PANTALLA - MINIMO_X_JUGADOR
MINIMO_X_BORDES = 40

MINIMO_Y_JUGADOR = 275
MAXIMO_Y_JUGADOR = ALTO_PANTALLA - MINIMO_Y_JUGADOR
MINIMO_Y_BORDES = 40

SEARCH_STEP=20
RAY_STEP=10
MAX_SEARCH_DIST=1500
TIEMPO_SONIDO_ALARMA=5000
# -------------------------------------------------
# Clase Fase


class Fase(Escena):
    def __init__(self,archivoFase, director):
        #VARIABLES LOCALES DE LA FASE
        self.escena=archivoFase
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
        self.pillado=False
        self.finjuego=False
        self.nodos=[]
        self.grafo=[]
        self.tiemposonidoalarma=0

        Escena.__init__(self, director)

        #CARGA EL ARCHIVO DE FASE
        datos = GestorRecursos.CargarArchivoFaseJSON(archivoFase)
        #print(datos)

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
            self.grupoSprites.add(self.objetos[nombre])
            self.grupoSpritesDinamicos.add(self.objetos[nombre])
            self.grupoSpritesDinamicos.add(self.objetos[nombre])
            self.grupoOpacos.add(self.objetos[nombre])
        for nombre,meta in datos["Metas"].iteritems():
            self.objetos[nombre]=Meta(meta[0],pygame.Rect(meta[1][0],meta[1][1],meta[1][2],meta[1][3]))
        for nombre,puerta in datos["Puertas_pequenas"].iteritems():
            self.objetos[nombre]=Puerta_pequena(puerta[0], pygame.Rect(puerta[1][0], puerta[1][1], puerta[1][2], puerta[1][3]))
            self.grupoSprites.add(self.objetos[nombre])
            self.grupoSpritesDinamicos.add(self.objetos[nombre])
            self.grupoColisionables.add(self.objetos[nombre])
            self.grupoOpacos.add(self.objetos[nombre])
            self.grupoOpacos.add(self.objetos[nombre])
        for nombre,puerta in datos["Puertas_verticales"].iteritems():
            self.objetos[nombre]=Puerta_vertical(puerta[0], pygame.Rect(puerta[1][0], puerta[1][1], puerta[1][2], puerta[1][3]))
            self.grupoSprites.add(self.objetos[nombre])
            self.grupoSpritesDinamicos.add(self.objetos[nombre])
            self.grupoColisionables.add(self.objetos[nombre])
            self.grupoOpacos.add(self.objetos[nombre])
            self.grupoOpacos.add(self.objetos[nombre])

        for nombre,puerta in datos["Puertas_verticales_grandes"].iteritems():
            self.objetos[nombre]=Puerta_vertical_grande(puerta[0], pygame.Rect(puerta[1][0], puerta[1][1], puerta[1][2], puerta[1][3]))
            self.grupoSprites.add(self.objetos[nombre])
            self.grupoSpritesDinamicos.add(self.objetos[nombre])
            self.grupoColisionables.add(self.objetos[nombre])
            self.grupoOpacos.add(self.objetos[nombre])
            self.grupoOpacos.add(self.objetos[nombre])

        for nombre,cuadro in datos["Cuadros"].iteritems():
            self.objetos[nombre]=Cuadro(cuadro[0], pygame.Rect(cuadro[1][0], cuadro[1][1], cuadro[1][2], cuadro[1][3]))
            self.grupoSprites.add(self.objetos[nombre])
            self.grupoSpritesDinamicos.add(self.objetos[nombre])
            self.grupoColisionables.add(self.objetos[nombre])
            self.grupoOpacos.add(self.objetos[nombre])
            self.grupoOpacos.add(self.objetos[nombre])
        for nombre,diamante in datos["Diamantes"].iteritems():
            self.objetos[nombre]=Diamante(diamante[0], pygame.Rect(diamante[1][0], diamante[1][1], diamante[1][2], diamante[1][3]))
            self.grupoSprites.add(self.objetos[nombre])
            self.grupoSpritesDinamicos.add(self.objetos[nombre])
            self.grupoColisionables.add(self.objetos[nombre])


        for nombre,puerta in datos["Puertas_grandes"].iteritems():
            self.objetos[nombre]=Puerta_grande(puerta[0], pygame.Rect(puerta[1][0], puerta[1][1], puerta[1][2], puerta[1][3]))
            self.grupoSprites.add(self.objetos[nombre])
            self.grupoSpritesDinamicos.add(self.objetos[nombre])
            self.grupoColisionables.add(self.objetos[nombre])
            self.grupoOpacos.add(self.objetos[nombre])
            self.grupoOpacos.add(self.objetos[nombre])

        for nombre,luz in datos["Luces"].iteritems():
            self.objetos[nombre]=Luz(luz[0],pygame.Rect(luz[1][0],luz[1][1],luz[1][2],luz[1][3]))
            self.grupoSprites.add(self.objetos[nombre])
            self.grupoSpritesDinamicos.add(self.objetos[nombre])
            self.grupoOpacos.add(self.objetos[nombre])

        for nombre,camara in datos["Camaras"].iteritems():
            self.objetos[nombre]=Camara(camara[0],pygame.Rect(0,0,1,1),camara[1],camara[2],camara[3],camara[4])
            self.grupoSprites.add(self.objetos[nombre])
            self.grupoSpritesDinamicos.add(self.objetos[nombre])
            self.grupoOpacos.add(self.objetos[nombre])

        #print self.objetos

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
            elif tipo==PILLADO:
               self.consecuencias[nombre]=Accion(PILLADO,None,None,None)
            elif tipo==ALARMA:
               self.consecuencias[nombre]=Accion(ALARMA,self.objetos[consecuencia[1]],None,None)
            elif tipo==SONIDO:
               self.consecuencias[nombre]=Accion(SONIDO,None,None,consecuencia[1]) #si se cargarran los sonidos en el json seria self.objetos[consecuencia[1]]
        for nombre,evento in datos["Eventos"].iteritems():
            causas=[]
            consecuencias=[]
            for causa in evento[0]:
                causas.append(self.causas[causa])
            for consecuencia in evento[1]:
                consecuencias.append(self.consecuencias[consecuencia])
            self.listaeventos[nombre]=Evento(causas,consecuencias)

        self.grafo=datos['grafo']
        nodos=datos['nodos']
        self.nodos={}
        for i in range(0,len(nodos)):
            self.nodos[i]=nodos[i]


        self.enemigo=[]
        patrulla=[]
        self.grupoEnemigos=pygame.sprite.Group()
        for i in range (0,len(datos['Enemigos'])):
          self.enemigo.append(Enemigo(self.nodos,datos['grafo'],datos['Enemigos'][i]))
          self.grupoEnemigos.add(self.enemigo[i])
          self.grupoSprites.add(self.enemigo[i])
        for i in range (0,len(datos['Enemigos2'])):
          self.enemigo.append(Enemigo2(self.nodos,datos['grafo'],datos['Enemigos2'][i]))
          self.grupoEnemigos.add(self.enemigo[i])
          self.grupoSprites.add(self.enemigo[i])
        self.siguientefase=datos['Siguiente']

        for sprite in iter(self.grupoSprites):
            sprite.establecerPosicionPantalla(self.scrollx, self.scrolly)
        # Ademas, actualizamos el decorado para que se muestre una parte distinta
            self.decorado.update(self.scrollx,self.scrolly)



        self.actualizarScroll(self.jugador1)



    # Devuelve True o False según se ha tenido que desplazar el scroll
    def actualizarScrollOrdenados(self, jugador):
        actualizar=False
        # Si el jugador se encuentra más allá del borde izquierdo
        if (jugador.rect.center[0]<MINIMO_X_JUGADOR):
            desplazamiento = MINIMO_X_JUGADOR - jugador.rect.center[0]
            self.scrollx = self.scrollx - desplazamiento;
            actualizar=True; # Se ha actualizado el scroll
        elif (jugador.rect.center[0]>MAXIMO_X_JUGADOR):
            desplazamiento = jugador.rect.center[0] - MAXIMO_X_JUGADOR
            self.scrollx = self.scrollx + desplazamiento;
            actualizar= True; # Se ha actualizado el scroll
        if (jugador.rect.center[1]<MINIMO_Y_JUGADOR):
            desplazamiento = MINIMO_Y_JUGADOR - jugador.rect.center[1]
            self.scrolly = self.scrolly - desplazamiento;
            actualizar= True; # Se ha actualizado el scroll
        elif (jugador.rect.center[1]>MAXIMO_Y_JUGADOR):
            desplazamiento = jugador.rect.center[1] - MAXIMO_Y_JUGADOR
            self.scrolly = self.scrolly + desplazamiento;
            actualizar= True; # Se ha actualizado el scroll




        if self.scrollx <= 0:
                self.scrollx = 0
        elif self.scrollx + ANCHO_PANTALLA >= self.decorado.rect.right:
                self.scrollx = self.decorado.rect.right - ANCHO_PANTALLA
        if self.scrolly + ALTO_PANTALLA >= self.decorado.rect.bottom:
                self.scrolly = self.decorado.rect.bottom-ALTO_PANTALLA
        elif self.scrolly <= 0:
                self.scrolly = 0
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
        if tiempo>80: tiempo=80
        if(not self.pausa):
            self.tiemposonidoalarma-=tiempo
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
                self.pillado=True
                self.mostrarMensaje("¡¡Te han pillado!!")

            # Actualizamos el scroll
            self.actualizarScroll(self.jugador1)



    def dibujar(self, pantalla):
        #Primero las capas que no tapan a los sprites
        self.decorado.dibujar_pre(pantalla)
        # Luego los Sprites


        #Luego las capas que tapan a los sprites
        self.grupoSprites.draw(pantalla)
        self.grupoJugadores.draw(pantalla)
        self.grupoEnemigos.draw(pantalla)
        self.decorado.dibujar_post(pantalla)


        Debuger.dibujarTexto(pantalla)
        Debuger.dibujarLineas(pantalla,(self.scrollx,self.scrolly))
        if(self.haymensaje):
            self.cuadrotexto.draw(pantalla)













    def dispararAlarma(self):
        for enemigo in self.grupoEnemigos.sprites():
              enemigo.alarma(self,self.nodo_mas_cercano(self.jugador1.posicion,self.nodos))
        if self.tiemposonidoalarma<0:
            son=GestorRecursos.CargarSonido("Danger_Alarm")
            son.play()
            self.tiemposonidoalarma=TIEMPO_SONIDO_ALARMA

    def colision(self,rect):
       rectlist=self.listaRectangulosColisionables()
       collidesprite=rect.collidelist(rectlist)
       return self.decorado.colision(rect,"colisiones") or collidesprite>-1

    def colisionOculta(self,rect):
       rectlist=self.listaRectangulosOpacos()
       collidesprite=rect.collidelist(rectlist)
       return self.decorado.colision(rect,"oculto") or collidesprite>-1


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



    def colisionLinea(self,origen,destino,step,capa):
        dif=(destino[0]-origen[0],destino[1]-origen[1])
        distancia=dist(origen,destino)
        rectlist=self.listaRectangulosOpacos()
        pointlist=[]
        for i in range(0,int(distancia),step):
            punto=(int(origen[0]+dif[0]*i/distancia),int(origen[1]+dif[1]*i/distancia))
            #Debuger.anadirLinea(punto,(punto[0],punto[1]+2))
            pointlist.append(punto)
            if self.decorado.colisionPunto(punto,capa):
                return True
            else:
                for rect in rectlist:
                    if rect.collidepoint(punto):
                        return True
        return False


    # estas dos funciones las usa ahora el enemigo para volver a la ruta cuando esta "perdido"
    #deberian sustituirse por funciones equivalentes usando rutas
    def nodo_mas_cercano(self,pos,nodos):

        mindist=dist(pos,nodos.values()[0])
        minindex=0
        for clave,valor in nodos.iteritems():
            nodedist=dist(pos,valor)
            if nodedist<mindist:
                mindist=nodedist
                minindex=clave
        return minindex

    def calcular_nodos_adyacentes(self,nodo,step):
        rectangulo=pygame.Rect(0,0,step*2,step*2) #Usado para calcular las posiciones de los nodos nuevos (top,bottom,left,right)
        rectangulo.center=nodo.pos
        rectangulocolision=pygame.Rect(0,0,13,10)
        rectangulocolision.center=rectangulo.center
        nodos = []
        rectangulonuevo=rectangulocolision.copy()
        rectangulonuevo.center=rectangulo.midtop
        #Debuger.anadirLinea(rectangulocolision.topleft,rectangulonuevo.topleft)
        #Debuger.anadirLinea(rectangulocolision.topright,rectangulonuevo.topright)
        if not self.colisionLinea(rectangulonuevo.topleft,rectangulocolision.topleft,RAY_STEP,"colisiones") \
            and not self.colisionLinea(rectangulonuevo.topright,rectangulocolision.topright,RAY_STEP,"colisiones"):
            nodos.append(Nodo(rectangulo.midtop,nodo,nodo.dist + step))
        rectangulonuevo.center=rectangulo.midbottom
        #Debuger.anadirLinea(rectangulocolision.bottomleft,rectangulonuevo.bottomleft)
        #Debuger.anadirLinea(rectangulocolision.bottomright,rectangulonuevo.bottomright)
        if not self.colisionLinea(rectangulonuevo.bottomleft,rectangulocolision.bottomleft,RAY_STEP,"colisiones") \
            and not self.colisionLinea(rectangulonuevo.bottomright,rectangulocolision.bottomright,RAY_STEP,"colisiones"):
            nodos.append(Nodo(rectangulo.midbottom,nodo,nodo.dist + step))
        rectangulonuevo.center=rectangulo.midright
        #Debuger.anadirLinea(rectangulocolision.topright,rectangulonuevo.topright)
        #Debuger.anadirLinea(rectangulocolision.bottomright,rectangulonuevo.bottomright)
        if not self.colisionLinea(rectangulonuevo.topright,rectangulocolision.topright,RAY_STEP,"colisiones") \
            and not self.colisionLinea(rectangulonuevo.bottomright,rectangulocolision.bottomright,RAY_STEP,"colisiones"):
            nodos.append(Nodo(rectangulo.midright,nodo,nodo.dist + step))
        rectangulonuevo.center=rectangulo.midleft
        #Debuger.anadirLinea(rectangulocolision.topleft,rectangulonuevo.topleft)
        #Debuger.anadirLinea(rectangulocolision.bottomleft,rectangulonuevo.bottomleft)
        if not self.colisionLinea(rectangulonuevo.topleft,rectangulocolision.topleft,RAY_STEP,"colisiones") \
            and not self.colisionLinea(rectangulonuevo.bottomleft,rectangulocolision.bottomleft,RAY_STEP,"colisiones"):
            nodos.append(Nodo(rectangulo.midleft,nodo,nodo.dist + step))
        return nodos


    def calcular_ruta_anchura(self,origen,destino):#La mas sencilla a saco sin distancias ni ostias??
        visitados=[origen]
        frontera=[origen]
        ruta=[]
        distancia={}
        distancia[origen]=0
        padre={}
        padre[origen]=None
        antes=time()
        while len(frontera)>0:
            abrir=frontera.pop(0)# Con un cero es anchura, con un -1 es profundidad, con una heuristica es hillclimb, con dist+heuristica es A*
            if abrir==destino:
                anterior=padre[abrir]
                ruta.append(abrir)
                while anterior is not None:
                    ruta.append(anterior)
                    anterior=padre[anterior]
                #print "Tiempo de busqueda: "+str(time()-antes)
                return ruta
            else:
                destinos=list(self.grafo[abrir])
                for dest in destinos:
                    if(self.colisionLinea(self.nodos[abrir],self.nodos[dest],RAY_STEP,"colisiones")):
                        destinos.remove(dest)
                for nodo in destinos:
                    if not visitados.__contains__(nodo):
                        padre[nodo]=abrir
                        visitados.append(nodo)
                        frontera.append(nodo)#Añadimos los adyacentes
                        distancia[nodo]=distancia[abrir]+dist(self.nodos[abrir],self.nodos[nodo])
                    else:
                        newdist=distancia[abrir]+dist(self.nodos[abrir],self.nodos[nodo])
                        if newdist<distancia[nodo]:
                            distancia[nodo]=newdist
                            padre[nodo]=abrir
        return []

#borrrar
    def buscar_nodo_visitado2(self,nodo,visitados):
        for visitado in visitados:
            if dist(nodo.pos,visitado.pos)<2:
                return visitado
        return None

    def buscar_nodo_visitado(self,nodo,visitados):
        for visitado in visitados:
            if nodo.pos==visitado.pos:
                return visitado
        return None

    #Comprueba si un noodo local esta lo bastante cerca de alguno de los waypoints del grafo
    def comprobar_llegada_nodos(self,pos,nodos):
        for nodo,dest in nodos.items():
            if dist(pos,dest)<SEARCH_STEP: #destino encontrado, calcular ruta (PROBAR NUMEROS)
                return nodo
        return -1

    def buscar_nodo_mas_cercano(self,origen,nodos):
        nodo_origen=Nodo(origen,None,0)
        frontera=[nodo_origen]
        ruta=[]
        visitados=[nodo_origen]
        antes=time()
        while len(frontera)>0:
            siguiente_nodo=0#ANCHURA Nodo.mejor_nodo(frontera,dest) #FUNCION DE SELECCION DE NODO
            abrir = frontera.pop(siguiente_nodo)
            nodo_destino=self.comprobar_llegada_nodos(abrir.pos,nodos)
            if nodo_destino>-1 : #destino encontrado, calcular ruta (PROBAR NUMEROS)
                    anterior=abrir.padre
                    ruta.append(abrir)
                    while anterior is not None and anterior.padre is not None:
                        ruta.append(anterior)
                        anterior=anterior.padre
                    #print "Tiempo de busqueda local multiple : " + str(1000*(time()-antes)) + " ms"
                    return (nodo_destino,ruta)
            else: #seguir buscando
                if abrir.dist > MAX_SEARCH_DIST:
                    break
                for nodo in self.calcular_nodos_adyacentes(abrir,SEARCH_STEP):
                    visitado=self.buscar_nodo_visitado(nodo,visitados)
                    if visitado is not None:
                        if nodo.dist<visitado.dist:
                            self.visitado=nodo
                    else:
                        frontera.append(nodo)
                        visitados.append(nodo)
        #print "Tiempo de busqueda local multiple (sin resultado) : " + str(1000*(time()-antes)) + " ms"
        return (0,[]) #No ha encontrado nada y devuelve una lista vacia


    def calcular_ruta_local(self,origen,dest):
        nodo_origen=Nodo(origen,None,0)
        frontera=[nodo_origen]
        ruta=[]
        visitados=[nodo_origen]
        antes=time()
        while len(frontera)>0:
            siguiente_nodo=Nodo.mejor_nodo(frontera,dest) #FUNCION DE SELECCION DE NODO
            abrir = frontera.pop(siguiente_nodo)
            if dist(abrir.pos,dest)<SEARCH_STEP: #destino encontrado, calcular ruta (PROBAR NUMEROS)
                anterior=abrir.padre
                ruta.append(abrir)
                while anterior is not None and anterior.padre is not None:
                    ruta.append(anterior)
                    anterior=anterior.padre
                #print "Tiempo de busqueda local : " + str(1000*(time()-antes)) + " ms"
                return ruta
            else: #seguir buscando
                if abrir.dist > MAX_SEARCH_DIST:
                    break
                for nodo in self.calcular_nodos_adyacentes(abrir,SEARCH_STEP):
                    visitado=self.buscar_nodo_visitado(nodo,visitados)
                    if visitado is not None:
                        if nodo.dist<visitado.dist:
                            self.visitado=nodo
                    else:
                        frontera.append(nodo)
                        visitados.append(nodo)
        #print "Tiempo de busqueda local (sin resultado) : " + str(1000*(time()-antes)) + " ms"
        return [] #No ha encontrado nada y devuelve una lista vacia

    def eventos(self, lista_eventos):
        # Miramos a ver si hay algun evento de salir del programa
        for evento in lista_eventos:
            # Si se quiere salir, se le indica al director
            if evento.type == pygame.QUIT:
                self.director.salirPrograma()

        # Indicamos la acción a realizar segun la tecla pulsada para cada jugador
        teclasPulsadas = pygame.key.get_pressed()

        if(not self.pausa):
             self.jugador1.mover(teclasPulsadas, K_w, K_s, K_a, K_d,K_RCTRL,K_RSHIFT)
             action=False
             if  not teclasPulsadas[K_RETURN]:
                self.actiondropped=True
             elif self.actiondropped:
                if not self.hay_persecucion():
                    action=True
                else:
                    if (random.randint(0,100)<95):
                        self.mostrarMensaje("Está atascado!!")
                    else:
                        action = True
                self.actiondropped=False
             for evento in self.listaeventos.itervalues():
                 if evento.comprobar(self.jugador1,self,action):
                     evento.lanzar(self)
        else:
            if not teclasPulsadas[K_RETURN]:
                self.actiondropped=True
            elif self.actiondropped:
                self.pausa=False
                self.haymensaje=False
                self.actiondropped=False
                if(self.finfase):
                    if self.siguientefase == "FIN":
                        self.mostrarMensaje("Enhorabuena, has terminado el juego")
                        self.finjuego=True
                        self.finfase=False
                    else:
                        nuevafase = Fase(self.siguientefase,self.director)
                        self.director.cambiarEscena(nuevafase)
                elif(self.pillado):
                    fase=Fase(self.escena,self.director)
                    self.mostrarMensaje("¡¡Te han pillado!!")
                    self.director.cambiarEscena(fase)
                elif(self.finjuego):
                    self.director.salirEscena()

        #AQUI SE DEBERIAN COMROBAR LOS EVENTOS DEL JUEGO

    def mostrarMensaje(self,texto):
        self.cuadrotexto.establecerTexto(texto)
        self.pausa=True
        self.haymensaje=True
        self.actiondropped=False

    def hay_persecucion(self):
        for enemigo in self.enemigo:
            if enemigo.estado==PERSIGUIENDO :
                return True
        return False

    def reproducirSonido(self,sonido):#SONIDO ES UN STRING CON EL NOMBRE DEL SONIDO QUE SE DEBERA CARGAR ANTES
        return False
