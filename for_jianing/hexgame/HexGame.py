import sys
import numpy as np
from time import sleep

sys.path.append('..')
from Game import Game
from .HexLogic import Board


class HexGame(Game):
    """
    Connect4 Game class implementing the alpha-zero-general Game interface.
    """

    def __init__(self, n=7):
        self.n = n

    def getInitBoard(self):
        # return initial board (numpy board)
        b = Board(n=self.n)
        return np.array(b.pieces)


    def getBoardSize(self):
        # (a,b) tuple
        return (self.n, self.n)

    def getActionSize(self):
        return self.n * self.n + 1

    def getNextState(self, board, player, action):
        # if player takes action on board, return next (board,player)
        # action must be a valid move
 #       print("Inside getNext State")
 #       ("Valids: ")
        valid_moves = self.getValidMoves(board)
 #       print(valid_moves)
 #       print("For board: ")
 #       print(board)
        if valid_moves[action] == 0:
            assert valid_moves[action] > 0
        b = Board(self.n)
        b.pieces = np.copy(board)
        move = (int(action / self.n), action % self.n)
        b.execute_move(move, 1) #always do 1 on the canonical board
        return (b.pieces, -player)


    def getValidMoves(self, board):
        # return a fixed size binary vector
        valids = [0]*self.getActionSize()
        b = Board(n=self.n)
        b.pieces = np.copy(board)
        legalMoves =  b.get_legal_moves()
        if len(legalMoves)==0:
            valids[-1]=1
            return np.array(valids)
        for x, y in legalMoves:
            valids[self.n*x+y]=1
        return np.array(valids)


    def getGameEnded(self, board, player):
        # return 0 if not ended, 1 if player 1 won, -1 if player 1 lost
        # player = 1
        b = Board(n=self.n)
        b.pieces = np.copy(board)

        if b.check_win(player):
            print('---RED WON---')
            # sleep(5)
            return 1
        if b.check_win(-player):
            print('---BLUE WON---')
            # sleep(5)
            return -1
        return 0

    def getCanonicalForm(self, board, player):
        # Flip player from 1 to -1
        #return board * player
        if player==1:
            return board
        else:
            return np.fliplr(np.rot90(-1*board, k=1, axes=(1, 0)))
    
    def getOriginalForm(self, board):
        return np.rot90(np.fliplr(-1*board), k=1, axes=(0, 1))



    def getSymmetries(self, board, pi):
        # rotation 180 degree
        assert (len(pi) == self.n ** 2 + 1)  # 1 for pass
        pi_board = np.reshape(pi[:-1], (self.n, self.n))
        l = []

        for i in [0, 2]:
            newB = np.rot90(board, i)
            newPi = np.rot90(pi_board, i)
            l += [(newB, list(newPi.ravel()) + [pi[-1]])]
        return l



    def stringRepresentation(self, board):
        return board.tostring()


def display(board):
    n = board.shape[0]

    for y in range(n):
        print (y,"|",end="") #end lines
    print("")
    print(" -----------------------")
    for y in range(n):
        print(y, "|",end="")    # print the row #
        for z in range(y):
            print(" ", end="")
        for x in range(n):
            piece = board[y][x]    # get the piece to print
            if piece == -1: print("b ",end="")
            elif piece == 1: print("r ",end="")
            else:
                if x==n:
                    print("-",end="")
                else:
                    print("- ",end="")
        print("|")

    print("   -----------------------")
                                                 
