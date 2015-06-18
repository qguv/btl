#!/usr/bin/env python3

from itertools import zip_longest

def print_side_by_side(a, b, sep=' ', fill=' ', empty=' ', fill_right=False, really_print=True):
    alines = str(a).split('\n')
    blines = str(b).split('\n')
    amax = len(max(alines, key=len))
    bmax = len(max(blines, key=len))

    lines = []
    for aline, bline in zip_longest(alines, blines, fillvalue=None):
        s = ' '
        if aline is None:
            s += empty * amax
        else:
            s += aline
            s += fill * (amax - len(aline))

        s += sep

        if bline is None:
            if fill_right:
                s += empty * bmax
        else:
            s += bline
            if fill_right:
                s += fill * (bmax - len(bline))
        lines.append(s)

    lines = '\n'.join(lines)
    if not really_print:
        return lines
    print(lines)

def col_row_from_str(s):
    col = ord(s[0].lower()) - ord('a')
    row = int(s[1:]) - 1
    return (col, row)

class Field:
    def __init__(self, name, size=10, default='.', sep=' '):
        self.array = [default] * (size * size)
        self.default = default
        self.name = name
        self.size = size
        self.sep = sep

    def __str__(self):

        # length of row-number column is the length of the longest number
        digits = len(str(self.size + 1))

        # represents the lowest letter column
        a = ord('a')

        # the string begins with a blank numeric column
        s = ' ' * digits

        # a space separates the numeric column and the letter column names
        s += ' '

        # the column names are single letters
        s += self.sep.join([ chr(a + i) for i in range(self.size) ])

        # center a header with the field's name above the letter indexes
        name_padding = (len(s) - len(self.name)) // 2 * ' '
        s = '\n' + name_padding + self.name.upper() + '\n' + s

        # for each row
        for row in range(self.size):
            s += '\n'

            # build the row number
            n = str(row + 1)

            # pad with spaces on the left side of the number
            num_padding = ' ' * (digits - len(n))
            s += num_padding + n
            
            # a space separates the numeric column and the field row
            s += ' '

            # print the field row
            first = row * self.size
            last = (row + 1) * self.size
            s += self.sep.join(self.array[first:last])
        return s

    def cell_index_from_str(self, key):
        col, row = col_row_from_str(key)
        return row * self.size + col

    def __getitem__(self, key):
        return self.array[self.cell_index_from_str(key)]

    def __setitem__(self, key, value):
        self.array[self.cell_index_from_str(key)] = value

    def place_ship(self, abbr, at, length, vertical=False, reverse=False):
        '''Give this method the top-left point of the ship.'''

        if vertical:
            delta = self.size
        else:
            delta = 1

        if reverse:
            delta *= -1

        i = self.cell_index_from_str(at)
        while length > 0:
            self.array[i] = abbr
            length -= 1
            i += delta

    def place_right(self, abbr, at, length):
        return self.place_ship(abbr, at, length)
    def place_left(self, abbr, at, length):
        return self.place_ship(abbr, at, length, reverse=True)
    def place_down(self, abbr, at, length):
        return self.place_ship(abbr, at, length, vertical=True)
    def place_up(self, abbr, at, length):
        return self.place_ship(abbr, at, length, vertical=True, reverse=True)
