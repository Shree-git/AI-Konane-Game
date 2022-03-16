# One Konane object contains one player's information in a Konane game.
#
# The 'move' method returns your move.  Put your code there!
#
#  At initialization, save the initial state of the game, plus
#  some other useful information:
#    board = game board
#    who = the current player 'o' or 'x'
#    other = the other player 'x' or 'o'
#
import random
import konaneutils as U

class Konane:
    def __init__(self, board, who):
        self.board = board
        self.who = who
        self.other = {'x':'o', 'o':'x'}[who]
   
    #  Move command.  It should return a 4-tuple containing
    #  the move that it thinks is best for the 'who' player
    def move(self):
        # Optional debugging write
        print("Score when move is called:" , self.simple_score(self.board))

        # All possible moves I can make
        mymoves = U.genmoves(self.board, self.who)

        # Optional for debugging: Print available moves
        print("available moves")
        for n in mymoves:
            print(n.mover, "moves ", n.move)

        #--------------------------------------------------------------------------------------
        # YOUR CODE REPLACES THIS SECTION


        who = self.who
        board = self.board
        newMoves = [(self.minimax(who, n, -1000, 1000, 0, 3), n.move) for n in mymoves]

        newMoves = sorted(newMoves)

        #
        #random.shuffle(mymoves)          # Use this to pick a random move
        #mymove = mymoves[-1].move        #   instead of the code below.

        # Make a list of (score, move) tuples for each of the
        #  possible successor boards
        #movesWithScore = [(self.simple_score(n.b), n.move) for n in mymoves]

        # Sort will put in order of the score (the first item in each tuple)
        #movesWithScore = sorted(movesWithScore)

        # Optional for debugging: print all the available moves with their scores
        for ms in newMoves:
            print("Score: ", ms)

        # Extract the move from the tuple at the end of the list (highest score)
        
        score, mymove = newMoves[-1]
        #random.shuffle(mymoves) 
        #mymove = mymoves[-1].move 
        #score, extra = nodeWithScore
        print(self.who, "picked move", mymove, "with score", score)
        #
        # YOUR CODE ENDS HERE
        #-------------------------------------------------------------------------

        # level = 3
        # values = []
        # alpha = -float("inf")
        # for move in mymoves:
        #     values.append(self.)

        return mymove


    # Simple scoring function
    #
    # Compute the number of moves available for the 'who' player, minus the
    # number of moves available for the 'other' player.
    # Exception: if this position is a win or a loss, return +/- 1000
    #
    # YOU MIGHT HAVE A MORE SOPHISTICATED SCORING FUNCTION
    #
    def simple_score(self, board):
        return len(U.genmoves(board, self.who)) - len(U.genmoves(board, self.other))

    def simple_score2(self, board):
        a = len(U.genmoves(board, self.who))
        b = len(U.genmoves(board, self.other))
        if a == 0:
            return -100000000
        if b == 0:
            return 100000000
        return a - b    

        

    def gameDone(self, mover):
        return U.gameDone(self.board, mover)



    def minimax(self, who, board, alpha, beta, r, depth):
        loop = depth
        if r == loop or self.gameDone(who):
            return self.simple_score2(board.b)
        mymoves = U.genmoves(board.b, who)
        integer = 5
        if who == self.who:
            for ms in mymoves:
                s = r + 1
                childScore = self.minimax(self.other, ms, alpha, beta, s, depth)
                setMoveScore = max(childScore, alpha)
                alpha = setMoveScore
                integer = alpha
                if alpha >= beta: break
        else:
            for ms in mymoves:
                s = r + 1
                childScore = self.minimax(self.who, ms, alpha, beta, s, depth)
                setMoveScore = min(childScore, beta)
                beta = setMoveScore
                integer = beta
                if beta <= alpha: break
        return integer  


            
