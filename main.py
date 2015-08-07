#!/usr/bin/env python3

import btl
import prompt
from sys import exit
from itertools import cycle

UNKNOWN = '·'
MISS    = ' '
HIT     = '#'

allies  = btl.Field("Allies",  default=UNKNOWN)
enemies = btl.Field("Enemies", default=UNKNOWN)

# main
try:
    ships = "Carrier Battleship Destroyer Submarine Patrolboat".split(' ')
    for ship in ships:
        prompt.place_ship(ship, allies)

    btl.clear()
    btl.print_side_by_side(enemies, allies)
    enemies_first = input("Are you going first? [yN] ").lower() != 'y'
    is_enemy_move = cycle( (True, False) if enemies_first else (False, True) )

except KeyboardInterrupt:
    print("\nQuit before game began!")
    exit(1)

btl.clear()
btl.print_side_by_side(enemies, allies)

allies_have_gone = False

# game loop
while True:

    try:
        btl.clear()
        btl.print_side_by_side(enemies, allies)

        if next(is_enemy_move):
            prompt.enemy_move(allies)
        else:
            prompt.ally_move(enemies)

    except EOFError:
        # the generator was advanced one too many times, as we're skipping the
        # "current" move, so we must reset it to its previous state, identical
        # to its next state; yeah generators; yeah itertools; yeah science
        next(is_enemy_move)

        try:
            while True:
                btl.clear()
                btl.print_side_by_side(enemies, allies)

                cell_raw = input("Which square? [e or a] + [a1-j10] ")
                team, cell = cell_raw[0], cell_raw[1:]
                board = allies if team.lower() == 'a' else enemies

                board[cell] = input("Change to what? ")

        except (EOFError, IndexError):
            print()
            continue

        except KeyboardInterrupt:
            print()
            exit()

    except KeyboardInterrupt:
        print()
        exit(0)
