#!/bin/env python3
#
# Konane manual operation main program.
#
# Usage: ./konaneman usermodule
#
#  It will load usermodule.py (put YOUR user module name)
#  and use the Konane method from inside.
#
import sys
import os.path
import konaneutils as U

#  Prompt the user for a board location (e.g. '3d'), and
#  keep prompting until the user types a valid location.
#
#  Inputs:  prompt     a prompt string
#           sqcontain  what the square should contain
#
#  Returns  row, col
#
def get_move_from_command_line(prompt, sqcontain, board):
    while 1:
        s = input(prompt).strip().lower()
        if s == 'quit' or s == 'exit': sys.exit(0)
        if not len(s) == 2: continue
        s1 = s[0]
        s2 = s[1]
        if s1.isalpha() and s2.isdigit():
            s2, s1 = s1, s2
        elif not s1.isdigit() and s2.isalpha():
            continue
        if not ('0' <= s1 and s1 <= '7'):
            continue
        if not ('a' <= s2 and s2 <= 'h'):
            continue
        row = int(s1)
        col = 'abcdefgh'.index(s2)
        if not board[row][col] == sqcontain:
            if sqcontain == ' ': sqcontain = 'blank'
            print("Square should contain ", sqcontain)
            continue
        return (row, col)
    

#  Encode a move (four numbers) into two board positions
#
def encode_move(from_row, from_col, to_row, to_col):
    if not (0 <= from_row and from_row <= 7 and
            0 <= to_row and to_row <= 7 and
            0 <= from_col and from_col <= 7 and
            0 <= to_col and to_col <= 7):
        print("Illegal move from=(%d,%d) to=(%d,%d)" % \
               (from_row, from_col, to_row, to_col))
        sys.exit(1)
    else:
        return str(from_row) + 'abcdefgh'[from_col] + ' ' + \
               str(to_row)  + 'abcdefgh'[to_col]


#  Place the move on the board.  Return None if move is not possible.
#  If the move is possible, the board is modified.
#
#  Inputs are:
#     board
#     sq       the player in question, 'x' or 'o'
#     othersq  the player being jumped over
#     from_row
#     from_col
#     to_row
#     to_col
#
#  make_move leaves . (dot) in place of the removed pieces, and
#  capitalizes the moved piece for emphasis.  cleanup_move() is
#  called to clean this stuff up after printing.
#
def make_move(board, sq, othersq, from_row, from_col, to_row, to_col):
    if not board[from_row][from_col] == sq: return None
    if not board[to_row][to_col] == ' ': return None
    (jump_over, jump_land) = jumppath(from_row, from_col, to_row, to_col)
    if not jump_over: return None
    for i,j in jump_over:
        if not board[i][j] == othersq: return None
    for i,j in jump_land:
        if not board[i][j] == ' ': return None
    for i,j in jump_over:
        board[i][j] = '.'
    for i,j in jump_land:
        board[i][j] = '.'
    board[to_row][to_col] = sq.capitalize()
    board[from_row][from_col] = '.'
    return 1

#  Cleanup_move cleans out the emphasis characters left by make_move
#
def cleanup_move(b):
    for i in range(len(b)):
        for j in range(len(b[i])):
            char = b[i][j]
            if char == '.' or char == '*':
                b[i][j] = ' '
            else:
                b[i][j] = b[i][j].lower()



#  Compute the squares being jumped over in a proposed move.
#  Returns two lists:
#    (i,j) tuples of the jumped-over positions.
#    (i,j) tuples of the intermediate landing positions
#
def jumppath(from_row, from_col, to_row, to_col):
    if from_row == to_row:
        jump_over = [(to_row, j) for j \
            in range(min(from_col, to_col)+1, max(from_col, to_col), 2)]
        jump_land = [(to_row, j) for j \
            in range(min(from_col, to_col)+2, max(from_col, to_col), 2)]
        return (jump_over, jump_land)
    elif from_col == to_col:
        jump_over = [(i, to_col) for i \
            in range(min(from_row, to_row)+1, max(from_row, to_row), 2)]
        jump_land = [(i, to_col) for i \
            in range(min(from_row, to_row)+2, max(from_row, to_row), 2)]
        return (jump_over, jump_land)

    else:
        return (None, None)



#  Populate the board
def populate_board():
    pieces = ['x', 'o']
    board = []
    polarity = 0
    for i in range(8):
        onerow = []
        for j in range(4):
            onerow.append(pieces[polarity])
            onerow.append(pieces[1-polarity])
        board.append(onerow)
        polarity = 1-polarity

    board[3][3] = ' '
    board[3][4] = ' '
    return board

#  A simple function to print the board
#
def print_board(b):
    print('  a b c d e f g h')
    
    for i in range(len(b)):
        r = ' '.join(b[i])
        print(str(i) + ' ' + r)

# Load user module
#  
def getmodule(filename):
    modname, ext = os.path.splitext(filename)
    try:
        modul = __import__(modname)
    except ImportError:
        print("Cannot import", modname)
        sys.exit(0) 
    return modul

# ----------- MAIN PROGRAM STARTS HERE
#
# load module 
if len(sys.argv) < 2:
   print("usage: ./konaneman usermodule.py")
   sys.exit(0)
modul = getmodule(sys.argv[1])

# Initialize board
board = populate_board()
K = modul.Konane(board, 'o')

while 1:
    winner = 'o'
    print_board(board)
    cleanup_move(board)
    if U.gameDone(board, 'x'): break
    from_row, from_col = get_move_from_command_line("Move From: ", "x", board)
    to_row, to_col = get_move_from_command_line("Move To: ", " ", board)
    if not make_move(board, "x", "o", from_row, from_col, to_row, to_col):
        print("Illegal Move")
        continue

    winner = 'x'
    print_board(board)
    cleanup_move(board)
    if U.gameDone(board, 'o'): break    
    print_board(board)
    from_row, from_col, to_row, to_col = K.move()
    print("Computer moves", encode_move(from_row, from_col, to_row, to_col))
    if not make_move(board, "o", "x", from_row, from_col, to_row, to_col):
        print("Illegal Move forfeited")
        continue

print("Winner is:", winner)

