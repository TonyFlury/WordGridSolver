#!/usr/bin/env python3
# coding=utf-8
"""
# WordGridSolver : Implementation of solver.py

Summary : 
    <summary of module/class being implemented>
Use Case : 
    As a <actor> I want <outcome> So that <justification>

Testable Statements :
    Can I <Boolean statement>
    ....
"""
import itertools
import sys
import copy
from math import sqrt

__version__ = "0.1"
__author__ = 'Tony Flury : anthony.flury@btinternet.com'
__created__ = '10 Jun 2016'

path_count = 0

class Grid(object):
    def __init__(self, grid, dictionary, word_sizes):
        """
        Basic word grid.
        """
        self._grid = grid
        self._size = len(grid)
        self._dictionary = dictionary
        self._word_sizes = word_sizes

    def _find_path_from(self, length, current_path):
        """given the current_path and therefore a start point of the last item in current_path
           find ALL possible paths of length through the grid

           A path is possible if :
               * each step is a move diagonally or laterally from  the previous position
               * each step consumes a letter (and not a cell with a ' ')
               * each step stays in the bounds of the grid.

            A recursive generator returning each possible path. Return/Yield -1 if there is no possible path
            from this point
           """
        global path_count
        start = current_path[-1]

        found_path = False

        for d in [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]:
            x, y = start[0] + d[0], start[1] + d[1]

            if x < 0 or x >= self._size:  # x co-ord out of bounds
                continue
            if y < 0 or y >= self._size:  # y co-ord out of bounds
                continue

            if (x, y) in current_path:  # Already in this route
                continue

            if self._grid[x][y] == " ":  # No letter there
                continue

            found_path = True

            if length == 1:
                path_count += 1
                sys.stdout.write("\r{0} {1:>10} paths".format('\|-/'[path_count %4], path_count))
                sys.stdout.flush()
                yield current_path + [(x,y)]
            else:
                for p in self._find_path_from(length-1, current_path+[(x,y)]):
                    yield p

        if not found_path:
            yield -1

    def find_paths(self, length):
        """
        For the grid generate all paths of a specific length from every legal starting point
        """
        for r in range(0, self._size):
            for c in range(0, self._size):
                if self._grid[r][c] == " ":
                    continue

                for p in  self._find_path_from(length-1, [(r,c)]):
                    if p == -1:
                        continue
                    else:
                       yield list(p)

    def get_text(self, path):
        """Convert a path into an actual text string"""
        path = list(path)
        return "".join(self._grid[p[0]][p[1]] for p in path)

    def __str__(self):
        """Print the Grid into an upper case """
        return "\n".join(''.join(c.upper() for c in r) for r in self._grid)

    def collapse(self, path):
        """Remove letters from the grid for a given path, and shuffle everything down
        """
        # Part 1 - blank out the path
        for loc in path:
            self._grid[loc[0]][loc[1]] = " "

        # Part2 - bubble letters down
        for c in range(self._size):
            txt = "".join(self._grid[r][c] for r in range(self._size) if self._grid[r][c] != " ")
            txt = " "*(self._size - len(txt)) + txt
            for r in range(self._size):
                self._grid[r][c] = txt[r]

    def find_words(self, index=0):
        """ Find words which comply to the word length as indexed.

            Pseudo code :
                for every possible path, check if resulting text is a word.
                if it is a word - collapse the grid and repeat for the next word length.
                if there are no remaining word lengths, generate just the word found.

            Generate -1 when there are no matches for this word length or subsequent ones.
        """

        found = False

        if index >= len(self._word_sizes):
            return

        for p in self.find_paths(self._word_sizes[index]):
            w = self.get_text(p)
            if w in self._dictionary:
                found = True
                if index+1 == len(self._word_sizes):
                    yield [w]
                else:
                    grid_copy = copy.deepcopy(self)
                    grid_copy.collapse(p)
                    for nw in grid_copy.find_words(index+1):
                        if nw == -1:
                            yield -1
                        else:
                            yield [w] + nw
                    del grid_copy

        if not found:
            yield -1

def capture_sizes():
    # Capture the word sizes
    word_sizes = input('Word sizes > ').split(',')
    word_sizes = [int(s.strip()) for s in word_sizes]
    size = int(sqrt(sum(word_sizes)))
    return word_sizes, size

def capture_grid(size):
    # Capture the grid
    grid = []

    for i in range(size):
        valid = False
        while not valid:
            row = input('Grid Row {} > '.format(i + 1))
            row = [c for c in row]
            if len(row) != size:
                print("Not enough letters - need {} per row".format(size))
            else:
                valid = True
        grid.append(row)
    return grid

def grab_dictionary():
    """Grab the dictionary into a dict
      Searching a dictionary is marginally quicker than an equivalent sized set

        $ python -m timeit -s 'fp = open("/etc/dictionaries-common/words","r")' -s "l = {w.strip():1 for w in fp.readlines() if not w.strip().endswith('s')}" -s 'fp.close()' '"autumn" in l'
        10000000 loops, best of 3: 0.0312 usec per loop

        $ python -m timeit -s 'fp = open("/etc/dictionaries-common/words","r")' -s "l = {w.strip() for w in fp.readlines() if not w.strip().endswith('s')}" -s 'fp.close()' '"autumn" in l'
        10000000 loops, best of 3: 0.0321 usec per loop
    """
    with open('/etc/dictionaries-common/words','r') as fp:
        dict_list = fp.readlines()
    return {w.strip():1 for w in dict_list if not w.strip().endswith("'s")}

if __name__ == "__main__":

    word_sizes, size = capture_sizes()

    # Capture the grid
    grid = capture_grid(size)
    dictionary = grab_dictionary()

    # Build the initial grid object
    g = Grid(grid, dictionary=dictionary, word_sizes=word_sizes)

    print ("*****************")
    print ("*  The Grid     *")
    print ("-----------------")
    print (g)
    print ("*****************")
    print ('Solving ....')

    print("")

    s = sorted(list(set(tuple(w) for w in g.find_words() if w != -1)))

    if s:
        print("\nFound Solutions (in order) : ", end="\n")
        print('\n'.join( ",".join(w for w in item) for item in s))
    else:
        print("\nNo Solutions Found")