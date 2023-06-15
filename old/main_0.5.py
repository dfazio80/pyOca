#  pyOca 0.5 - una versión del juego de la oca en python
#  Copyright (C) 2014 Diego Fazio (dfazio80@gmail.com)
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.


import pygame, sys, os, random
from pygame.locals import *

VERSION = '0.5'

# ---- CLASES ----

class cTablero:
    # __init__ carga la imagen para el tablero
    # posXY: coordenadas donde se dibuja la imagen (estatica)
    def __init__(self):
        self.posXY = (0,0)
        self.coordX = [45,115,205,255,305,355,400,445,490,515,515, #10
                         515,515,515,515,515,515,515,515,490,445,  #20
                         400,350,300,255,205,155,110,70,40,40,     #30
                         40,40,40,40,40,40,65,110,155,205,         #40
                         250,300,350,390,415,415,415,415,415,415,  #50
                         395,350,305,255,210,165,140,140,140,140,  #60
                         170,215,275]
        self.coordY = [515,515,515,515,515,515,515,515,515,485,445,#10
                         400,350,300,255,205,155,115,70,45,45,     #20
                         45,45,45,45,45,45,45,45,65,115,           #30
                         155,205,255,305,350,395,415,415,415,415,  #40
                         415,415,415,415,390,345,300,255,215,165,  #50
                         140,140,140,140,140,140,165,210,255,295,  #60
                         320,320,320]
        try:
            self.img = pygame.image.load(os.path.join(data_folder,'tablero_oca.png')).convert()
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
                            pygame.image.load(os.path.join(data_folder,'dado1.png')).convert_alpha(),
                            pygame.image.load(os.path.join(data_folder,'dado2.png')).convert_alpha(),
                            pygame.image.load(os.path.join(data_folder,'dado3.png')).convert_alpha(),
                            pygame.image.load(os.path.join(data_folder,'dado4.png')).convert_alpha(),
                            pygame.image.load(os.path.join(data_folder,'dado5.png')).convert_alpha(),
                            pygame.image.load(os.path.join(data_folder,'dado6.png')).convert_alpha(),
                            pygame.image.load(os.path.join(data_folder,'gana.png')).convert_alpha(),  # posic 7: cara ganador
                            pygame.image.load(os.path.join(data_folder,'pierde.png')).convert_alpha()]  # posic 8: cara perdedor
            self.img = self.listimg[self.valor]
        except:
            print ("Error: No se pueden cargar las imagenes de los dados")
            fin_programa()
        try:
            self.sonido = pygame.mixer.Sound(os.path.join(data_folder,'s_dado.ogg'))
        except:
            print ("Error: No se pueden cargar los sonidos de los dados")
            fin_programa()
    def tirar(self):
        self.valor = random.randint(1,6)
        self.img = self.listimg[self.valor]
        self.sonido.play() #Sonido del dado
        pygame.time.wait(int(MSWAIT/2))
    def reinit(self, pos):
        self.valor = 0
        self.posXY = pos
        self.img = self.listimg[self.valor]
        
class cJugador:
    # __init__: el jugador comienza en la casilla 1 y se cargan las imagenes de ficha
    # mover: mueve la ficha tantas posiciones indique el dado, retrocede si se excede de 63
    # turno: define quien es el proximo a tirar los dados (1 o 2)
    # pierdeTurno: define la cantidad de turnos que pierde un jugador
    # posX, posY: coordenadas donde se dibuja la imagen
    turno = 0
    def __init__(self, color, primerPos):
        self.posic = 1
        self.posAnt = 1
        self.posX = tablero.coordX[primerPos]
        self.posY = tablero.coordY[primerPos]
        self.pierdeTurno = 0
        try:
            self.img = pygame.image.load(os.path.join(data_folder,'ficha_'+color+'.png')).convert()
        except:
            print ("Error: No se pueden cargar las imagenes de las fichas")
            fin_programa()

    def mover(self, cantMov, avanza = True): # Le envio a la funcion si tiene que avanzar o retroceder
                                             # por defecto, siempre avanza
        self.posAnt = self.posic # guardo en que posicion estaba antes
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

    def reinit(self,primerPos):
        self.posic = 1
        self.posX = tablero.coordX[primerPos]
        self.posY = tablero.coordY[primerPos]
        self.pierdeTurno = 0

