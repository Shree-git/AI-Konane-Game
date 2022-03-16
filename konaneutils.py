# Useful CS 345 Konane Board Routines
#
#-------------------------------------------------------------------------
# Node object is one node of the game tree.  It contains:
#    a board
#    the mover who produced that board ('x' or 'o')
#    the move that produced in that board (a four-number tuple)
#
# There is no need to keep structural tree information (pointers to 
# parent, children) because the Minimax algorithm generates and
# explores nodes as it traverses the tree. 
#
#------------------------------------------------------------------------------
#
# Functions that utilize a game board in progress:
#
# print_board:  Prints the board to stdout
#
# genmove: from a board and a player,
#          produce list of Node objects with all possible moves
#
# gameDone: from a board and a player, return True if there are no moves
#           for that player
#
# moveable: from an x,y position and a board, True if there is at least
#           one available move from that position.
#
# make_succ: from a board and the x,y starting and ending points, make
#           a new board, encapsulated in a new node.
#
#------------------------------------------------------------------------------
# Functions that don't reference the current game board.
#
# each_players_places: produce two lists, one for each player, of the
#           board positions that belong to that player
#
# jumppath: from a proposed x,y starting position to an x,y ending
#           position, return the squares that are landed on and the
#           squares that are jumped over.
#
# dests_from: from an x,y starting position, all possible jump destinations
#
#------------------------------------------------------------------------------
#
class Node:
    def __init__(self, b, mover, move):
        self.b = b
        self.mover = mover
        self.move = move # A tuple of from_row, from_col, to_row, to_col

#------------------------------------------------------------------------------
#  A simple function to print the board
#
def print_board(b):
    print('  a b c d e f g h')
    
    for i in range(len(b)):
        r = ' '.join(b[i])
        print(str(i) + ' ' + r)

#------------------------------------------------------------------------------
#  gameDone command
#  It will check whether the game is finished for a particular mover and board
#  Returns boolean True if the game is over
#
def gameDone(b, mover):
    global places
    for from_row, from_col in places[mover]:
        if moveable(from_row, from_col, b):
            return None
    return True

#------------------------------------------------------------------------------
#  Generate all possible moves
#  Returns list of Nodes of successor moves.
#
def genmoves(b, mover):
    global places   # Assuming you put this in a global variable
    successors = []

    # For each places that mover can be
    for from_row, from_col in places[mover]:
        if not moveable(from_row, from_col, b): continue
        
        # generate all the destinations the mover can jump to 
        dests = dests_from(from_row, from_col)

        # And make a successor node for valid move
        for to_row, to_col in dests:
            succ = make_succ(b, mover, from_row, from_col, to_row, to_col)
            if succ:
                successors.append(succ)
    return successors

#------------------------------------------------------------------------------
#  List of all possible board positions for each player
#
#  Returns a dictionary.
#   places['x'] = [ (0,0), (0,2), ... (7,6) ] # All of X player's squares
#   places['o'] = [ (0,1), (0,3), ... (7,7) ] # All of O player's squares
#
#  Call this once at the beginning of your program.
#  (So you don't call it repeatedly every time you want to move)
#
def each_players_places():
    global places
    places = {'x':[], 'o':[]}
    for i in range(8):
        for j in range(0,8,2):
            if i%2 == 0:
                places['x'].append((i, j))
                places['o'].append((i, j+1))
            else:
                places['o'].append((i, j))
                places['x'].append((i, j+1))
    return places

# Populate the global variable
places = each_players_places()

#------------------------------------------------------------------------------
# Determine whether a piece is moveable
#
# b is a board (the list of lists)
#
# Returns None if there are no moves available from
#   (from_row, from_col).
#   
def moveable(from_row, from_col, b):
    if b[from_row][from_col] == ' ': return None
    if from_row > 1:
        if (not b[from_row-1][from_col] == ' ') and \
            (b[from_row-2][from_col] == ' '): return 1
    if from_row < 6:
        if (not b[from_row+1][from_col] == ' ') and \
            (b[from_row+2][from_col] == ' '): return 1
    if from_col > 1:
        if (not b[from_row][from_col-1] == ' ') and \
            (b[from_row][from_col-2] == ' '): return 1
    if from_col < 6:
        if (not b[from_row][from_col+1] == ' ') and \
            (b[from_row][from_col+2] == ' '): return 1
    return None

#------------------------------------------------------------------------------
#  Compute the squares being jumped over in a proposed move.
#
#  Jumps must be vertical or horizontal, so either the x postion
#  is the same (horizontal jump) or the y position is the same
#
#  lorow, lowcol  x,y for the lowest number row,col position
#  hirow, hicol   x,y for the highest number row,col position
#
#  Returns two lists:
#    (i,j) tuples of the jumped-over positions.
#    (i,j) tuples of the intermediate landing positions
#
def jumppath(lorow, locol, hirow, hicol):
    if lorow == hirow:
        jump_over = [(hirow, j) for j in range(locol+1, hicol, 2)]
        jump_land = [(hirow, j) for j in range(locol+2, hicol, 2)]
        return (jump_over, jump_land)
    elif locol == hicol:
        jump_over = [(i, hicol) for i in range(lorow+1, hirow, 2)]
        jump_land = [(i, hicol) for i in range(lorow+2, hirow, 2)]
        return (jump_over, jump_land)
    else:
        return (None, None)

#------------------------------------------------------------------------------
# For one starting position, all possible jump destinations
#
# (This is all possible destinations, regardless of whether
#  they are possible jumps in the current game)
#
def dests_from(from_row, from_col):
    dests = []
    for j in range(from_col%2, 8, 2):
        if not j==from_col:
            dests.append((from_row, j))
            
    for i in range(from_row%2, 8, 2):
        if not i==from_row:
            dests.append((i, from_col))
    return dests

#------------------------------------------------------------------------------
# Make successor node. 
#   Input is curent board and the proposed move (from and to), 
#   Output is one of these:
#       The resulting new board, in a Node object (move is valid)
#       None (the move is not possible)
#
def make_succ(b, mover, from_row, from_col, to_row, to_col):
    if not b[to_row][to_col] == ' ': return None

    locol, hicol = min(from_col, to_col), max(from_col, to_col)
    lorow, hirow = min(from_row, to_row), max(from_row, to_row)

    (jump_over, jump_land) = jumppath(lorow, locol, hirow, hicol)
    if not jump_over: return None
    for i,j in jump_over:
        if b[i][j] == ' ': return None
    for i,j in jump_land:
        if not b[i][j] == ' ': return None

    # Build a copy of the board, copying only those rows that are affected.
    newb = b[:]
    for i in range(lorow, hirow+1):
        newb[i] = b[i][:]

    for i,j in jump_over:
        newb[i][j] = ' '
    newb[to_row][to_col] = mover
    newb[from_row][from_col] = ' '
    return Node(newb, mover, (from_row, from_col, to_row, to_col))
