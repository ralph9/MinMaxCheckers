# -*- coding: utf-8 -*-
"""
Created on Fri May  1 21:02:31 2020

@author: Raúl
"""
from Piece import Piece
import copy
from TreeNode import TreeNode

BOARD_SIZE = 8
MAX = "white"
MIN = "black"

class CheckersBoard:
    board = []
    
    #array of positions where the pieces of both sides are placed during 
    #the current state of the board
    whitePiecesPositions = []
    blackPiecesPositions = []
       
    def __init__(self,board):
        self.board = board
             
    def printBoard(self):
        for row in self.board:
            for square in row:
                if(square[0] == False):
                    print(" - ", end="")
                else:
                    if square[1] is not None:
                        if(square[1].isBlack == True):
                            print(" ● ", end="")
                        else:
                            print(" ○ ",end="")
                    else:
                        print(" - ", end="")
            print("")
                        
    def getAllPossibleMoves(self,colorForMoves):
        #first we retrieve the position of the pieces for the current
        #state of the board (we have to empty the old position data before)
        listOfMoves = []
        if colorForMoves == MIN:
            self.blackPiecesPositions = []
        else:
            self.whitePiecesPositions = []
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                #if the square can be occupied (thus, it is a black square)
                if self.board[row][col][0] == True: 
                    #if there is currently a piece in that square
                    if self.board[row][col][1] is not None:
                        if colorForMoves == MIN and self.board[row][col][1].isBlack == True:
                           self.blackPiecesPositions.append([row,col])
                        elif colorForMoves == MAX and self.board[row][col][1].isBlack == False:
                           self.whitePiecesPositions.append([row,col])
                                    
       
        #first we have to consider the possible captures, since they are 
        #forced moves, otherwise we will consider normal moves
        listOfMoves = self.getPossibleCaptures(colorForMoves)
        
        #since captures are forced, even with only one the rest of the moves
        #don't have to be considered
        if len(listOfMoves) == 0:
            allMoves = self.getNormalMoves(colorForMoves)
            if not isinstance(allMoves, TreeNode):
                filteredListOfMoves = filter(None.__ne__, allMoves)
                listOfMoves = list(filteredListOfMoves)     
                allMoves = listOfMoves
            return allMoves
        else:
            listOfFinalCapturePositions = []
            for capture in listOfMoves:
                #for each different capture we find the end positions that
                #arise from it and add them to the list
                capturePositionToAdd = self.getRecursiveCaptures(capture[0],capture[1],capture[2])
                listOfFinalCapturePositions.append(capturePositionToAdd)
            filteredListOfCaptures = filter(None.__ne__, listOfFinalCapturePositions)
            listOfFinalCapturePositions = list(filteredListOfCaptures)    
            if len(listOfFinalCapturePositions) == 0:
                print("something wrong")
                return [] 
            return listOfFinalCapturePositions
                
    def getRecursiveCaptures(self, initialTreeNode, row,col):
        #if we have a capture, we call recursively for each one until we reach
        #the end of the jump move, in that case we return the final treeNode
        listOfMoreCaptures = self.checkForMoreCaptures(initialTreeNode,row,col)
        #print("len") 
        if len(listOfMoreCaptures) == 0:
            #if no more captures are possible then we return the original & fin
            return initialTreeNode
        else:
            #if more capture nodes are available from that position, keep
            #calling the method to find out where it stops
            for capture in listOfMoreCaptures:
                return self.getRecursiveCaptures(capture[0],capture[1],capture[2])
        #return initialTreeNode
        
    def getPossibleCaptures(self,colorForMoves):
       listOfCaptures = []
       #depending on the color the direction of the capture is different,
       #but in the cases of kings, they have capture in both directions,
       #so we can reuse the capture code for the other color's pieces
       if colorForMoves == MIN:
           for positionOfPiece in self.blackPiecesPositions:
                row = positionOfPiece[0]
                col = positionOfPiece[1]
                if self.board[row][col][1].isKing:
                    #found a king on the board, gotta react differently 
                    listOfCaptures.append(self.getBlackCaptures(row,col,False))
                    listOfCaptures.append(self.getWhiteCaptures(row,col,True))
                else:
                    listOfCaptures.append(self.getBlackCaptures(row,col,False))
             
       #calculate captures for the white pieces
       else:
            for positionOfPiece in self.whitePiecesPositions:
                row = positionOfPiece[0]
                col = positionOfPiece[1]
                if self.board[row][col][1].isKing:
                    #found a king on the board, gotta react differently 
                    #normal captures for a black piece
                    listOfCaptures.append(self.getWhiteCaptures(row,col,False))
                    #plus the captures for a black one with the colour reversed
                    listOfCaptures.append(self.getBlackCaptures(row,col,True))
                else:
                    #in the case of not a king, then normal one
                    listOfCaptures.append(self.getWhiteCaptures(row,col,False))
       filteredListOfCaptures = filter(None.__ne__, listOfCaptures)
       filteredListOfCaptures = list(filteredListOfCaptures)
       return filteredListOfCaptures

    def getBlackCaptures(self,row,col,isWhiteKing):
                if col != 0 and col != BOARD_SIZE-2 and col != BOARD_SIZE-1 and row+2 < BOARD_SIZE:
                    #check for the diagonal capture left move validity
                        #if on diagonal to the left we have a white piece, 
                    #we might be able to capture
                     if isinstance(self.board[row+1][col-1][1], Piece):
                          if self.board[row+1][col-1][1].isBlack == isWhiteKing:
                            if col-2 >= 0 and row+2 < BOARD_SIZE:
                                if self.board[row+2][col-2][1] is None:
                                    captureTreeNode = self.generateTreeNodeWithCapture(row,col,row+2,col-2, None)
                                    nodeWithInfo = [captureTreeNode, row+2,col-2]
                                    return nodeWithInfo
                    #check for diagonal capture right move validity
                     if isinstance(self.board[row+1][col+1][1], Piece):
                         #if on diagonal to the left we have a white piece, 
                        #we might be able to capture
                          if self.board[row+1][col+1][1].isBlack == isWhiteKing:
                            #check it is in board dimensions
                            if col+2 >= 0 and row+2 < BOARD_SIZE:
                                if self.board[row+2][col+2][1] is None:
                                    captureTreeNode = self.generateTreeNodeWithCapture(row,col,row+2,col+2, None)
                                    nodeWithInfo = [captureTreeNode, row+2,col+2]
                                    return nodeWithInfo
                #check for the first column captures, only to the right and down
                elif col == 0 and row+2 < BOARD_SIZE:
                    if isinstance(self.board[row+1][col+1][1], Piece):
                     #if on diagonal to the left we have a white piece, 
                        #we might be able to capture
                        if self.board[row+1][col+1][1].isBlack == isWhiteKing:
                            #check it is in board dimensions
                                if not isinstance(self.board[row+2][col+2][1], Piece):
                                    captureTreeNode = self.generateTreeNodeWithCapture(row,col,row+2,col+2, None)
                                    nodeWithInfo = [captureTreeNode, row+2,col+2]
                                    return nodeWithInfo
                #check for one sided captures (to the left)
                elif (col == BOARD_SIZE-1 and row+2 < BOARD_SIZE) or (col == BOARD_SIZE-2 and row+2 < BOARD_SIZE):
                     #check for the diagonal capture left move validity
                     if isinstance(self.board[row+1][col-1][1], Piece):
                         if self.board[row+1][col-1][1].isBlack == isWhiteKing:
                            #check it is on the board dimension
                                if not isinstance(self.board[row+2][col-2][1], Piece):
                                    captureTreeNode = self.generateTreeNodeWithCapture(row,col,row+2,col-2, None)
                                    nodeWithInfo = [captureTreeNode, row+2,col-2]
                                    return nodeWithInfo
                                
                                
    def getWhiteCaptures(self, row,col, isBlackKing):
                #check for middle columns captures, to both sides as long
                #as the row is one where a capture is possible
                if col != 0 and col != BOARD_SIZE-2 and col != BOARD_SIZE-1 and row > 1:
                    #check for the diagonal capture left move validity
                    if isinstance(self.board[row-1][col-1][1], Piece):
                        #if on diagonal to the left we have a white piece, 
                        #we might be able to capture
                        if self.board[row-1][col-1][1].isBlack != isBlackKing:
                            if col-2 >= 0 and row-2 >= 0:
                                if self.board[row-2][col-2][1] is None:
                                    captureTreeNode = self.generateTreeNodeWithCapture(row,col,row-2,col-2, None)
                                    nodeWithInfo = [captureTreeNode, row-2,col-2]
                                    return nodeWithInfo
                    #check for diagonal capture right move validity
                    if isinstance(self.board[row-1][col+1][1], Piece):
                         #if on diagonal to the left we have a white piece, 
                        #we might be able to capture
                        if self.board[row-1][col+1][1].isBlack != isBlackKing:
                            if row-2 >= 0 and col+2 < BOARD_SIZE:
                                 if not isinstance(self.board[row-2][col+2][1], Piece):
                                    captureTreeNode = self.generateTreeNodeWithCapture(row,col,row-2,col+2, None)
                                    nodeWithInfo = [captureTreeNode, row-2,col+2]
                                    return nodeWithInfo
                #check for the first column captures, only to the right and down
                elif col == 0 and row-2 >= 0:
                    if isinstance(self.board[row-1][col+1][1], Piece):
                     #if on diagonal to the left we have a white piece, 
                        #we might be able to capture
                        if self.board[row-1][col+1][1].isBlack != isBlackKing:
                            #check it is within board dimensions
                                if not isinstance(self.board[row-2][col+2][1], Piece):
                                    captureTreeNode = self.generateTreeNodeWithCapture(row,col,row-2,col+2, None)
                                    nodeWithInfo = [captureTreeNode, row-2,col+2]
                                    return nodeWithInfo
                #check for one sided captures (to the left)
                elif (col == BOARD_SIZE-1 and row-2 >= 0) or (col == BOARD_SIZE-2 and row-2 >= 0):
                     #check for the diagonal capture left move validity
                    if isinstance(self.board[row-1][col-1][1], Piece):
                        #if on diagonal to the left we have a white piece, 
                        #we might be able to capture
                        if self.board[row-1][col-1][1].isBlack != isBlackKing:
                            #check it is on board dimensions
                                if not isinstance(self.board[row-2][col-2][1], Piece):
                                    captureTreeNode = self.generateTreeNodeWithCapture(row,col,row-2,col-2, None)
                                    nodeWithInfo = [captureTreeNode, row-2,col-2]
                                    return nodeWithInfo

    
    def getNormalMoves(self,colorForMoves):
        listOfNormalMoves =  []
        #the way of checking depends on the color of the piece
        if colorForMoves == MIN:
            #we iterate over the positions and see if the normal squares for 
            #a move are free, in case of the king we look also backwards
            for positionOfPiece in self.blackPiecesPositions:
                row = positionOfPiece[0]
                col = positionOfPiece[1]
                if col != 0 and col != BOARD_SIZE-1 and row < BOARD_SIZE-1:
                    #check for the diagonal left move validity
                    if self.board[row+1][col-1][1] is None:
                        moveTreeNode = self.generateTreeNodeWithMove(row,col,row+1,col-1)
                        listOfNormalMoves.append(moveTreeNode)
                    #check for diagonal right move validity
                    if self.board[row+1][col+1][1] is None:
                        moveTreeNode = self.generateTreeNodeWithMove(row,col,row+1,col+1)
                        listOfNormalMoves.append(moveTreeNode)
                #side scenarios, to check only left or right diagonal move
                elif col == 0 and row<BOARD_SIZE-1:
                    if not isinstance(self.board[row+1][col+1][1], Piece):
                        moveTreeNode = self.generateTreeNodeWithMove(row,col,row+1,col+1)
                        listOfNormalMoves.append(moveTreeNode)
                elif col == BOARD_SIZE-1 and row<BOARD_SIZE-1:
                    if self.board[row+1][col-1][1] is None:
                        moveTreeNode = self.generateTreeNodeWithMove(row,col,row+1,col-1)
                        listOfNormalMoves.append(moveTreeNode)
                        
            #check for black kings moves, now backwards
            for positionOfPiece in [pos for pos in self.blackPiecesPositions if self.board[pos[0]][pos[1]][1].isKing == True]:
                row = positionOfPiece[0]
                col = positionOfPiece[1]
                if col != 0 and col != BOARD_SIZE-1 and row != 0 and row < BOARD_SIZE:
                    if self.board[row-1][col+1][1] is None:
                        moveTreeNode = self.generateTreeNodeWithMove(row,col,row-1,col+1)
                        listOfNormalMoves.append(moveTreeNode)
                    if self.board[row-1][col-1][1] is None:
                        moveTreeNode = self.generateTreeNodeWithMove(row,col,row-1,col-1)
                        listOfNormalMoves.append(moveTreeNode)
                elif col == 0:
                    if self.board[row-1][col+1][1] is None:
                        moveTreeNode = self.generateTreeNodeWithMove(row,col,row-1,col+1)
                        listOfNormalMoves.append(moveTreeNode)
                elif col == BOARD_SIZE-1:
                     if self.board[row-1][col-1][1] is None:
                        moveTreeNode = self.generateTreeNodeWithMove(row,col,row-1,col-1)
                        listOfNormalMoves.append(moveTreeNode)
        #white's possible moves        
        else:
            #we iterate over the positions and see if the normal squares for 
            #a move are free, in case of the king we look also backwards
            for positionOfPiece in self.whitePiecesPositions:
                row = positionOfPiece[0]
                col = positionOfPiece[1]
                if col != 0 and col != BOARD_SIZE-1 and row > 0:
                    #check for the diagonal left move validity
                    if self.board[row-1][col-1][1] is None:
                        moveTreeNode = self.generateTreeNodeWithMove(row,col,row-1,col-1)
                        listOfNormalMoves.append(moveTreeNode)
                    #check for diagonal right move validity
                    if self.board[row-1][col+1][1] is None:
                        moveTreeNode = self.generateTreeNodeWithMove(row,col,row-1,col+1)
                        listOfNormalMoves.append(moveTreeNode)
                #side scenarios, to check only left or right diagonal move
                elif col == 0:
                    if self.board[row-1][col+1][1] is None:
                        moveTreeNode = self.generateTreeNodeWithMove(row,col,row-1,col+1)
                        listOfNormalMoves.append(moveTreeNode)
                elif col == BOARD_SIZE-1:
                    if self.board[row-1][col-1][1] is None:
                        moveTreeNode = self.generateTreeNodeWithMove(row,col,row-1,col-1)
                        listOfNormalMoves.append(moveTreeNode)
        
            #check for white kings moves, now backwards
            for positionOfPiece in [pos for pos in self.whitePiecesPositions if self.board[pos[0]][pos[1]][1].isKing == True]:
                row = positionOfPiece[0]
                col = positionOfPiece[1]
                if col != 0 and col != BOARD_SIZE-1 and row < BOARD_SIZE-1:
                    if self.board[row+1][col+1][1] is None:
                        moveTreeNode = self.generateTreeNodeWithMove(row,col,row+1,col+1)
                        listOfNormalMoves.append(moveTreeNode)
                    if self.board[row+1][col-1][1] is None:
                        moveTreeNode = self.generateTreeNodeWithMove(row,col,row+1,col-1)
                        listOfNormalMoves.append(moveTreeNode)
                elif col == 0 and row < BOARD_SIZE-1:
                    if self.board[row+1][col+1][1] is None:
                        moveTreeNode = self.generateTreeNodeWithMove(row,col,row+1,col+1)
                        listOfNormalMoves.append(moveTreeNode)
                elif col == BOARD_SIZE-1 and row < BOARD_SIZE-1:
                     if self.board[row+1][col-1][1] is None:
                        moveTreeNode = self.generateTreeNodeWithMove(row,col,row+1,col-1)
                        listOfNormalMoves.append(moveTreeNode)
        return listOfNormalMoves
        
        
    def generateTreeNodeWithMove(self, rowOrigin, colOrigin, rowDest, colDest):
      #copy of the board to have the required version of it
      boardCopy = copy.deepcopy(self.board)
      #copy the piece from the previous position
      pieceToMove = boardCopy[rowOrigin][colOrigin]
      #we have to check the color to convert it to king if necessary
      if rowDest == 0 and pieceToMove[1].isBlack == False:
          pieceToMove[1].isKing = True
      elif rowDest == BOARD_SIZE-1 and pieceToMove[1].isBlack:
          pieceToMove[1].isKing = True
      #empty the original position
      boardCopy[rowOrigin][colOrigin] = [True,None]
      #and put the piece in its new place
      boardCopy[rowDest][colDest] = pieceToMove
      treeNodeGeneratedByMove = TreeNode(boardCopy)
      return treeNodeGeneratedByMove
  
    
    
    def generateTreeNodeWithCapture(self,rowOrigin, colOrigin, rowDest,colDest,extraBoardForCaptures):
        boardCopy = None
        pieceToMove = None
        if extraBoardForCaptures is not None:
            boardCopy = copy.deepcopy(extraBoardForCaptures)
            pieceToMove = copy.deepcopy(boardCopy[rowOrigin][colOrigin])
        else:
            boardCopy = copy.deepcopy(self.board)
            pieceToMove = copy.deepcopy(self.board[rowOrigin][colOrigin])

        if rowDest == 0 and pieceToMove[1].isBlack == False:
          pieceToMove[1].isKing = True
        elif rowDest == BOARD_SIZE-1 and pieceToMove[1].isBlack:
          pieceToMove[1].isKing = True
        #empty the original position
        boardCopy[rowOrigin][colOrigin] = [True,None]
        #and put the piece in its new place
        boardCopy[rowDest][colDest] = pieceToMove
        #finally, remove the piece that has been captured
        if rowOrigin > rowDest:
            if colOrigin > colDest:
                colToDelete = colOrigin-1
                rowToDelete = rowOrigin-1
            else:
                colToDelete = colDest-1
                rowToDelete = rowOrigin-1
        else:
            if colOrigin > colDest:
                colToDelete = colOrigin-1
                rowToDelete = rowDest-1
            else:
                colToDelete = colDest-1
                rowToDelete = rowDest-1
        boardCopy[rowToDelete][colToDelete] = [True,None]
        treeNodeGeneratedByCapture = TreeNode(boardCopy)
        return treeNodeGeneratedByCapture
    
    def checkForMoreCaptures(self, originalCaptureNode, row, col):
        #first we check if it is a king
        boardForChecking = copy.deepcopy(originalCaptureNode.boardObject.board)
        isKing = boardForChecking[row][col][1].isKing
        colorIsBlack = boardForChecking[row][col][1].isBlack
        listOfCaptures = []
        #######################
        #KINGS
        if isKing:
            if col != 0 and col != BOARD_SIZE-2 and col != BOARD_SIZE-1 and row+2 < BOARD_SIZE:
                    if isinstance(boardForChecking[row+1][col-1][1], Piece):
                        if not boardForChecking[row+1][col-1][1].isBlack != colorIsBlack:
                            if col-2 >= 0 and row+2 < BOARD_SIZE:
                                if boardForChecking[row+2][col-2][1] is None:
                                    #create capture node
                                    newNode = self.generateTreeNodeWithCapture(row,col,row+2,col-2, copy.deepcopy(boardForChecking))
                                    #add it to the listOfCaptures
                                    listOfCaptures.append([newNode,row+2,col-2])
                    if isinstance(boardForChecking[row+1][col+1][1], Piece):
                         if not boardForChecking[row+1][col+1][1].isBlack != colorIsBlack:
                             if col+2 >= 0 and row+2 < BOARD_SIZE:
                                 if boardForChecking[row+2][col+2][1] is None:
                                    #create capture node
                                    newNode = self.generateTreeNodeWithCapture(row,col,row+2,col+2, copy.deepcopy(boardForChecking))
                                    #add it to the listOfCaptures
                                    listOfCaptures.append([newNode,row+2,col+2])
            elif col == 0 and row+2 < BOARD_SIZE:
                    if isinstance(boardForChecking[row+1][col+1][1], Piece):
                        if not boardForChecking[row+1][col+1][1].isBlack != colorIsBlack:
                            if not isinstance(boardForChecking[row+2][col+2][1], Piece):
                                    #create capture node
                                    newNode = self.generateTreeNodeWithCapture(row,col,row+2,col+2, copy.deepcopy(boardForChecking))
                                    #add it to the listOfCaptures
                                    listOfCaptures.append([newNode,row+2,col+2])
            elif (col == BOARD_SIZE-1 and row+2 < BOARD_SIZE) or (col == BOARD_SIZE-2 and row+2 < BOARD_SIZE):
                    if isinstance(boardForChecking[row+1][col-1][1], Piece):
                        if not boardForChecking[row+1][col-1][1].isBlack != colorIsBlack:
                            if not isinstance(boardForChecking[row+2][col-2][1], Piece):
                                    #create capture node
                                    newNode = self.generateTreeNodeWithCapture(row,col,row+2,col-2, copy.deepcopy(boardForChecking))
                                    #add it to the listOfCaptures
                                    listOfCaptures.append([newNode,row+2,col-2])
                                    
            if col != 0 and col != BOARD_SIZE-2 and col != BOARD_SIZE-1 and row > 1:
                    if isinstance(boardForChecking[row-1][col-1][1], Piece):
                        if boardForChecking[row-1][col-1][1].isBlack != colorIsBlack:
                             if col-2 >= 0 and row-2 >= 0:
                                 if boardForChecking[row-2][col-2][1] is None:
                                    #create capture node
                                    newNode = self.generateTreeNodeWithCapture(row,col,row-2,col-2, copy.deepcopy(boardForChecking))
                                    #add it to the listOfCaptures
                                    listOfCaptures.append([newNode,row-2,col-2])
                    if isinstance(boardForChecking[row-1][col+1][1], Piece):
                        if boardForChecking[row-1][col+1][1].isBlack != colorIsBlack:
                            if row-2 >= 0 and col+2 < BOARD_SIZE:
                                if not isinstance(boardForChecking[row-2][col+2][1], Piece):
                                    #create capture node
                                    newNode = self.generateTreeNodeWithCapture(row,col,row-2,col+2, copy.deepcopy(boardForChecking))
                                    #add it to the listOfCaptures
                                    listOfCaptures.append([newNode,row-2,col+2])
            elif col == 0 and row-2 >= 0:
                    if isinstance(boardForChecking[row-1][col+1][1], Piece):
                        if boardForChecking[row-1][col+1][1].isBlack != colorIsBlack:
                            if not isinstance(boardForChecking[row-2][col+2][1], Piece):
                                    #create capture node
                                    newNode = self.generateTreeNodeWithCapture(row,col,row-2,col+2, copy.deepcopy(boardForChecking))
                                    #add it to the listOfCaptures
                                    listOfCaptures.append([newNode,row-2,col+2])
            elif (col == BOARD_SIZE-1 and row-2 >= 0) or (col == BOARD_SIZE-2 and row-2 >= 0):
                    if isinstance(boardForChecking[row-1][col-1][1], Piece):
                        if boardForChecking[row-1][col-1][1].isBlack != colorIsBlack:
                                if not isinstance(boardForChecking[row-2][col-2][1], Piece):
                                    #create capture node
                                    newNode = self.generateTreeNodeWithCapture(row,col,row-2,col-2, copy.deepcopy(boardForChecking))
                                    #add it to the listOfCaptures
                                    listOfCaptures.append([newNode,row-2,col-2])
        #############################################
        #NO KINGS
        else:
            if colorIsBlack:
                if col != 0 and col != BOARD_SIZE-2 and col != BOARD_SIZE-1 and row+2 < BOARD_SIZE:
                    if isinstance(boardForChecking[row+1][col-1][1], Piece):
                        if not boardForChecking[row+1][col-1][1].isBlack:
                            if col-2 >= 0 and row+2 < BOARD_SIZE:
                                if boardForChecking[row+2][col-2][1] is None:
                                    #create capture node
                                    newNode = self.generateTreeNodeWithCapture(row,col,row+2,col-2, copy.deepcopy(boardForChecking))
                                    #add it to the listOfCaptures
                                    listOfCaptures.append([newNode,row+2,col-2])
                    if isinstance(boardForChecking[row+1][col+1][1], Piece):
                         if not boardForChecking[row+1][col+1][1].isBlack:
                             if col+2 >= 0 and row+2 < BOARD_SIZE:
                                 if boardForChecking[row+2][col+2][1] is None:
                                    #create capture node
                                    newNode = self.generateTreeNodeWithCapture(row,col,row+2,col+2, copy.deepcopy(boardForChecking))
                                    #add it to the listOfCaptures
                                    listOfCaptures.append([newNode,row+2,col+2])
                elif col == 0 and row+2 < BOARD_SIZE:
                    if isinstance(boardForChecking[row+1][col+1][1], Piece):
                        if not boardForChecking[row+1][col+1][1].isBlack:
                            if not isinstance(boardForChecking[row+2][col+2][1], Piece):
                                    #create capture node
                                    newNode = self.generateTreeNodeWithCapture(row,col,row+2,col+2, copy.deepcopy(boardForChecking))
                                    #add it to the listOfCaptures
                                    listOfCaptures.append([newNode,row+2,col+2])
                                    #print("extra capture")
                elif (col == BOARD_SIZE-1 and row+2 < BOARD_SIZE) or (col == BOARD_SIZE-2 and row+2 < BOARD_SIZE):
                    if isinstance(boardForChecking[row+1][col-1][1], Piece):
                        if not boardForChecking[row+1][col-1][1].isBlack:
                            if not isinstance(boardForChecking[row+2][col-2][1], Piece):
                                    #create capture node
                                    newNode = self.generateTreeNodeWithCapture(row,col,row+2,col-2, copy.deepcopy(boardForChecking))
                                    #add it to the listOfCaptures
                                    listOfCaptures.append([newNode,row+2,col-2])
            #white normal double captures
            else:
                if col != 0 and col != BOARD_SIZE-2 and col != BOARD_SIZE-1 and row > 1:
                    if isinstance(boardForChecking[row-1][col-1][1], Piece):
                        if boardForChecking[row-1][col-1][1].isBlack:
                             if col-2 >= 0 and row-2 >= 0:
                                 if boardForChecking[row-2][col-2][1] is None:
                                    #create capture node
                                    newNode = self.generateTreeNodeWithCapture(row,col,row-2,col-2, copy.deepcopy(boardForChecking))
                                    #add it to the listOfCaptures
                                    listOfCaptures.append([newNode,row-2,col-2])
                    if isinstance(boardForChecking[row-1][col+1][1], Piece):
                        if boardForChecking[row-1][col+1][1].isBlack:
                            if row-2 >= 0 and col+2 < BOARD_SIZE:
                                if not isinstance(boardForChecking[row-2][col+2][1], Piece):
                                    #create capture node
                                    newNode = self.generateTreeNodeWithCapture(row,col,row-2,col+2, copy.deepcopy(boardForChecking))
                                    #add it to the listOfCaptures
                                    listOfCaptures.append([newNode,row-2,col+2])
                elif col == 0 and row-2 >= 0:
                    if isinstance(boardForChecking[row-1][col+1][1], Piece):
                        if boardForChecking[row-1][col+1][1].isBlack:
                            if not isinstance(boardForChecking[row-2][col+2][1], Piece):
                                    #create capture node
                                    newNode = self.generateTreeNodeWithCapture(row,col,row-2,col+2, copy.deepcopy(boardForChecking))
                                    #add it to the listOfCaptures
                                    listOfCaptures.append([newNode,row-2,col+2])
                elif (col == BOARD_SIZE-1 and row-2 >= 0) or (col == BOARD_SIZE-2 and row-2 >= 0):
                    if isinstance(boardForChecking[row-1][col-1][1], Piece):
                        if boardForChecking[row-1][col-1][1].isBlack:
                                if not isinstance(boardForChecking[row-2][col-2][1], Piece):
                                    #create capture node
                                    newNode = self.generateTreeNodeWithCapture(row,col,row-2,col-2, copy.deepcopy(boardForChecking))
                                    #add it to the listOfCaptures
                                    listOfCaptures.append([newNode,row-2,col-2])

        if len(listOfCaptures) > 0:
            return listOfCaptures
        else:
            return []




