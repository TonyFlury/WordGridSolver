==============
WordGridSolver
==============

A simplish app to solve word grids such as those found in the Words Smart puzzle game - and others.

The Game
--------

The game displays a square grid of letters (e.g.) :

.. line-block::

 RWET
 CHAA
 ATLC
 SETE


and an indication of the number of words to find and their lengths - in the above grid, the indicated words are 6,3 & 7 letters long.

A word is found by tracing a path across the grid from letter to letter - moving up, dowm, left, right and diagonally. Letters cannot be re-used within a word. If the correct word is traced the letters are removed from the grid, and the rest of the grid falls into the gaps. This collapse step significantly changes the available paths through the grid - making some words traceable which weren't traceable before. It is the intention that most grids are solved in the order that the word lengths are specified.

A grid may support more than one set of words which match the indicated word lengths, but the game only accepts one set of words as the 'right' answer.

The App
-------

Given a set of word lengths, the App peforms an exhaustive search of all possible paths from
all possible starting positions for a path of the length of the first word length, forming a character string from the grid from each path. Each character string is tested against the system dictionary '/etc/dictionaries-common/words', and if the character string is a real word, then that word is removed from a copy of the grid, and a search is carried out for the next word, and so on until all words are found.

If the search fails (i.e. a valid word isn't found) then the grip collapse is rolled back, and the process continues with the next path :

.. code-block::

  Psuedo code :
        For each possible path in the grid
            if resulting text is a word -
                    create a copy of the grid,
                    remove the found word,
                    if there are word left to be found
                        collapse the grid and repeat above but for the next word length.
                        generate the found word, and any found from the collapsed grid
                    if there are no remaining word lengths, generate just the word found.

For the above grid, the algorithm looks at a total of 37696 paths across the grid, and finds the words
'castle', 'cat' and 'weather'.