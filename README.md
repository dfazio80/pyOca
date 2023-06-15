Juego de la Oca
===============

**Autor:** Diego Fazio
**Lenguaje:** Python 3.3 32bit + Pygame 1.9.2
**Fecha:** 22/01/14

Versiones:
1.0	Documento Inicial
1.1	Cambio del juego a 1(un) dado, y alteraciones en algunas casillas especiales

Requisitos:
Python 3.x
Pygame

Elementos del juego:
Una ficha por jugador (inicialmente para dos jugadores)
Un dado
Tablero del juego

Reglas:
1.	Cada jugador lanza el dado la primera vez, para definir quien comienza. El jugador con la tirada más alta comenzará primero. En caso de empate, se vuelve a tirar.
2.	Ambos jugadores comienzan en la casilla número 1.
3.	Se arroja el dado y se avanza la cantidad de casillas que indique el dado
4.	Si un jugador debe avanzar a una casilla ya ocupada por otro jugador, debe permanecer donde está.
5.	Si se cae en alguna de las casilla especiales, se debe cumplir el premio o castigo correspondiente.
6.	Para entrar en la casilla 63 es necesario sacar el número exacto, si se excede se retrocede la cantidad de casilleros como se haya pasado.
7.	Gana el primer jugador que entre en la casilla 63.

Casillas especiales:
Existen casillas con premios y castigos, se listan a continuación

OCA (5, 9, 14, 18, 23, 27, 32, 36, 41, 45, 50, 54, 59): se avanza hasta la siguiente casilla que tenga una OCA y se vuelve a tirar.
PUENTE (6,12): se avanza hasta la casilla 19 y se pierde un turno.
POSADA (19): se pierde un turno.
DADOS (26,53): se avanza hacia la siguiente casilla de dados (si es 26), o se vuelve a la casilla de dados anterior (si es 53), en ambos casos, se vuelve a tirar.
POZO(31): se pierden dos turnos.
LABERINTO(42): se retrocede hasta la casilla 30.
CARCEL (56): se pierden tres turnos.
CALAVERA(58): vuelve a la casilla 1.

Licencia:
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Graficos y sonidos descargados de:
http://openclipart.org/
http://freesound.org/
