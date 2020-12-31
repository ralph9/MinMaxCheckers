# -*- coding: utf-8 -*-
"""
Created on Sun May  3 18:21:59 2020

@author: Raúl
"""

from Piece import Piece

BOARD_SIZE = 8

MAX = "white"
MIN = "black"

#class to represent a node in the tree, with a board and a turn assigned to it
class TreeNode:
    boardObject = None
    currentTurnWhite = None

    def __init__(self,board):
        from Board import CheckersBoard
        self.boardObject = CheckersBoard(board)

    def evaluationOfNode(self):
        #The evaluation depends on the stage of the game
        #which can be delimited by the number of pieces left
        numberOfWhitePieces = 0
        numberOfBlackPieces = 0
        numberOfWhiteKings = 0
        numberOfBlackKings = 0
        whitePositions = []
        blackPositions = []
        boardRef = self.boardObject.board
        for i in range(len(boardRef)):
            for j in range(len(boardRef)):
                if boardRef[i][j][0] == True and boardRef[i][j][1] is not None:
                    if boardRef[i][j][1].isBlack and boardRef[i][j][1].isKing:
                        numberOfBlackKings += 1
                        blackPositions.append([i,j])
                    elif boardRef[i][j][1].isBlack and boardRef[i][j][1].isKing == False:
                        numberOfBlackPieces += 1
                        blackPositions.append([i,j])
                    elif boardRef[i][j][1].isBlack == False and boardRef[i][j][1].isKing:
                        numberOfWhiteKings += 1
                        whitePositions.append([i,j])
                    elif boardRef[i][j][1].isBlack == False and boardRef[i][j][1].isKing == False:
                        numberOfWhitePieces += 1
                        whitePositions.append([i,j])

        positionSpectrumWhite = 0
        positionSpectrumBlack = 0

        ################################
        #ENDGAME
        #once we reach the endgame the evaluation prefers the kings in the middle of the board
        if numberOfWhitePieces + numberOfWhiteKings < 5 and numberOfBlackPieces + numberOfBlackKings < 5:
            positionSpectrumWhite = int(self.calculatePositionsValueForEndgame(whitePositions,MAX)) * 0.5
            positionSpectrumBlack = int(self.calculatePositionsValueForEndgame(blackPositions,MIN)) *0.5

        numberOfWhitePieces *= 2
        numberOfWhiteKings *= 4
        numberOfBlackPieces *= 2
        numberOfWhiteKings *= 4


        trappedWhitePieces = int(self.calculateNumberOfTrappedPieces(whitePositions,MAX)) * 0.75
        trappedBlackPieces = int(self.calculateNumberOfTrappedPieces(blackPositions,MIN)) * 0.75

        whitePiecesInDanger = int(self.calculateNumberOfPiecesInDanger(MAX)) * 1.75
        blackPiecesInDanger = int(self.calculateNumberOfPiecesInDanger(MIN)) * 1.75

        numberOfWhiteMoves = int(len(self.boardObject.getNormalMoves(MAX))) * 0.5
        numberOfBlackMoves = int(len(self.boardObject.getNormalMoves(MIN))) * 0.5

        whiteScore = numberOfWhitePieces + numberOfWhiteKings + positionSpectrumWhite + numberOfWhiteMoves  - whitePiecesInDanger - trappedWhitePieces
        blackScore = numberOfBlackPieces + numberOfBlackKings + positionSpectrumBlack + numberOfBlackMoves  - blackPiecesInDanger - trappedBlackPieces

        return whiteScore - blackScore


    def evaluationOfNodeAggressive(self):
        #The evaluation depends on the stage of the game
        #which can be delimited by the number of pieces left
        numberOfWhitePieces = 0
        numberOfBlackPieces = 0
        numberOfWhiteKings = 0
        numberOfBlackKings = 0
        whitePositions = []
        blackPositions = []
        boardRef = self.boardObject.board
        for i in range(len(boardRef)):
            for j in range(len(boardRef)):
                if boardRef[i][j][0] == True and boardRef[i][j][1] is not None:
                    if boardRef[i][j][1].isBlack and boardRef[i][j][1].isKing:
                        numberOfBlackKings += 1
                        blackPositions.append([i,j])
                    elif boardRef[i][j][1].isBlack and boardRef[i][j][1].isKing == False:
                        numberOfBlackPieces += 1
                        blackPositions.append([i,j])
                    elif boardRef[i][j][1].isBlack == False and boardRef[i][j][1].isKing:
                        numberOfWhiteKings += 1
                        whitePositions.append([i,j])
                    elif boardRef[i][j][1].isBlack == False and boardRef[i][j][1].isKing == False:
                        numberOfWhitePieces += 1
                        whitePositions.append([i,j])

        positionSpectrumWhite = 0
        positionSpectrumBlack = 0

        numberOfWhitePieces *= 1.75
        numberOfWhiteKings *= 4.25
        numberOfBlackPieces *= 1.75
        numberOfWhiteKings *= 4.25

        ################################
        #ENDGAME
        #once we reach the endgame the evaluation prefers the kings in the middle of the board
        if numberOfWhitePieces + numberOfWhiteKings < 5 and numberOfBlackPieces + numberOfBlackKings < 5:
            positionSpectrumWhite = int(self.calculatePositionsValueForEndgame(whitePositions,MAX)) * 0.5
            positionSpectrumBlack = int(self.calculatePositionsValueForEndgame(blackPositions,MIN)) *0.5
        else:
            positionSpectrumBlack = self.calculatePositionsValue(blackPositions,MIN) * 0.75
            positionSpectrumWhite = self.calculatePositionsValue(whitePositions,MAX) * 0.75

        trappedWhitePieces = int(self.calculateNumberOfTrappedPieces(whitePositions,MAX)) * 1.25
        trappedBlackPieces = int(self.calculateNumberOfTrappedPieces(blackPositions,MIN)) * 1.25

        whitePiecesInDanger = int(self.calculateNumberOfPiecesInDanger(MAX)) * 1.25
        blackPiecesInDanger = int(self.calculateNumberOfPiecesInDanger(MIN)) * 1.25

        numberOfWhiteMoves = int(len(self.boardObject.getNormalMoves(MAX))) * 0.75
        numberOfBlackMoves = int(len(self.boardObject.getNormalMoves(MIN))) * 0.75

        whiteScore = numberOfWhitePieces + numberOfWhiteKings + positionSpectrumWhite + numberOfWhiteMoves  - whitePiecesInDanger  - trappedWhitePieces
        blackScore = numberOfBlackPieces + numberOfBlackKings + positionSpectrumBlack + numberOfBlackMoves  - blackPiecesInDanger  - trappedBlackPieces

        return whiteScore - blackScore





    def calculateNumberOfPiecesInDanger(self,colorOfPieces):
        if colorOfPieces == MAX:
            return len(self.boardObject.getPossibleCaptures(MIN))

        else:
            return len(self.boardObject.getPossibleCaptures(MAX))


    def calculateNumberOfTrappedPieces(self,positionsOfPieces, colorForCalculation):
        trappedPieces = 0
        boardForCalculations = self.boardObject.board
        #white kings
        if colorForCalculation == MAX:
            for position in positionsOfPieces:
                row = position[0]
                col = position[1]
                pieceForIteration = boardForCalculations[row][col]
                isKing = pieceForIteration[1].isKing
                #we only care about the trapped kings so if it isn't we continue
                if not isKing:
                            continue
                else:
                    #if it has at least one move then it is not trapped
                    kingAvailableMoves = self.checkKingMobility(row,col)
                    if kingAvailableMoves:
                        continue
                trappedPieces += 1
        #black kings
        else:
            for position in positionsOfPieces:
                row = position[0]
                col = position[1]
                pieceForIteration = boardForCalculations[row][col]
                if pieceForIteration[0] == False:
                    print(row)
                    print(col)
                    self.printTreeNode()
                isKing = pieceForIteration[1].isKing
                if not isKing:
                            continue
                else:
                    kingAvailableMoves = self.checkKingMobility(row,col)
                    if kingAvailableMoves:
                        continue
                trappedPieces += 1
        #we return the final number of trapped kings of the given color
        return trappedPieces

    #since it is a king we have to look in both directions for a move
    def checkKingMobility(self,row,col):
        boardForCalculations = self.boardObject.board
        if col != 0 and col != BOARD_SIZE-1 and row != 0 and row != BOARD_SIZE-1:
            if boardForCalculations[row-1][col-1][1] is None or boardForCalculations[row-1][col+1][1] is None:
                return True
            if boardForCalculations[row+1][col-1][1] is None or boardForCalculations[row+1][col+1][1] is None:
                return True
        if row == 0:
            if col == 0:
                if boardForCalculations[row+1][col+1][1] is None:
                    return True
            elif col == BOARD_SIZE-1:
                if boardForCalculations[row+1][col-1][1] is None:
                    return True
            else:
                if boardForCalculations[row+1][col-1][1] is None or boardForCalculations[row+1][col+1][1] is None:
                    return True
        if row == BOARD_SIZE-1:
            if col == 0:
                if boardForCalculations[row-1][col+1][1] is None:
                    return True
            elif col == BOARD_SIZE-1:
                if boardForCalculations[row-1][col-1][1] is None:
                    return True
            else:
                if boardForCalculations[row-1][col-1][1] is None or boardForCalculations[row-1][col+1][1] is None:
                    return True

    def calculatePositionsValue(self,positionsOfPieces, colorForCalculation):
        valueOfPositions = 0
        if colorForCalculation == MAX:
            #if we're white we wanna get to row 0 to make a king
            for position in positionsOfPieces:
                if self.boardObject.board[position[0]][position[1]][1].isKing == False:
                    valueOfPositions += len(self.boardObject.board) - position[0]
        else:
            #for black it's the opposite case
            for position in positionsOfPieces:
                if self.boardObject.board[position[0]][position[1]][1].isKing == False:
                    valueOfPositions += position[0]
        return valueOfPositions


    def calculatePositionsValueForEndgame(self, positionsOfPieces, colorForCalculation):
        valueOfPositions = 0
        if colorForCalculation == MAX:
            for position in positionsOfPieces:
                if self.boardObject.board[position[0]][position[1]][1].isKing == False:
                    valueOfPositions += len(self.boardObject.board) - position[0]
                else:
                    #if the kings are well positioned (centered) in the endgame, a plus is added to the score
                    if position[0] == int(BOARD_SIZE/2) or position[0] == int(BOARD_SIZE/2 -1) or position[0] == int(BOARD_SIZE/2 +1):
                        valueOfPositions += 4
        else:
            for position in positionsOfPieces:
                if self.boardObject.board[position[0]][position[1]][1].isKing == False:
                    valueOfPositions += position[0]
                #if the kings are well positioned (centered) in the endgame, a plus is added to the score
                elif position[0] == int(BOARD_SIZE/2) or position[0] == int(BOARD_SIZE/2 -1) or position[0] == int(BOARD_SIZE/2 +1):
                        valueOfPositions += 4
        return valueOfPositions




    #method to find out if the game is over
    #two possibilities, one side hasn't got any more pieces
    #or cannot move any of the pieces
    def isGameOver(self,currentTurnWhite):
        noMoreWhitePieces = None
        noMoreBlackPieces = None
        if currentTurnWhite:
            noMoreWhitePieces = True
            for row in self.boardObject.board:
             for cell in row:
              if isinstance(cell[1],Piece):
                if not cell[1].isBlack:
                    noMoreWhitePieces = False
                    break
        else:
            noMoreBlackPieces = True
            for row in self.boardObject.board:
             for cell in row:
               if isinstance(cell[1],Piece):
                if cell[1].isBlack:
                    noMoreBlackPieces = False
                    break

        if noMoreBlackPieces and not currentTurnWhite:
            return True
        if noMoreWhitePieces and currentTurnWhite:
            return True

        #now onto the second check, gotta see if there's any available move
        if self.currentTurnWhite:
            if self.boardObject.getAllPossibleMoves(MAX) == []:
                return True
        else:
            if self.boardObject.getAllPossibleMoves(MIN) == []:
                return True

    def printTreeNode(self):
        for row in self.boardObject.board:
            for square in row:
                if(square[0] == False):
                    print(" - ", end="")
                else:
                    if square[1] is not None:
                        if square[1].isBlack and square[1].isKing == False:
                            print(" ● ", end="")
                        elif square[1].isBlack and square[1].isKing:
                            print(" ⚉ ", end="")
                        elif square[1].isBlack == False and square[1].isKing == False:
                            print(" ○ ",end="")
                        else:
                            print(" ⚇ ",end="")
                    else:
                        print(" - ", end="")
            print("")

    def getNodeString(self):
        nodeString = ""
        for row in self.boardObject.board:
            for square in row:
                if(square[0] == False):
                    nodeString += " - "
                else:
                    if square[1] is not None:
                        if square[1].isBlack and square[1].isKing == False:
                            nodeString += " ● "
                        elif square[1].isBlack and square[1].isKing:
                            nodeString += " ⚉ "
                        elif square[1].isBlack == False and square[1].isKing == False:
                            nodeString += " ○ "
                        else:
                            nodeString += " ⚇ "
                    else:
                        nodeString += " - "
            nodeString += "\n"
        return nodeString



    #call to the move from the CheckersBoardClass to get the available moves,
    #either captures or normal ones
    def getAllPossibleMoves(self,colorForMoves):
        return self.boardObject.getAllPossibleMoves(colorForMoves)