class cEventTexto:
    def __init__(self, txt, pos, color):
        self.dictTxt = {'vacio':'',
                        'inicio':'La primer tirada define que jugador comienza',
                        'ini1':'Comienza el JUGADOR 1',
                        'ini2':'Comienza el JUGADOR 2',
                        'empate':'Empate, vuelve a tirar',
                        'oca':'Oca: avanza hasta la próxima oca y vuelve a tirar',
                        'puente':'Puente: avanza hasta la posada y pierde un turno',
                        'posada':'Posada: la oca descansa. Pierde un turno',
                        'dados':'Dados: se mueve hacia la otra casilla de dados y tira nuevamente',
                        'pozo':'Pozo: la oca se cae al pozo, pierde dos turnos',
                        'lab':'Laberinto: la oca se pierde, retrocede hasta la casilla 30',
                        'carcel':'Carcel: atrapan a la oca, pierde tres turnos',
                        'calavera':'Calavera: la oca vuelve a empezar! Retrocede hasta la casilla 1',
                        'llega':'Jardín de la oca: la oca se reune con su familia. Ganaste!',
                        'mismacasilla': 'Hay otro jugador en la casilla, vuelve a su posición anterior'}
        self.texto = fuente.render (self.dictTxt[txt], True, color)
        self.posXY = pos
    def cambiaTxt (self, txt, color):
        self.texto = fuente.render (self.dictTxt[txt], True, color)

class cTurnoTexto:
    def __init__(self, txt, pos, color):
        self.dictTxt = {'vacio':'',
                        'enter': 'ENTER',
                        'turno1':'CTRL Izq.',
                        'turno2':'CTRL Der.'}
        self.texto = fuente.render (self.dictTxt[txt], True, color)
        self.posXY = pos
    def cambiaTxt (self, txt, color):
        self.texto = fuente.render (self.dictTxt[txt], True, color)
    

# ---- FUNCIONES ----

def define_primero():
    eventosTxt.cambiaTxt('inicio', NEGRO)
    turnoTxt.cambiaTxt('enter', NEGRO)
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
                    turnoTxt.cambiaTxt('turno1', AZUL)
                    cJugador.turno = 1
                    empate = False
                elif (dadoA.valor < dadoB.valor):
                    eventosTxt.cambiaTxt('ini2', ROJO)
                    turnoTxt.cambiaTxt('turno2', ROJO)
                    cJugador.turno = 2
                    empate = False
                else:
                    eventosTxt.cambiaTxt('empate', NEGRO)
                    turnoTxt.cambiaTxt('enter', NEGRO)
                    empate = True
                dibuja_pantalla(False) # Llamo dibuja_pantalla con dos dados
            if event.type == pygame.MOUSEBUTTONDOWN:
                muestra_creditos()

def dibuja_pantalla(unDado=True):
    display.fill(NEGRO)
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
    pygame.display.update()
    clock.tick(60)

def cambia_turno():
    #Verifico si hay algun jugador con turnos perdidos
    if (jugador1.pierdeTurno == 0 and jugador2.pierdeTurno == 0): #Cambio de turno
        if (cJugador.turno == 1):
            turnoTxt.cambiaTxt('turno2', ROJO)
            dibuja_pantalla()
            return 2
        elif (cJugador.turno == 2):
            turnoTxt.cambiaTxt('turno1', AZUL)
            dibuja_pantalla()
            return 1
    elif (jugador1.pierdeTurno > 0): #Decremento turno y devuelvo J2
        jugador1.pierdeTurno -= 1
        turnoTxt.cambiaTxt('turno2', ROJO)
        dibuja_pantalla()
        return 2
    elif (jugador2.pierdeTurno > 0): #Decremento turno y devuelvo J1
        jugador2.pierdeTurno -= 1
        turnoTxt.cambiaTxt('turno1', AZUL)
        dibuja_pantalla()
        return 1                

def casilla_libre(jugAct, jugEsp):
    #jugAct: jugador actual (el que tiro el dado), #jugEsp: jugador en espera
    if (jugAct.posic == jugEsp.posic): #Cayo en la misma casilla que el otro jugador, vuelve a la posición anterior
        eventosTxt.cambiaTxt('mismacasilla', NEGRO)
        pygame.time.wait(MSWAIT)
        jugAct.posic = jugAct.posAnt
        jugAct.posX = tablero.coordX[jugAct.posic]
        jugAct.posY = tablero.coordY[jugAct.posic]
        dibuja_pantalla()
        cJugador.turno = cambia_turno()
        return False
    else:
        return True

