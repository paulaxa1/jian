import Arena
from MCTS import MCTS
# from othello.OthelloGame import OthelloGame, display
#from othello.OthelloPlayers import *
from hexgame.keras.NNet import NNetWrapper as NNet
#from connect4.Connect4Game import Connect4Game
#from connect4.Connect4Players import *
from hexgame.HexGame import HexGame, display
from hexgame.HexPlayers import *

import numpy as np
from utils import *


"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

mini_othello = False  # Play in 6x6 instead of the normal 8x8.
human_vs_cpu = True

if mini_othello:
    g = HexGame(4)
else:
    g = HexGame(7)

# all players
rp = RandomPlayer(g).play
#gp = GreedyOthelloPlayer(g).play
hp = HumanHexPlayer(g).play



# nnet players
n1 = NNet(g)
if mini_othello:
    n1.load_checkpoint('./pretrained_models/othello/pytorch/','6x100x25_best.pth.tar')
else:
    n1.load_checkpoint('./temp/','checkpoint_21.pth.tar')
args1 = dotdict({'numMCTSSims': 50, 'cpuct':1.0})
mcts1 = MCTS(g, n1, args1)
n1p = lambda x,y: np.argmax(mcts1.getActionProb(x, temp=0, player1=True if y==1 else False))
#if human_vs_cpu:
#    player2 = hp
#else:
#    n2 = NNet(g)
#    n2.load_checkpoint('./pretrained_models/othello/pytorch/', '8x8_100checkpoints_best.pth.tar')
#    args2 = dotdict({'numMCTSSims': 50, 'cpuct': 1.0})
#    mcts2 = MCTS(g, n2, args2)
#    n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))

#    player2 = n2p  # Player 2 is neural network if it's cpu vs cpu.

arena = Arena.Arena(hp, n1p, g, display=display)

print(arena.playGames(2, verbose=True))
