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
MINIMO_X_JUGADOR = 50
MAXIMO_X_JUGADOR = ANCHO_PANTALLA - MINIMO_X_JUGADOR


MINIMO_Y_JUGADOR = 50
MAXIMO_Y_JUGADOR = ALTO_PANTALLA - MINIMO_Y_JUGADOR
# -------------------------------------------------
# Clase Fase


class Fase(Escena):
    def __init__(self,archivoFase, director):

        # Habria que pasarle como parámetro el número de fase, a partir del cual se cargue
        #  un fichero donde este la configuracion de esa fase en concreto, con cosas como
        #   - Nombre del archivo con el decorado
        #   - Posiciones de las plataformas
        #   - Posiciones de los enemigos
        #   - Posiciones de inicio de los jugadores
        #  etc.
        # Y cargar esa configuracion del archivo en lugar de ponerla a mano, como aqui abajo
        # De esta forma, se podrian tener muchas fases distintas con esta clase

        # Primero invocamos al constructor de la clase padre
        Escena.__init__(self, director)

        datos = GestorRecursos.CargarArchivoFase(archivoFase)
        print(datos)


        # Creamos el decorado y el fondo
        self.decorado = Mapa(datos['$mapa'])

        # Que parte del decorado estamos visualizando
        self.scrollx = 0
        self.scrolly = 0
        #  En ese caso solo hay scroll horizontal
        #  Si ademas lo hubiese vertical, seria self.scroll = (0, 0)

        # Creamos los sprites de los jugadores
        self.jugador1 = Jugador()
        # Ponemos a los jugadores en sus posiciones iniciales
        self.jugador1.establecerPosicion((datos['posicion_inicial'][0],datos['posicion_inicial'][1]))

        #Creamos los grupos de sprites con el jugador
        self.grupoSprites = pygame.sprite.Group( self.jugador1)
        self.grupoJugadores=pygame.sprite.Group(self.jugador1)
        # Cargamos los enemigos
        enemigo=[]
        self.grupoEnemigos=pygame.sprite.Group()
        for i in range (0,datos['enemigo'][0]):
          enemigo.append(Sniper())
          enemigo[i].establecerPosicion((datos['enemigo'][(2*i+1)],datos['enemigo'][(2*i+2)]))
          self.grupoEnemigos.add(enemigo[i])
          #self.grupoSpritesDinamicos.add(enemigo[i] )
          self.grupoSprites.add(enemigo[i])

        self.grupoSpritesDinamicos = pygame.sprite.Group()
        self.grupoColisionables = pygame.sprite.Group()
        ##TODO ESTO DESDE ARCHIVO FASE

        #Cargamos los objetos
        self.boton=accionable("boton_verde_pequeno.png",(187,562),pygame.Rect(170,573,66,55))
        self.grupoSprites.add(self.boton) #(NO SE PORQUE NO)
        self.boton2=accionable("boton_verde_pequeno.png",(556,623),pygame.Rect(546,623,66,55))
        self.grupoSprites.add(self.boton2) #(NO SE PORQUE NO)

        self.meta=accionable("boton_verde_pequeno.png",(1140,170),pygame.Rect(1111,192,146,128))
        self.grupoSprites.add(self.meta) #(NO SE PORQUE NO)




        self.puerta=activable("puerta_pequeña.png","coord_puerta_pequena",(368,898),pygame.Rect(362,890,68,60),False,1000)
        self.grupoSprites.add(self.puerta)
        self.grupoSpritesDinamicos.add(self.puerta)
        self.grupoColisionables.add(self.puerta)
        self.puerta2=activable("puerta_pequeña.png","coord_puerta_pequena",(594,610),pygame.Rect(0,0,1,1),False,1000)
        self.grupoSprites.add(self.puerta2)
        self.grupoSpritesDinamicos.add(self.puerta2)
        self.grupoColisionables.add(self.puerta2)
        self.luz=activable("luzprueba.png","coordenadasluz.txt",(328,575),pygame.Rect(328,575,497,143),True,1000)
        self.grupoSprites.add(self.luz)
        self.grupoSpritesDinamicos.add(self.luz)

        #Causas
        pulsar_puerta_1=causa(ACCION_AREA,self.puerta)
        pulsar_boton_1=causa(ACCION_AREA,self.boton)
        pulsar_boton_2=causa(ACCION_AREA,self.boton2)
        llegar_a_meta=causa(AREA,self.meta)

        #Consecuencias
        cambiar_puerta_1=accion(CAMBIAR,self.puerta,"",None)
        cambiar_puerta_2=accion(CAMBIAR,self.puerta2,"",None)
        cambiar_luz=accion(CAMBIAR,self.luz,"",None)
        mensaje_puerta=accion(MENSAJE,None,"Escuchas una puerta a lo lejos",None)
        mensaje_luz=accion(MENSAJE,None,"Escuchas el zuimbido de un tubo fluorescente ",None)
        fin=accion(FIN,None,"",None)
        self.listaeventos=[]
        self.listaeventos.append(evento([pulsar_puerta_1], [cambiar_puerta_1]))
        self.listaeventos.append(evento([pulsar_boton_1], [cambiar_puerta_2,mensaje_puerta]))
        self.listaeventos.append(evento([pulsar_boton_2], [cambiar_luz,mensaje_luz]))
        self.listaeventos.append(evento([llegar_a_meta], [fin]))

        #Cuadro de texto (provisional podria pasarse a una clase GUI)
        self.cuadrotexto=CuadroTexto()
        self.pausa=False
        self.haymensaje=False
        self.actiondropped=True

        #Grafo de prueba
        grafo={'1050 994':['1050 1118','1050 924','1175 994'] ,
               '1050 1118':['1050 994','1304 1118','920 1118'],
               '1304 994':['1304 1118','1175 994','1304 786'],
               '1304 1118':['1050 1118','1304 994'],
               '920 1118':['1050 994','802 1118','920 924'],
               '802 1118':['920 1118','687 1118','802 924'],
               '687 1118':['802 1118','687 924'],
               '1050 924':['1050 994','920 924','1050 786'],
               '920 924':['920 1118','1050 924','802 924'],
               '802 924':['802 1118','920 924','687 924'],
               '687 924':['687 1118', '802 924'],
               '1175 994':['1050 994','1304 994','1175 786'],
               '1050 786':['1050 924','1175 786','1050 604'],
               '1175 786':['1175 994','1050 786', '1304 786'],
               '1304 786':['1304 994','1175 994','1304 604'],
               '1050 604':['1050 786','1175 604'],
               '1175 604':['1175 786','1050 604','1304 604'],
               '1304 604':['1304 786','1175 604']}






        #Enemigo con grafo
        patrulla=Patrulla(grafo)
        patrulla.establecerPosicion((1050,998))
        self.grupoEnemigos.add(patrulla)
        #self.grupoSpritesDinamicos.add(enemigo[i] )
        self.grupoSprites.add(patrulla)


        
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
        # Primero, se indican las acciones que van a hacer los enemigos segun como esten los jugadores
            for enemigo in iter(self.grupoEnemigos):
                enemigo.mover_cpu(self.jugador1)
            #self.grupoJugadores.update(self,tiempo)
            self.jugador1.update(self,tiempo)
            #self.grupoEnemigos.update(self,tiempo) provisionalmente 1 a 1
            for enemigo in self.grupoEnemigos.sprites():
                enemigo.update(self,tiempo)
            self.grupoSpritesDinamicos.update(tiempo)
            #if pygame.sprite.groupcollide(self.grupoJugadores, self.grupoEnemigos, False, False)!={}:
            #    self.director.salirEscena()

            # Actualizamos el scroll
            self.actualizarScroll(self.jugador1)
  

        
    def dibujar(self, pantalla):
        #Primero las capas que no tapan a los sprites
        self.decorado.dibujar_pre(pantalla)
        # Luego los Sprites
        self.grupoSprites.draw(pantalla)
        #Luego las capas que tapan a los sprites
        self.decorado.dibujar_post(pantalla)

        Debuger.anadirRectangulo(self.boton.area)
        Debuger.anadirRectangulo(self.puerta.area)
        Debuger.anadirRectangulo(self.meta.area)


        Debuger.dibujarTexto(pantalla)
        Debuger.dibujarLineas(pantalla,(self.scrollx,self.scrolly))
        if(self.haymensaje):
            self.cuadrotexto.draw(pantalla)

    def colision(self,rect):
       rectlist=[]
       for sprite in self.grupoColisionables.sprites():
           if not sprite.estado:
              rectlist.append(sprite.pos_inicial)
       collidesprite=rect.collidelist(rectlist)
       Debuger.anadirTextoDebug("colisiones "+str(collidesprite))
       return self.decorado.colision(rect) or collidesprite>-1


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
             for evento in self.listaeventos:
                 if evento.comprobar(self.jugador1,action):
                     evento.lanzar(self)
        else:
            if not teclasPulsadas[K_RETURN]:
                self.actiondropped=True
            elif self.actiondropped:
                self.pausa=False
                self.haymensaje=False
                self.actiondropped=False


        #AQUI SE DEBERIAN COMROBAR LOS EVENTOS DEL JUEGO

    def mostrarMensaje(self,texto):
        self.cuadrotexto.establecerTexto(texto)
        self.pausa=True
        self.haymensaje=True
        self.actiondropped=False