def evalua_casilla(jugAct, jugEsp):
    #jugAct: jugador actual (el que tiro el dado), #jugEsp: jugador en espera	
    if jugAct.posic in POS_OCA: #Oca
        eventosTxt.cambiaTxt('oca', NEGRO)
        pygame.time.wait(MSWAIT)
        i = POS_OCA.index(jugAct.posic)
        if jugAct.posic != 59: #En caso de ser la ultima oca, solo tira nuevamente
            jugAct.mover(POS_OCA[i+1]-POS_OCA[i])            
        if (jugEsp.pierdeTurno == 0): #deja pasar el turno solo si tiene turno perdido
           jugEsp.pierdeTurno = 1
        cJugador.turno = cambia_turno()

    elif jugAct.posic in POS_PUENTE: #Puente
        eventosTxt.cambiaTxt('puente', NEGRO)
        pygame.time.wait(MSWAIT)
        jugAct.mover(19 - jugAct.posic)
        if casilla_libre(jugAct, jugEsp): #verifico que no haya nadie en la posada
            jugAct.pierdeTurno = 2
            cJugador.turno = cambia_turno()

    elif jugAct.posic == POS_POSADA: #Posada
        eventosTxt.cambiaTxt('posada', NEGRO)
        pygame.time.wait(MSWAIT)
        if casilla_libre(jugAct, jugEsp): #verifico que no haya nadie en la posada
            jugAct.pierdeTurno = 2
            cJugador.turno = cambia_turno()

    elif jugAct.posic in POS_DADOS: #Dados
        eventosTxt.cambiaTxt('dados', NEGRO)
        pygame.time.wait(MSWAIT)
        if jugAct.posic == 26: #mueve a 53
            jugAct.mover(53 - 26)
        else: #mueve a 26
            jugAct.mover(53 - 26, avanza = False)
        if (jugEsp.pierdeTurno == 0): #deja pasar el turno solo si tiene turno perdido
           jugEsp.pierdeTurno = 1
        cJugador.turno = cambia_turno()

    elif jugAct.posic == POS_POZO: #Pozo
        eventosTxt.cambiaTxt('pozo', NEGRO)
        pygame.time.wait(MSWAIT)
        if casilla_libre(jugAct, jugEsp): #verifico que no haya nadie en el pozo
            jugAct.pierdeTurno = 3
            cJugador.turno = cambia_turno()

    elif jugAct.posic == POS_LAB: #Laberinto
        eventosTxt.cambiaTxt('lab', NEGRO)
        pygame.time.wait(MSWAIT)
        jugAct.mover(POS_LAB - 30, avanza = False)
        if casilla_libre(jugAct, jugEsp): #verifico que no haya nadie en la 30            
            cJugador.turno = cambia_turno()

    elif jugAct.posic == POS_CARCEL: #Carcel
        eventosTxt.cambiaTxt('carcel', NEGRO)
        pygame.time.wait(MSWAIT)
        if casilla_libre(jugAct, jugEsp): #verifico que no haya nadie en la carcel
            jugAct.pierdeTurno = 4
            cJugador.turno = cambia_turno()

    elif jugAct.posic == POS_CALAV: #Calavera
        eventosTxt.cambiaTxt('calavera', NEGRO)
        pygame.time.wait(MSWAIT)
        jugAct.mover(POS_CALAV - 1, avanza = False)
        cJugador.turno = cambia_turno()

    else: #Casilla comun
        if casilla_libre(jugAct, jugEsp): #verifico que no haya nadie en la casilla
            cJugador.turno = cambia_turno()

def hay_ganador(j1, j2):
    if j1.posic == POS_LLEGA:
        eventosTxt.cambiaTxt('llega', NEGRO)
        turnoTxt.cambiaTxt('enter', NEGRO)
        dadoA.img = dadoA.listimg[7]
        dadoB.img = dadoB.listimg[8]
        dibuja_pantalla(False)
        return True
    elif j2.posic == POS_LLEGA:
        eventosTxt.cambiaTxt('llega', NEGRO)
        turnoTxt.cambiaTxt('enter', NEGRO)
        dadoA.img = dadoA.listimg[8]
        dadoB.img = dadoB.listimg[7]
        dibuja_pantalla(False)
        return True
    else:
        return False

