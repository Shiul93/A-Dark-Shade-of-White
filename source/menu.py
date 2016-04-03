# -*- encoding: utf-8 -*-

import pygame
from pygame.locals import *
from escena import *
from gestorRecursos import *
from fase import *
from menu import *
# -------------------------------------------------
# Clase abstracta ElementoGUI
ANCHO_PANTALLA =800
ALTO_PANTALLA_MENU =720
class ElementoGUI:
	def __init__(self, pantalla, rectangulo):
		self.pantalla = pantalla
		self.rect = rectangulo

	def establecerPosicion(self, posicion):
		(posicionx, posiciony) = posicion
		self.rect.left = posicionx
		self.rect.bottom = posiciony

	def posicionEnElemento(self, posicion):
		(posicionx, posiciony) = posicion
		if (posicionx>=self.rect.left) and (posicionx<=self.rect.right) and (posiciony>=self.rect.top) and (posiciony<=self.rect.bottom):
			return True
		else:
			return False

	def dibujar(self):
		raise NotImplemented("Tiene que implementar el metodo dibujar.")
	def accion(self):
		raise NotImplemented("Tiene que implementar el metodo accion.")


# -------------------------------------------------
# Clase Boton y los distintos botones

class Boton(ElementoGUI):
	def __init__(self, pantalla, nombreImagen, posicion):
		# Se carga la imagen del boton
		self.imagen = GestorRecursos.CargarImagenMenu(nombreImagen,-1)
		#self.imagen = pygame.transform.scale(self.imagen, (20, 20))
		# Se llama al método de la clase padre con el rectángulo que ocupa el botón
		ElementoGUI.__init__(self, pantalla, self.imagen.get_rect())
		# Se coloca el rectangulo en su posicion
		self.establecerPosicion(posicion)
	def dibujar(self, pantalla):
		pantalla.blit(self.imagen, self.rect)

#Botones menu principal
class BotonNP(Boton):
	def __init__(self, pantalla):
		Boton.__init__(self, pantalla, 'humo.png', (60,200))
	def accion(self):
		self.pantalla.menu.ejecutarJuego()

class BotonCP(Boton):
	def __init__(self, pantalla):
		Boton.__init__(self, pantalla, 'humo.png', (500,200))
	def accion(self):
		self.pantalla.menu.mostrarPantallaFases()

class BotonOpciones(Boton):
	def __init__(self, pantalla):
		Boton.__init__(self, pantalla, 'humo.png', (60,540))
	def accion(self):
		self.pantalla.menu.mostrarPantallaOpciones()

class BotonSalir(Boton):
	def __init__(self, pantalla):
		Boton.__init__(self, pantalla, 'humo.png', (500,540))
	def accion(self):
		self.pantalla.menu.salirPrograma()

#Botones menu fases

class BotonF1(Boton):
	def __init__(self, pantalla):
		Boton.__init__(self, pantalla, 'humo.png', (40,160))
	def accion(self):
		self.pantalla.menu.ejecutarF1()

class BotonF2(Boton):
	def __init__(self, pantalla):
		Boton.__init__(self, pantalla, 'humo.png', (500,160))
	def accion(self):
		self.pantalla.menu.ejecutarF2()

class BotonF3(Boton):
	def __init__(self, pantalla):
		Boton.__init__(self, pantalla, 'humo.png', (40,350))
	def accion(self):
		self.pantalla.menu.ejecutarF3()

class BotonF4(Boton):
	def __init__(self, pantalla):
		Boton.__init__(self, pantalla, 'humo.png', (500,350))
	def accion(self):
		self.pantalla.menu.ejecutarF4()
		
class BotonF5(Boton):
	def __init__(self, pantalla):
		Boton.__init__(self, pantalla, 'humo.png', (40,540))
	def accion(self):
		self.pantalla.menu.ejecutarF5()

class BotonVolver(Boton):
	def __init__(self, pantalla):
		Boton.__init__(self, pantalla, 'humo.png', (500,540))
	def accion(self):
		self.pantalla.menu.mostrarPantallaInicial()

# -------------------------------------------------
# Clase TextoGUI y los distintos textos

class TextoGUI(ElementoGUI):
	def __init__(self, pantalla, fuente, color, texto, posicion):
		# Se crea la imagen del texto
		self.imagen = fuente.render(texto, True, color)
		# Se llama al método de la clase padre con el rectángulo que ocupa el texto
		ElementoGUI.__init__(self, pantalla, self.imagen.get_rect())
		# Se coloca el rectangulo en su posicion
		self.establecerPosicion(posicion)
	def dibujar(self, pantalla):
		pantalla.blit(self.imagen, self.rect)

#Textos menu principal
class TextoNP(TextoGUI):
	def __init__(self, pantalla):
		# La fuente la debería cargar el estor de recursos
		fuente = pygame.font.SysFont('arial', 26);
		TextoGUI.__init__(self, pantalla, fuente, (255, 255, 255), 'Nueva Partida', (100, 160))
	def accion(self):
		self.pantalla.menu.ejecutarJuego()

