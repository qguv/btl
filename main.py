#!/usr/bin/env python3

import btl
from time import sleep

def clear(height=200):
    for i in range(height):
        print()

UNKNOWN = '·'
MISS    = ' '
HIT     = '#'

allies  = btl.Field("Allies",  default=UNKNOWN)
enemies = btl.Field("Enemies", default=UNKNOWN)

lengths = {"p": 2,
           "d": 3,
           "s": 3,
           "b": 4,
           "c": 5}

place_fns = {"l": allies.place_left,
             "d": allies.place_down,
             "r": allies.place_right,
             "u": allies.place_up}

# main script functionality
try:

    # place ships
    ships = list("pdsbc")
    while ships:
        clear()
        print(allies)

        while True:
            try:
                abbr = input("Which ship? [{}] ".format(''.join(ships)))[0]
                length = lengths[abbr]
                ships.remove(abbr)
                break
            except (IndexError, KeyError, ValueError):
                clear()
                print(allies, "What?", end=' ')

        clear()
        print(allies)

        while True:
            try:
                cell = input("Where? [a1-j10] ").lower()
                allies[cell] = abbr.upper()
                break
            except (IndexError, KeyError):
                clear()
                print(allies, "What?", end=' ')

        clear()
        print(allies)

        while True:
            try:
                place_fn = place_fns[input("Which way? [ldru] ").lower()]
                place_fn(abbr.upper(), cell, length)
                break
            except KeyError:
                clear()
                input(allies, "What?", end=' ')

    clear()
    btl.print_side_by_side(enemies, allies)
    enemies_first = input("Are you going first? [yN] ").lower() != 'y'

    clear()
    btl.print_side_by_side(enemies, allies)

    allies_have_gone = False

    # game loop
    while True:

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

except KeyboardInterrupt:
    clear()
    btl.print_side_by_side(enemies, allies)