def muestra_creditos():
    pygame.draw.rect(display, GRIS, (0,200,750,250))
    tituloTxt = fuenteGrande.render (TXTTITULO, True, AZUL)
    subTxt1 = fuenteChica.render ('El clásico juego de tablero hecho en Python', True, ROJO)
    subTxt2 = fuenteChica.render ('Copyright (C) 2014 Diego Fazio (dfazio80@gmail.com)', True, ROJO)
    subTxt3 = fuenteChica.render ('Bajo licencia GNU...free as in freedom', True, ROJO)
    display.blit(tituloTxt,(20,230))
    display.blit(subTxt1,(20,285))
    display.blit(subTxt2,(20,325))
    display.blit(subTxt3,(20,365))
    pygame.display.update()

    creditos = True
    while creditos:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:    
                dibuja_pantalla()
                creditos = False


def fin_programa():
    pygame.quit()
    sys.exit()

def main():
    while True: #loop infinito
        # defino quien comienza con una tirada de dados inicial 
        define_primero()
        while not hay_ganador(jugador1, jugador2): # loop principal del juego. Termina si hay un ganador
            for event in pygame.event.get(): # eventos de pygame -- deteccion de input de teclado
                if event.type == pygame.QUIT:
                    fin_programa()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LCTRL and cJugador.turno == 1: # Tira dados el jugador 1 con LCTRL
                        eventosTxt.cambiaTxt('vacio', NEGRO)
                        dado.posXY = POSDADO1
                        dado.tirar()
                        jugador1.mover(dado.valor)
                        evalua_casilla(jugador1, jugador2)
                    if event.key == pygame.K_RCTRL and cJugador.turno == 2: # Tira dados el jugador 2 con RCTRL
                        eventosTxt.cambiaTxt('vacio', NEGRO)
                        dado.posXY = POSDADO2
                        dado.tirar()
                        jugador2.mover(dado.valor)
                        evalua_casilla(jugador2, jugador1)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    muestra_creditos()

        # loop secundario que espera si se pulsa la tecla enter para empezar un nuevo juego
        juegadeNuevo = False
        while not juegadeNuevo:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    fin_programa()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    #Reinicio los objetos
                    jugador1.reinit(0)
                    jugador2.reinit(1)
                    dado.reinit((0,0))
                    dadoA.reinit(POSDADO1)
                    dadoB.reinit(POSDADO2)
                    juegadeNuevo = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                        muestra_creditos()
    
# ---- CONSTANTES ----
SIZEXY = (750,650)
POSDADO1 = (645,130)
POSDADO2 = (645,455)
POS_TXT_EVT = (20,605)
POS_TXT_TURNO = (625,605)
MSWAIT = 800
TXTTITULO = 'pyOca '+ VERSION + ' - El juego de la oca'
# casillas especiales
POS_OCA = [5,9,14,18,23,27,32,36,41,45,50,54,59]
POS_PUENTE = [6,12]
POS_POSADA = 19
POS_DADOS = [26,53]
POS_POZO = 31
POS_LAB = 42
POS_CARCEL = 56
POS_CALAV = 58
POS_LLEGA = 63
# colores para los textos (R,G,B)
AZUL = (0,71,255)
ROJO = (255,51,51)
NEGRO = (0,0,0)
GRIS = (179, 179, 179)

# ---- INICIO ----

# inicio pygame y reloj para FPS
pygame.init()
clock = pygame.time.Clock()
# defino carpeta de imagenes y sonido
data_folder = os.path.join(os.path.dirname(__file__), 'data')
# cargo la fuente para el texto
fuente = pygame.font.SysFont('Verdana', 18)
fuenteGrande = pygame.font.SysFont('Verdana', 20)
fuenteChica = pygame.font.SysFont('Verdana', 16)
# inicio ventana
display = pygame.display.set_mode(SIZEXY)
icono = pygame.image.load(os.path.join(data_folder,'icono.png')).convert()
pygame.display.set_icon(icono)
pygame.display.set_caption(TXTTITULO)
# creo los objetos principales del juego
tablero = cTablero()
dado = cDado()
jugador1 = cJugador('azul',0)
jugador2 = cJugador('rojo',1)
eventosTxt = cEventTexto('vacio',POS_TXT_EVT,NEGRO)
turnoTxt = cTurnoTexto('vacio',POS_TXT_TURNO,NEGRO)
# genero dos dados para la primer tirada y para mostrar las caritas
dadoA = cDado()
dadoB = cDado()
dadoA.posXY = POSDADO1
dadoB.posXY = POSDADO2

if __name__ == "__main__":
    main()