class TextoCP(TextoGUI):
	def __init__(self, pantalla):
		# La fuente la debería cargar el estor de recursos
		fuente = pygame.font.SysFont('arial', 26);
		TextoGUI.__init__(self, pantalla, fuente, (255, 255, 255), 'Cargar Fase', (550, 160))
	def accion(self):
		self.pantalla.menu.mostrarPantallaFases()

class TextoOpciones(TextoGUI):
	def __init__(self, pantalla):
		# La fuente la debería cargar el estor de recursos
		fuente = pygame.font.SysFont('arial', 26);
		TextoGUI.__init__(self, pantalla, fuente, (255, 255, 255), 'Opciones', (130, 500))
	def accion(self):
		self.pantalla.menu.mostrarPantallaOpciones()

class TextoSalir(TextoGUI):
	def __init__(self, pantalla):
		# La fuente la debería cargar el estor de recursos
		fuente = pygame.font.SysFont('arial', 26);
		TextoGUI.__init__(self, pantalla, fuente, (255, 255, 255), 'Salir', (590, 500))
	def accion(self):
		self.pantalla.menu.salirPrograma()

#Textos menu fases

class TextoF1(TextoGUI):
	def __init__(self, pantalla):
		# La fuente la debería cargar el estor de recursos
		fuente = pygame.font.SysFont('arial', 26);
		TextoGUI.__init__(self, pantalla, fuente, (255, 255, 255), 'Fase 1', (120, 120))
	def accion(self):
		self.pantalla.menu.ejecutarF1()
		
class TextoF2(TextoGUI):
	def __init__(self, pantalla):
		# La fuente la debería cargar el estor de recursos
		fuente = pygame.font.SysFont('arial', 26);
		TextoGUI.__init__(self, pantalla, fuente, (255, 255, 255), 'Fase 2', (580, 120))
	def accion(self):
		self.pantalla.menu.ejecutarF2()
		
class TextoF3(TextoGUI):
	def __init__(self, pantalla):
		# La fuente la debería cargar el estor de recursos
		fuente = pygame.font.SysFont('arial', 26);
		TextoGUI.__init__(self, pantalla, fuente, (255, 255, 255), 'Fase 3', (120, 310))
	def accion(self):
		self.pantalla.menu.ejecutarF3()
		
class TextoF4(TextoGUI):
	def __init__(self, pantalla):
		# La fuente la debería cargar el estor de recursos
		fuente = pygame.font.SysFont('arial', 26);
		TextoGUI.__init__(self, pantalla, fuente, (255, 255, 255), 'Fase 4', (580, 310))
	def accion(self):
		self.pantalla.menu.ejecutarF4()
		
class TextoF5(TextoGUI):
	def __init__(self, pantalla):
		# La fuente la debería cargar el estor de recursos
		fuente = pygame.font.SysFont('arial', 26);
		TextoGUI.__init__(self, pantalla, fuente, (255, 255, 255), 'Fase 5', (120, 500))
	def accion(self):
		self.pantalla.menu.ejecutarF5()

class TextoVolver(TextoGUI):
	def __init__(self, pantalla):
		# La fuente la debería cargar el estor de recursos
		fuente = pygame.font.SysFont('arial', 26);
		TextoGUI.__init__(self, pantalla, fuente, (255, 255, 255), 'Volver', (590, 500))
	def accion(self):
		self.pantalla.menu.mostrarPantallaInicial()
		
# -------------------------------------------------
# Clase PantallaGUI y las distintas pantallas

class PantallaGUI:
	def __init__(self, menu, nombreImagen):
		self.menu = menu
		# Se carga la imagen de fondo
		GestorRecursos.getPath() #ESTA LLAMADA SE REALIZA ANTES DE CARGAR NINGUN ARCHIVO PARA QUE CALCULE EL PATH PORQUE ME DABA PROBLEMAS
		self.imagen = GestorRecursos.CargarImagenMenu(nombreImagen)
		self.imagen = pygame.transform.scale(self.imagen, (ANCHO_PANTALLA, ALTO_PANTALLA_MENU))
		# Se tiene una lista de elementos GUI
		self.elementosGUI = []

	def eventos(self, lista_eventos):
		for evento in lista_eventos:
			if evento.type == MOUSEBUTTONDOWN:
				self.elementoClic = None
				for elemento in self.elementosGUI:
					if elemento.posicionEnElemento(evento.pos):
						self.elementoClic = elemento
			if evento.type == MOUSEBUTTONUP:
				for elemento in self.elementosGUI:
					if elemento.posicionEnElemento(evento.pos):
						if (elemento == self.elementoClic):
							elemento.accion()

	def dibujar(self, pantalla):
		# Dibujamos primero la imagen de fondo
		pantalla.blit(self.imagen, self.imagen.get_rect())
		# Después los botones
		for elemento in self.elementosGUI:
			elemento.dibujar(pantalla)

