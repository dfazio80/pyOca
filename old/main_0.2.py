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
    # turno: define quien tira el dado (jugador1 o jugador 2)
    # posX, posY: coordenadas donde se dibuja la imagen
    turno = 0
    def __init__(self, color):
        self.posic = 1
        self.posX = tablero.coordX[self.posic]
        self.posY = tablero.coordY[self.posic]
        self.turno = False
        try:
            self.img = pygame.image.load(os.path.join(img_folder,'ficha_'+color+'.png'))
        except:
            print ("Error: No se pueden cargar las imagenes de las fichas")
            fin_programa()

    def mover(self, cantMov, avanza = True): # Le envio a  la funcion si tiene que avanzar o retroceder
                                             # por defecto, siempre avanza
        while not (cantMov == 0):
            if (self.posic == 63 and cantMov > 0): #defino si se pasa de 63, debe retroceder
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

class cCajaTexto:
    def __init__(self, txt, pos, color):
        self.dictTxt = {'vacio':'',
                        'inicio':'La primer tirada define que jugador comienza. Presione ENTER',
                        'ini1':'Comienza el JUGADOR 1',
                        'ini2':'Comienza el JUGADOR 2',
                        'empate':'Empate, vuelve a tirar. Presione ENTER',
                        'turno1':'Turno: JUGADOR 1',
                        'turno2':'Turno: JUGADOR 2',
                        'oca':'Casilla de Oca: avanza hasta la próxima oca y vuelve a tirar',
                        'puente':'Casilla de Puente: avanza hasta la posada (casilla 19) y pierde un turno',
                        'mismacasilla': 'Hay otro jugador en la casilla, vuelve a su posición anterior'}
        self.texto = fuente.render (self.dictTxt[txt], True, color)
        self.posXY = pos
    def cambiaTxt (self, txt, color):
        self.texto = fuente.render (self.dictTxt[txt], True, color)

# ---- FUNCIONES ----

def define_primero():
    eventosTxt.cambiaTxt('inicio', NEGRO)
    dibuja_pantalla()
        
    empate = True
    while empate:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                fin_programa()
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN):
                dadoA.tirar()
                dadoB.tirar()
                if (dadoA.valor > dadoB.valor):
                    eventosTxt.cambiaTxt('ini1', AZUL)
                    cJugador.turno = 1
                    empate = False
                elif (dadoA.valor < dadoB.valor):
                    eventosTxt.cambiaTxt('ini2', ROJO)
                    cJugador.turno = 2
                    empate = False
                else:
                    eventosTxt.cambiaTxt('empate', NEGRO)
                    empate = True
                dibuja_pantalla(False) # Llamo dibuja_pantalla con dos dados
    pygame.time.wait(2000)

def dibuja_pantalla(unDado=True):
    display.fill((0, 0, 0))
    display.blit(tablero.img, tablero.posXY)
    if unDado:
        display.blit(dado.img, dado.posXY)
    else:
        display.blit(dadoA.img, dadoA.posXY)
        display.blit(dadoB.img, dadoB.posXY)
    display.blit(jugador1.img, (jugador1.posX,jugador1.posY))
    display.blit(jugador2.img, (jugador2.posX,jugador2.posY))
    display.blit(eventosTxt.texto, eventosTxt.posXY)
    display.blit(turnoTxt.texto, turnoTxt.posXY)
    pygame.display.flip()
    clock.tick(60)

def cambiaTurno():
    if (cJugador.turno == 1):
        cJugador.turno = 2
        turnoTxt.cambiaTxt('turno2', ROJO)
    else:
        cJugador.turno = 1
        turnoTxt.cambiaTxt('turno1', AZUL)
    dibuja_pantalla()    

def evalua_casilla(jugAct, jugEsp): #jugAct: jugador actual, #jugEsp: jugador en espera

    if (jugAct.posic == jugEsp.posic): #Cayo en la misma casilla que el otro jugador, debe retroceder
        eventosTxt.cambiaTxt('mismacasilla', NEGRO)
        pygame.time.wait(800)
        jugAct.mover(dado.valor, avanza = False)
        cambiaTurno()
    elif jugAct.posic in POS_OCA: #Casilla de Oca: avanza hasta la próxima oca y vuelve a tirar
        eventosTxt.cambiaTxt('oca', NEGRO)
        pygame.time.wait(800)
        i = POS_OCA.index(jugAct.posic)
        if jugAct.posic != 59: #Es la ultima oca, solo tira nuevamente
            jugAct.mover(POS_OCA[i+1]-POS_OCA[i])
            eventosTxt.cambiaTxt('vacio', NEGRO)
    elif jugAct.posic in POS_PUENTE: #Casilla de Puente: avanza hasta la posada (casilla 19) y pierde un turno
        eventosTxt.cambiaTxt('puente', NEGRO)
        

        
    else: # casilla comun, cambia turno
        cambiaTurno()

def fin_programa():
    pygame.quit()
    sys.exit()

def main():
    # defino quien comienza con una tirada de dados inicial 
    define_primero()
    dibuja_pantalla()
    while True: # loop principal
        for event in pygame.event.get(): # eventos de pygame -- deteccion de input de teclado
                if event.type == pygame.QUIT:
                    fin_programa()
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_LCTRL) and (cJugador.turno == 1): # Tira dados el jugador 1 con LCTRL
                    eventosTxt.cambiaTxt('vacio', NEGRO)
                    dado.posXY = POSDADO1
                    dado.tirar()
                    jugador1.mover(dado.valor)
                    evalua_casilla(jugador1, jugador2)
                if (event.type == pygame.KEYDOWN and event.key == pygame.K_RCTRL) and (cJugador.turno == 2): # Tira dados el jugador 2 con RCTRL
                    eventosTxt.cambiaTxt('vacio', NEGRO)
                    dado.posXY = POSDADO2
                    dado.tirar()
                    jugador2.mover(dado.valor)
                    evalua_casilla(jugador2, jugador1)
                    
# ---- INIT, VAR y CONST ----

# inicio pygame y reloj para FPS
pygame.init()
clock = pygame.time.Clock()
# defino constantes
SIZEXY = (750,650)
POSDADO1 = (645,130)
POSDADO2 = (645,455)
POS_TXT_EVT = (20,610)
POS_TXT_TURNO = (550,610)
POS_OCA = [5,9,14,18,23,27,32,36,41,45,50,54,59]
POS_PUENTE = [6,12]
# defino los colores para los textos
AZUL = (0,71,255)
ROJO = (255,51,51)
NEGRO = (0,0,0)
# inicio ventana
display = pygame.display.set_mode(SIZEXY)
pygame.display.set_caption('El juego de la oca')
# cargo la fuente para el texto
fuente = pygame.font.SysFont("Microsoft Sans Serif", 18)
# defino carpeta de imagenes
img_folder = os.path.join(os.path.dirname(__file__), 'img')
# creo los objetos principales del juego
tablero = cTablero()
dado = cDado()
jugador1 = cJugador('azul')
jugador2 = cJugador('rojo')
eventosTxt = cCajaTexto('vacio',POS_TXT_EVT,NEGRO)
turnoTxt = cCajaTexto('vacio',POS_TXT_TURNO,NEGRO)
# genero dos dados temporales para la primer tirada
dadoA = cDado()
dadoB = cDado()
dadoA.posXY = POSDADO1
dadoB.posXY = POSDADO2

if __name__ == "__main__":
    main()
