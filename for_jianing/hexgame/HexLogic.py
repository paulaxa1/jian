from collections import namedtuple
import numpy as np
class Board():
    BLUE=1
    RED=-1
    EMPTY=0
    # list of all  directions on the board, as (x,y) offsets
    #
    DEFAULT_HEIGHT = 4
    DEFAULT_WIDTH = 4
    # DEFAULT_WIN_LENGTH = 4

    WinState = namedtuple('WinState', 'is_ended winner')

    def __init__(self, n=7):
        "Set up initial board configuration."

        self.n = n
        # Create the empty board array.
        self.pieces = [None]*self.n
        for i in range(self.n):
            self.pieces[i] = [0]*self.n

    def __getitem__(self, index):
        return self.pieces[index]



    def get_legal_moves(self):
        """Returns all the legal moves for the given color.
        (1 for white, -1 for black)
        @param color not used and came from previous version.        
        """
        moves = set()  # stores the legal moves.

        # Get all the empty squares (color==0)
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y]==0:
                    newmove = (x,y)
                    moves.add(newmove)
        return list(moves)


    def has_legal_moves(self):
        for y in range(self.n):
            for x in range(self.n):
                if self[x][y]==0:
                    return True
        return False

    def execute_move(self, move, color):
        """Perform the given move on the board; 
        color gives the color pf the piece to play (1=white,-1=black)
        """

        x,y = move

        # Add the piece to the empty square.
        # if self[x][y]!=0:
        #     print(self[x][y])
        # print(self[x][y])
        # assert self[x][y] == 0
        self[x][y] = color



    def is_color(self, coordinates, color):
        return self.pieces[coordinates] == color



    def get_neighbors(self, coordinates):
        (cx,cy) = coordinates
        neighbors = []

        if cx-1>=0:   neighbors.append((cx-1,cy))
        if cx+1<self.n: neighbors.append((cx+1,cy))
        if cx-1>=0    and cy+1<=self.n-1: neighbors.append((cx-1,cy+1))
        if cx+1<self.n  and cy-1>=0: neighbors.append((cx+1,cy-1))
        if cy+1<self.n: neighbors.append((cx,cy+1))
        if cy-1>=0:   neighbors.append((cx,cy-1))
        # print('neighbo')
        # for i in neighbors:
        #     print("neighbour of ", coordinates)
        #     print("my piece: ",self.np_pieces[coordinates])
        #     print(self.np_pieces[i]," at coordinate: ",i)
        return neighbors


    def border(self, color, move):
        (nx, ny) = move
        # print(f'BORDER of {color} : ',move)
        return (color == self.BLUE and nx == self.n-1) or (color == self.RED and ny == self.n-1)

    def traverse(self, color, move, visited):
        if not self.is_color(move, color) or (move in visited and visited[move]): return False
        if self.border(color, move): return True
        visited[move] = True
        for n in self.get_neighbors(move):
            if self.traverse(color, n, visited): return True
        return False

    def check_win(self, color):
        # print('inside check_win: player: ',color)
        for i in range(self.n):
            # print('inside for loop for : ', self.n)
            if color == self.BLUE: move = (0,i)
            else: move = (i,0)
            if self.traverse(color, move, {}):
                return True
        return False


    # def __str__(self):
    #     return str(self.np_pieces)