class PantallaInicialGUI(PantallaGUI):
	def __init__(self, menu):
		PantallaGUI.__init__(self, menu, 'hacker.jpg')
		# Creamos los botones y los metemos en la lista
		botonNP = BotonNP(self)
		botonCP = BotonCP(self)
		botonOpciones = BotonOpciones(self)
		botonSalir = BotonSalir(self)
		self.elementosGUI.append(botonNP)
		self.elementosGUI.append(botonCP)
		self.elementosGUI.append(botonOpciones)
		self.elementosGUI.append(botonSalir)
		# Creamos el texto y lo metemos en la lista
		textoNP = TextoNP(self)
		textoCP = TextoCP(self)
		textoOpciones = TextoOpciones(self)
		textoSalir = TextoSalir(self)
		self.elementosGUI.append(textoNP)
		self.elementosGUI.append(textoCP)
		self.elementosGUI.append(textoOpciones)
		self.elementosGUI.append(textoSalir)
		
class PantallaFasesGUI(PantallaGUI):
	def __init__(self, menu):
		PantallaGUI.__init__(self, menu, 'hacker.jpg')
		# Creamos los botones y los metemos en la lista
		botonF1 = BotonF1(self)
		botonF2 = BotonF2(self)
		botonF3 = BotonF3(self)
		botonF4 = BotonF4(self)
		botonF5 = BotonF5(self)
		botonVolver = BotonVolver(self)
		self.elementosGUI.append(botonF1)
		self.elementosGUI.append(botonF2)
		self.elementosGUI.append(botonF3)
		self.elementosGUI.append(botonF4)
		self.elementosGUI.append(botonF5)
		self.elementosGUI.append(botonVolver)
		# Creamos el texto y lo metemos en la lista
		textoF1 = TextoF1(self)
		textoF2 = TextoF2(self)
		textoF3 = TextoF3(self)
		textoF4 = TextoF4(self)
		textoF5 = TextoF5(self)
		textoVolver = TextoVolver(self)
		self.elementosGUI.append(textoF1)
		self.elementosGUI.append(textoF2)
		self.elementosGUI.append(textoF3)
		self.elementosGUI.append(textoF4)
		self.elementosGUI.append(textoF5)
		self.elementosGUI.append(textoVolver)

class PantallaOpcionesGUI(PantallaGUI):
	def __init__(self, menu):
		PantallaGUI.__init__(self, menu, 'hacker.jpg')
		# Creamos los botones y los metemos en la lista
		botonVolver = BotonVolver(self)
		self.elementosGUI.append(botonVolver)
		# Creamos el texto y lo metemos en la lista
		textoVolver = TextoVolver(self)
		self.elementosGUI.append(textoVolver)

# -------------------------------------------------
# Clase Menu, la escena en sí

class Menu(Escena):

	def __init__(self, director):
		# Llamamos al constructor de la clase padre
		Escena.__init__(self, director);
		# Creamos la lista de pantallas
		self.listaPantallas = []
		# Creamos las pantallas que vamos a tener
		#	y las metemos en la lista
		self.listaPantallas.append(PantallaInicialGUI(self))
		self.listaPantallas.append(PantallaFasesGUI(self))
		self.listaPantallas.append(PantallaOpcionesGUI(self))
		GestorRecursos.CargarMusica('A-Dark-Shade-of-White')
		pygame.mixer.music.play()
		# En que pantalla estamos actualmente
		self.mostrarPantallaInicial()


	def update(self, *args):
		return

	def eventos(self, lista_eventos):
		# Se mira si se quiere salir de esta escena
		for evento in lista_eventos:
			# Si se quiere salir, se le indica al director
			if evento.type == KEYDOWN:
				if evento.key == K_ESCAPE:
					self.salirPrograma()
			elif evento.type == pygame.QUIT:
				self.director.salirPrograma()

		# Se pasa la lista de eventos a la pantalla actual
		self.listaPantallas[self.pantallaActual].eventos(lista_eventos)

	def dibujar(self, pantalla):
		self.listaPantallas[self.pantallaActual].dibujar(pantalla)

	#--------------------------------------
	# Metodos propios del menu

	def salirPrograma(self):
		self.director.salirPrograma()

	def ejecutarJuego(self):
		fase = Fase('fase1',self.director)
		self.director.apilarEscena(fase)

	def mostrarPantallaInicial(self):
		self.pantallaActual = 0
		
	def mostrarPantallaFases(self):
		self.pantallaActual = 1
	
	def mostrarPantallaOpciones(self):
		self.pantallaActual = 2
	
	def ejecutarF1(self):
		fase = Fase('fase1',self.director)
		self.director.apilarEscena(fase)
		
	def ejecutarF2(self):
		fase = Fase('fase2',self.director)
		self.director.apilarEscena(fase)
		
	def ejecutarF3(self):
		fase = Fase('fase3',self.director)
		self.director.apilarEscena(fase)
		
	def ejecutarF4(self):
		fase = Fase('fase4',self.director)
		self.director.apilarEscena(fase)
		
	def ejecutarF5(self):
		fase = Fase('fase5',self.director)
		self.director.apilarEscena(fase)


