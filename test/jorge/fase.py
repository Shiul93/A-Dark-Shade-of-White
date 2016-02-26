# -*- coding: utf-8 -*-

import pygame, escena
from escena import *
from personajes import *
from pygame.locals import *

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
    def __init__(self, director):

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

        # Creamos el decorado y el fondo
        self.decorado = Decorado()

        # Que parte del decorado estamos visualizando
        self.scrollx = 0
        self.scrolly = 0
        #  En ese caso solo hay scroll horizontal
        #  Si ademas lo hubiese vertical, seria self.scroll = (0, 0)

        # Creamos los sprites de los jugadores
        self.jugador1 = Jugador()
        self.grupoJugadores = pygame.sprite.Group( self.jugador1 )

        # Ponemos a los jugadores en sus posiciones iniciales
        self.jugador1.establecerPosicion((400, 980))


        # Y los enemigos que tendran en este decorado
        enemigo1 = Sniper()
        enemigo1.establecerPosicion((582, 716))
        enemigo2 = Sniper()
        enemigo2.establecerPosicion((1309, 1113))
        enemigo3 = Sniper()
        enemigo3.establecerPosicion((386, 356))
        # Creamos un grupo con los enemigos
        self.grupoEnemigos = pygame.sprite.Group( enemigo1 , enemigo2 , enemigo3 )


        # Creamos un grupo con los Sprites que se mueven
        #  En este caso, solo los personajes, pero podría haber más (proyectiles, etc.)
        self.grupoSpritesDinamicos = pygame.sprite.Group( self.jugador1,  enemigo1, enemigo2,enemigo3 )
        # Creamos otro grupo con todos los Sprites
        self.grupoSprites = pygame.sprite.Group( self.jugador1,  enemigo1,enemigo2,enemigo3)



        
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
                actualizar=True; # Se ha actualizado el scroll
        # Si el jugador están entre los dos límites de la pantalla, no se hace nada
        return actualizar;


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

        # Primero, se indican las acciones que van a hacer los enemigos segun como esten los jugadores
        for enemigo in iter(self.grupoEnemigos):
            enemigo.mover_cpu(self.jugador1)
        # Esta operación es aplicable también a cualquier Sprite que tenga algún tipo de IA
        # En el caso de los jugadores, esto ya se ha realizado

        # Actualizamos los Sprites dinamicos
        # De esta forma, se simula que cambian todos a la vez
        # Esta operación de update ya comprueba que los movimientos sean correctos
        #  y, si lo son, realiza el movimiento de los Sprites
        self.grupoSpritesDinamicos.update(self.decorado, tiempo)
        # Dentro del update ya se comprueba que todos los movimientos son válidos
        #  (que no choque con paredes, etc.)

        # Los Sprites que no se mueven no hace falta actualizarlos,
        #  si se actualiza el scroll, sus posiciones en pantalla se actualizan más abajo
        # En cambio, sí haría falta actualizar los Sprites que no se mueven pero que tienen que
        #  mostrar alguna animación

        # Comprobamos si hay colision entre algun jugador y algun enemigo
        # Se comprueba la colision entre ambos grupos
        # Si la hay, indicamos que se ha finalizado la fase
        if pygame.sprite.groupcollide(self.grupoJugadores, self.grupoEnemigos, False, False)!={}:
            # Se le dice al director que salga de esta escena y ejecute la siguiente en la pila
            self.director.salirEscena()

        # Actualizamos el scroll
        self.actualizarScroll(self.jugador1)
  
        # Actualizamos el fondo:
        #  la posicion del sol y el color del cielo

        
    def dibujar(self, pantalla):
        # Ponemos primero el fondo
        #self.fondo.dibujar(pantalla)
        # Después el decorado
        self.decorado.dibujar(pantalla)
        # Luego los Sprites
        self.grupoSprites.draw(pantalla)


    def eventos(self, lista_eventos):
        # Miramos a ver si hay algun evento de salir del programa
        for evento in lista_eventos:
            # Si se quiere salir, se le indica al director
            if evento.type == pygame.QUIT:
                self.director.salirPrograma()

        # Indicamos la acción a realizar segun la tecla pulsada para cada jugador
        teclasPulsadas = pygame.key.get_pressed()
        self.jugador1.mover(teclasPulsadas, K_UP, K_DOWN, K_LEFT, K_RIGHT,K_RCTRL,K_RSHIFT)


# -------------------------------------------------
# Clase Decorado

class Decorado:
    def __init__(self):
        #Cargamos la imagen del fondo
        self.imagen = GestorRecursos.CargarImagen('museo_1.png', 1)
        #Cargamos el mapa de colisiones
        self.collmap= GestorRecursos.CargarImagen('museo_1_coll.png',-1)
        self.rect = self.imagen.get_rect()
        #self.rect.bottom = 1200#ALTO_PANTALLA

        # La subimagen que estamos viendo
        self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
        self.rectSubimagen.left = 0 # El scroll horizontal empieza en la posicion 0 por defecto
        self.rectSubimagen.top = 0 # El scroll vertical empieza en la posicion 0 por defecto

    def update(self, scrollx,scrolly):
        #Cuando cambia el scroll cambiamos la posicion del rectangulo que define el trozo de fondo que se muestra
        self.rectSubimagen.left = scrollx
        self.rectSubimagen.top = scrolly


    def dibujar(self, pantalla):
        #Vuelca el rectángulo con el trozo corresponiente de la imagen
        pantalla.blit(self.imagen, self.rect, self.rectSubimagen)

    def colision(self,rect):
        #Comprueba si hay colision en cualquiera de las 4 esquinas del rectángulo recibido
        #Lo que comprueba es el color del pixel del mapa de colisiones en el punto deseado
        #En este caso se comprueba que el rojo no valga 0
        #Si vale 0 en las 4 esquinas no hay colision
        #Se podria usar tambien el alfa ( seria mas lógico)
        #pygame.Color.r = rojo .g = verde .b = azul .a = alfa
        color1=self.collmap.get_at(rect.topleft)
        color2=self.collmap.get_at(rect.topright)
        color3=self.collmap.get_at(rect.bottomleft)
        color4=self.collmap.get_at(rect.bottomright)
        return color1.r>0 or color2.r>0 or color3.r>0 or color4.r>0

