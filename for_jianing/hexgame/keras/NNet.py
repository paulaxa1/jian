import argparse
import os
import shutil
import time
import random
import numpy as np
import math
import sys
sys.path.append('../..')
from utils import *
from NeuralNet import NeuralNet

#for CLR
#from CLR.clr_callback import *

import argparse
from .clr import OneCycleLR
from .clr import LRFinder
from .HexNNet import HexNNet as onnet

args = dotdict({
    'lr': 0.001,
    'dropout': 0.3,
    'epochs': 10,
    'batch_size': 64,
    'cuda': False,
    'num_channels': 512,
})

class NNetWrapper(NeuralNet):
    def __init__(self, game):
        self.nnet = onnet(game, args)
        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize()

    def train(self, examples):
        """
        examples: list of examples, each example is of form (board, pi, v)
        """
        input_boards, target_pis, target_vs = list(zip(*examples))
        input_boards = np.asarray(input_boards)
        target_pis = np.asarray(target_pis)
        target_vs = np.asarray(target_vs)
        #for CLR is is recommended by the authors to use around 2-3 * iterations per epoch
        #therefore, len(examples)//64 is iterations per 1 epoch
        step_size = (len(examples)//64)//2
        #stepsize is set to default (2000)
        #clr_triangular = CyclicLR(base_lr=0.01, max_lr=0.1,step_size=step_size, mode='triangular')
        #lr_callback = LRFinder(len(examples), 64, 0.001, 0.1, lr_scale='exp', save_dir='./')
 #       clr_triangular = OneCycleLR(0.1, end_percentage=0.1, scale_percentage=None, maximum_momentum=None, minimum_momentum=None)
        history = self.nnet.model.fit(x = input_boards, y = [target_pis, target_vs], batch_size = args.batch_size, epochs = args.epochs)
        #print(history.history)
        with open('loss.dat', 'a') as file:
            print([history.history['loss'],history.history['pi_loss'],history.history['v_loss']], file=file)
    
    def predict(self, board):
        """
        board: np array with board
        """
        # timing
        start = time.time()

        # preparing input
        board = board[np.newaxis, :, :]

        # run
        pi, v = self.nnet.model.predict(board)

        #print('PREDICTION TIME TAKEN : {0:03f}'.format(time.time()-start))
        return pi[0], v[0]

    def save_checkpoint(self, folder='checkpoint', filename='checkpoint.pth.tar'):
        filepath = os.path.join(folder, filename)
        if not os.path.exists(folder):
            print("Checkpoint Directory does not exist! Making directory {}".format(folder))
            os.mkdir(folder)
        else:
            print("Checkpoint Directory exists! ")
        self.nnet.model.save_weights(filepath)

    def load_checkpoint(self, folder='checkpoint', filename='checkpoint.pth.tar'):
        # https://github.com/pytorch/examples/blob/master/imagenet/main.py#L98
        filepath = os.path.join(folder, filename)
        if not os.path.exists(filepath):
            raise("No model in path {}".format(filepath))
        self.nnet.model.load_weights(filepath)
