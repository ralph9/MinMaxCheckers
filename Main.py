# -*- coding: utf-8 -*-
"""
Created on Fri May 15 21:03:20 2020

@author: Raúl
"""

from MinMax import MinMaxAlgorithm
from Piece import Piece
from Board import CheckersBoard
from TreeNode import TreeNode
import copy 



class CheckersGame:
    
    initialBoardForTest = []


    evenRowBlack = [[False,'.'],[True,Piece("black")],[False,'.'],[True,Piece("black")],[False,'.'],[True,Piece("black")],[False,'.'],[True,Piece("black")]]
    oddRowBlack = [[True,Piece("black")],[False,'.'],[True,Piece("black")],[False,'.'],[True,Piece("black")],[False,'.'],[True,Piece("black")],[False,'.']]
    
    oddRowWhite = [[True,Piece("white")],[False,'.'],[True,Piece("white")],[False,'.'],[True,Piece("white")],[False,'.'],[True,Piece("white")],[False,'.']]
    evenRowWhite = [[False,'.'],[True,Piece("white")],[False,'.'],[True,Piece("white")],[False,'.'],[True,Piece("white")],[False,'.'],[True,Piece("white")]]
    emptyRowOne = [[True,None],[False,'.'],[True,None],[False,'.'],[True,None],[False,'.'],[True,None],[False,'.']]
    emptyRowTwo = emptyRowOne.copy()
    elementToAppend = emptyRowTwo.pop(0)
    emptyRowTwo.append(elementToAppend)
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
        ai = MinMaxAlgorithm()
        boardForTest = CheckersBoard(self.initialBoardForTest)
        print("game starts")
        currentNode = TreeNode(boardForTest.board)
        currentNode.printTreeNode()
        currentNode.currentTurnWhite = True
        while True: 
            #turn of the player
            if currentNode.currentTurnWhite:
                  if len(currentNode.boardObject.getPossibleCaptures("white")) != 0:
                      print("you have to make a capture, choose the piece")
                      originX = int(input('Insert the piece origin row: '))
                      originY = int(input('Insert the piece origin column: '))
                      destX = int(input('Insert the piece destination row: '))
                      destY = int(input('Insert the piece destination column: '))   
                      currentNode = currentNode.boardObject.generateTreeNodeWithCapture(originX,originY,destX,destY,None)
                      print("after your capture")
                      currentNode.printTreeNode()
                      moreCaptures = str(input("if you wanna make more captures with that piece type Y, otherwise type N"))
                      while moreCaptures == "Y":
                          originX = int(input('Insert the piece origin row: '))
                          originY = int(input('Insert the piece origin column: '))
                          destX = int(input('Insert the piece destination row: '))
                          destY = int(input('Insert the piece destination column: '))  
                          currentNode = currentNode.boardObject.generateTreeNodeWithCapture(originX,originY,destX,destY,None)
                          print("after your capture")
                          currentNode.printTreeNode()
                          moreCaptures = str(input("if you wanna make more captures with that piece type Y, otherwise type N"))
                  else:   
                      originX = int(input('Insert the X origin row: '))
                      originY = int(input('Insert the Y origin column: '))
                      destX = int(input('Insert the X destination row: '))
                      destY = int(input('Insert the Y destination column: '))      
                      currentNode = currentNode.boardObject.generateTreeNodeWithMove(originX,originY,destX,destY)      
                      currentNode.printTreeNode()
                      currentNode.currentTurnWhite = False
                  if currentNode.isGameOver("black"):
                      print("game ended, white won")
                      break
            #turn of the AI    
            else:
                  nodeToPass = copy.deepcopy(currentNode)
                  print("computer is thinking")
                  evaluation, currentNode = ai.minmax(nodeToPass, 4, False)
                  print("it made a move")
                  currentNode.printTreeNode()
                  currentNode.currentTurnWhite = True
                  if currentNode.isGameOver("white"):
                      print("game ended, black won")

check = CheckersGame()
check.play()



