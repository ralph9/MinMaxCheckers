"""
Created on Fri May 15 21:03:20 2020

@author: Raúl
"""
from Piece import Piece
from Board import CheckersBoard
from TreeNode import TreeNode
from MinMaxAlphaBeta import MinMaxAlphaBetaAlgorithm
#from MinMax import MinMaxAlgorithm

import copy 
import time
import math

MAX = "white"
MIN = "black"

class CheckersGame:
    
    initialBoardForTest = []


    evenRowBlack = [[False,'.'],[True,Piece(MIN)],[False,'.'],[True,Piece(MIN)],[False,'.'],[True,Piece(MIN)],[False,'.'],[True,Piece(MIN)]]
    oddRowBlack = [[True,Piece(MIN)],[False,'.'],[True,Piece(MIN)],[False,'.'],[True,Piece(MIN)],[False,'.'],[True,Piece(MIN)],[False,'.']]
    
    oddRowWhite = [[True,Piece(MAX)],[False,'.'],[True,Piece(MAX)],[False,'.'],[True,Piece(MAX)],[False,'.'],[True,Piece(MAX)],[False,'.']]
    evenRowWhite = [[False,'.'],[True,Piece(MAX)],[False,'.'],[True,Piece(MAX)],[False,'.'],[True,Piece(MAX)],[False,'.'],[True,Piece(MAX)]]
    
    emptyRowOne = [[True,None],[False,'.'],[True,None],[False,'.'],[True,None],[False,'.'],[True,None],[False,'.']]
    emptyRowTwo = emptyRowOne.copy()
    
    elementToAppend = emptyRowTwo.pop(0)
    emptyRowTwo.append(elementToAppend)
    
    #append rows to board
    for i in range(8):
            #even rows
            if(i % 2 == 0):
                #white ones
                if(i<3):
                    initialBoardForTest.append(copy.deepcopy(evenRowBlack))
                #black ones
                elif(i>4):
                    initialBoardForTest.append(copy.deepcopy(evenRowWhite))
                #empty ones
                else:
                    initialBoardForTest.append(copy.deepcopy(emptyRowTwo))
            #odd rows
            else:
                #white ones
                if(i<3):
                    initialBoardForTest.append(copy.deepcopy(oddRowBlack))
                #black ones
                elif(i>4):
                    initialBoardForTest.append(copy.deepcopy(oddRowWhite))
                #empty ones
                elif(i % 2 != 0):
                    initialBoardForTest.append(copy.deepcopy(emptyRowOne))               

    def play(self):
        ai = MinMaxAlphaBetaAlgorithm()
        boardForTest = CheckersBoard(self.initialBoardForTest)
        print("the game starts")
        currentNode = TreeNode(boardForTest.board)
        currentNode.printTreeNode()
        currentNode.currentTurnWhite = True
        while True: 
            if currentNode.currentTurnWhite:
                  nodeToPass = copy.deepcopy(currentNode)
                  print("white is thinking")
                  start_time = time.time()
                  evaluation, currentNode = ai.minmaxAlphaBeta(nodeToPass, 4, -math.inf, math.inf, True)
                  print("--- %s seconds ---" % (time.time() - start_time))
                  print("it made a move")
                  currentNode.printTreeNode()
                  currentNode.currentTurnWhite = False
                  if currentNode.isGameOver("black"):
                      print("game ended")
                      print("white is the winner")
                      break
            else:
                  nodeToPass = copy.deepcopy(currentNode)
                  print("black is thinking")
                  start_time = time.time()
                  evaluation, currentNode = ai.minmaxAlphaBeta(nodeToPass, 4, -math.inf, math.inf, False)
                  print("--- %s seconds ---" % (time.time() - start_time))
                  print("it made a move")
                  currentNode.printTreeNode()
                  currentNode.currentTurnWhite = True
                  if currentNode.isGameOver("white"):
                      print("game ended")
                      print("black is the winner")
                      break
                  
check = CheckersGame()
check.play()


