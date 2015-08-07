#!/usr/bin/env python3

from btl import clear

UNKNOWN = '·'
MISS    = ' '
HIT     = '#'

def place_ship(ship, board):
    clear()
    print(board)
    while True:
        try:
            cell = input("Place {} where? [A1-J10] ".format(ship))
            board[cell] = ship[0]
            break
        except (IndexError, KeyError, ValueError):
            clear()
            print(board, "What?", sep='\n', end=' ')

    clear()
    print(board)
    direction = input("Which way? [ldru] ")

    board.place(ship, cell, direction)

def ally_move(enemy_board):
    while True:
        move = input("Your move? [a1-j10] ").lower()
        if (not move) or enemy_board[move] == UNKNOWN:
            break
        else:
            print("You already know that cell!", end=' ')
            input("Press return.")
    if move:
        if input("Hit? [yN] ").lower() != 'y':
            enemy_board[move] = MISS
        else:
            enemy_board[move] = HIT
            if input("Sink? [yN] ").lower() == 'y':
                enemy_board[move] = input("Sink what? ")[0]

    return bool(move)

def enemy_move(allied_board):
    move = input("Enemy's move? [a1-j10] ").lower()
    if move:

        if allied_board[move] in (allied_board.default, MISS):
            allied_board[move] = MISS
            print(move, "miss!", end=' ')

        else:
            allied_board[move] = HIT
            print(move, "hit!", end=' ')

        input("Press return to continue.")

    return bool(move)
