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
        print("Available moves")
        for n in mymoves:
            print(n.mover, "moves ", n.move)

        #--------------------------------------------------------------------------------------
        # YOUR CODE REPLACES THIS SECTION
        #
        # random.shuffle(mymoves)          # Use this to pick a random move
        # mymove = mymoves[-1].move        #   instead of the code below.
        nMoves = [(self.minimax(self.who, n, -1000, 1000, 0, 3), n.move) for n in mymoves]
        nMoves = sorted(nMoves)
        # Make a list of (score, move) tuples for each of the
        #  possible successor boards
        mScore = [(self.simple_score(n.b), n.move) for n in mymoves]

        # Sort will put in order of the score (the first item in each tuple)
        mScore = sorted(mScore)

        # Optional for debugging: print all the available moves with their scores
        for x in mScore:
            print("Scored move", x)

        # Extract the move from the tuple at the end of the list (highest score)
        myscore, mymove =mScore[-1]
        print(self.who, "picked move", mymove, "with score", myscore)
        #
        # YOUR CODE ENDS HERE
        #-------------------------------------------------------------------------

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

    def gameDone(self, mover):
        return U.gameDone(self.board, mover)

    def minimax(self, who, board, alpha, beta, ran, depth):
        if ran == depth or self.gameDone(who):
            return self.simple_score(board.b)
        moves = U.genmoves(board.b, who)
        temp = 5
        if who == self.who:
            for x in moves:
                s = ran + 1
                cScore = self.minimax(self.other, x, alpha, beta, s, depth)
                setScore = max(cScore, alpha)
                alpha = setScore
                temp = alpha
                if alpha >= beta: 
                    break
        else:
            for x in moves:
                s = ran + 1
                cScore = self.minimax(self.who, x, alpha, beta, s, depth)
                setScore = min(cScore, beta)
                beta = setScore
                temp = beta
                if beta <= alpha: 
                    break
        return temp  
