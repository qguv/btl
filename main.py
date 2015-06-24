#!/usr/bin/env python3

import btl
from time import sleep
from sys import exit

def clear(height=200):
    for i in range(height):
        print()

UNKNOWN = '·'
MISS    = ' '
HIT     = '#'

allies  = btl.Field("Allies",  default=UNKNOWN)
enemies = btl.Field("Enemies", default=UNKNOWN)

# place ships
try:

    ships = "Carrier Battleship Destroyer Submarine Patrolboat".split(' ')
    while ships:
        ship = ships[0]

        clear()
        print(allies)

        while True:
            try:
                cell = input("Place {} where? [A1-J10] ".format(ship))
                allies[cell] = ship[0]
                break
            except (IndexError, KeyError, ValueError):
                clear()
                print(allies, "What?", sep='\n', end=' ')

        clear()
        print(allies)

        while True:
            # try:
            direction = input("Which way? [ldru] ")
            allies.place(ship, cell, direction)
            break

        ships.remove(ship)

    clear()
    btl.print_side_by_side(enemies, allies)
    enemies_first = input("Are you going first? [yN] ").lower() != 'y'

except KeyboardInterrupt:
    print("\nQuit before game began!")
    exit(1)

clear()
btl.print_side_by_side(enemies, allies)

allies_have_gone = False

# game loop
while True:

    try:
        # enemies move
        if allies_have_gone or enemies_first:

            move = input("Enemy's move? [a1-j10] ").lower()
            if move:

                if allies[move] in (allies.default, MISS):
                    allies[move] = MISS
                    clear()
                    btl.print_side_by_side(enemies, allies)
                    print(move, "miss!", end=' ')

                else:
                    allies[move] = HIT
                    clear()
                    btl.print_side_by_side(enemies, allies)
                    print(move, "hit!", end=' ')

                input("Press return to continue.")

        clear()
        btl.print_side_by_side(enemies, allies)

        # allies move
        if not allies_have_gone:
            allies_have_gone = True

        while True:
            move = input("Your move? [a1-j10] ").lower()
            if (not move) or enemies[move] == UNKNOWN:
                break
            else:
                input("You already know that cell! Press return.")
                clear()
                btl.print_side_by_side(enemies, allies)
        if move:
            if input("Hit? [yN] ").lower() != 'y':
                enemies[move] = MISS
            else:
                enemies[move] = HIT
                if input("Sink? [yN] ").lower() == 'y':
                    enemies[move] = input("Sink what? ")[0]

        clear()
        btl.print_side_by_side(enemies, allies)

    except EOFError:
        try:
            while True:
                clear()
                btl.print_side_by_side(enemies, allies)

                cell_raw = input("Which square? [e or a] + [a1-j10] ")
                team, cell = cell_raw[0], cell_raw[1:]
                board = allies if team.lower() == 'a' else enemies

                board[cell] = input("Change to what? ")
        except (KeyboardInterrupt, EOFError):
            print()
            continue
    except KeyboardInterrupt:
        print()
        exit(0)
