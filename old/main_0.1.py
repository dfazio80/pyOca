import pygame, sys, os, random
from pygame.locals import *

# ---- CLASES ----

class cTablero:
    # __init__ carga la imagen para el tablero
    # posXY: coordenadas donde se dibuja la imagen (estatica)
    def __init__(self):
        self.posXY = (0,0)
        self.coordX = [0,135,205,255,305,355,400,445,490,515,515, #10
                         515,515,515,515,515,515,515,515,490,445, #20
                         400,350,300,255,205,155,110,70,40,40,    #30
                         40,40,40,40,40,40,65,110,155,205,        #40
                         250,300,350,390,415,415,415,415,415,415, #50
                         395,350,305,255,210,165,140,140,140,140, #60
                         170,215,275]
        self.coordY = [0,515,515,515,515,515,515,515,515,485,445, #10
                         400,350,300,255,205,155,115,70,45,45,    #20
                         45,45,45,45,45,45,45,45,65,115,          #30
                         155,205,255,305,350,395,415,415,415,415, #40
                         415,415,415,415,390,345,300,255,215,165, #50
                         140,140,140,140,140,140,165,210,255,295, #60
                         320,320,320]
        try:
            self.img = pygame.image.load(os.path.join(img_folder,'tablero_oca.png'))
        except:
            print ("Error: No se pueden cargar la imagen del tablero")
            fin_programa()

class cDado:
    # __init__ : El dado carga las seis imagenes con sus seis valores
    # tirar: Se usa un random entre 1 y 6 y se carga la imagen correspondiente en self.imgAct
    # valor: valor del dado de la tirada actual (inicializada en 0)
    # posXY: coordenadas donde se dibuja la imagen (estatica)
    def __init__(self):
        self.valor = 0
        self.posXY = (0,0)
        try:
            self.listimg = [pygame.Surface((0,0)), 
                            pygame.image.load(os.path.join(img_folder,'dado1.png')),
                            pygame.image.load(os.path.join(img_folder,'dado2.png')),
                            pygame.image.load(os.path.join(img_folder,'dado3.png')),
                            pygame.image.load(os.path.join(img_folder,'dado4.png')),
                            pygame.image.load(os.path.join(img_folder,'dado5.png')),
                            pygame.image.load(os.path.join(img_folder,'dado6.png'))]
            self.img = self.listimg[self.valor]
        except:
            print ("Error: No se pueden cargar las imagenes de los dados")
            fin_programa()
    def tirar(self):
        self.valor = random.randint(1,6)
        self.img = self.listimg[self.valor]

class cJugador:
    # __init__: el jugador comienza en la casilla 1 y se cargan las imagenes de ficha
    # mover: mueve la ficha tantas posiciones indique el dado, retrocede si se excede de 63
    # La var turno define a quien le toca tirar los dados (turno = 1 o 2)
    # posX, posY: coordenadas donde se dibuja la imagen
    turno = 1
    def __init__(self, color):
        self.posic = 1
        self.posX = tablero.coordX[self.posic]
        self.posY = tablero.coordY[self.posic]
        try:
            self.img = pygame.image.load(os.path.join(img_folder,'ficha_'+color+'.png'))
        except:
            print ("Error: No se pueden cargar las imagenes de las fichas")
            fin_programa()

    def mover(self, cantMov):
        # avanza: Si se pasa de 63, se retroceden tantas casillas se haya pasado, sino es una jugada normal
        avanza = True
        while not (cantMov == 0):
            if (self.posic == 63 and cantMov > 0):
              avanza = False
            if (avanza):
                # movimiento normal
                self.posic += 1
            else:
                # va hacia atras
                self.posic -= 1
            # animacion de la ficha
            while not (self.posX == tablero.coordX[self.posic] and self.posY == tablero.coordY[self.posic]):
                if (self.posX > tablero.coordX[self.posic]):
                    self.posX -= 5
                elif (self.posX < tablero.coordX[self.posic]):
                    self.posX += 5
                if (self.posY > tablero.coordY[self.posic]):
                    self.posY -= 5
                elif (self.posY < tablero.coordY[self.posic]):
                    self.posY += 5
                dibuja_pantalla()                
            # Siempre decrementa la cantidad a avanzar
            cantMov -= 1
                
# ---- FUNCIONES ----

def dibuja_pantalla():
    display.fill((0, 0, 0))
    display.blit(tablero.img, tablero.posXY)
    display.blit(dado.img, dado.posXY)
    display.blit(jugador1.img, (jugador1.posX,jugador1.posY))
    display.blit(jugador2.img, (jugador2.posX,jugador2.posY))
    pygame.display.flip()
    clock.tick(60)

def fin_programa():
    pygame.quit()
    sys.exit()

def main():
    dibuja_pantalla()
    while True: # loop principal
        for event in pygame.event.get(): # eventos de pygame -- deteccion de input de teclado
                if event.type == pygame.QUIT:
                    fin_programa()
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_LCTRL) and (cJugador.turno == 1): # Tira dados el jugador 1 con LCTRL
                    dado.posXY = posDado1
                    dado.tirar()
                    jugador1.mover(dado.valor)
                    cJugador.turno = 2
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_RCTRL) and (cJugador.turno == 2): # Tira dados el jugador 2 con RCTRL
                    dado.posXY = posDado2
                    dado.tirar()
                    jugador2.mover(dado.valor)
                    cJugador.turno = 1
                    
# ---- INIT, VAR y CONST ----

# inicio pygame y reloj para FPS
pygame.init()
clock = pygame.time.Clock()
# defino constantes
sizeXY = (800,600)
posDado1 = (670,80)
posDado2 = (670,240)
# inicio ventana
display = pygame.display.set_mode(sizeXY)
pygame.display.set_caption('El juego de la oca')
# defino carpeta de imagenes
img_folder = os.path.join(os.path.dirname(__file__), 'img')
# creo los objetos del juego
tablero = cTablero()
dado = cDado()
jugador1 = cJugador('azul')
jugador2 = cJugador('rojo')

if __name__ == "__main__":
    main()
