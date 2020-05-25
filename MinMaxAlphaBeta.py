# -*- coding: utf-8 -*-
"""
Created on Sun May  3 17:18:38 2020

@author: Raúl
"""
import math

MAX = "white"
MIN = "black"

class MinMaxAlphaBetaAlgorithm:

        
    def minmaxAlphaBeta(self,currentNode,depthOfAnalysis,alpha,beta,maxPlayer):
        if currentNode.isGameOver(maxPlayer) or depthOfAnalysis == 0:
            if depthOfAnalysis == 0:
                #######
                #THE MOST PRIMITIVE QUIESCENT SEARCH
                #if there are captures in the current position, it can be considered
                #an unstable one, therefore, we should explore it in more depth
                #to guarantee that the evaluation score is more realistic
                if len(currentNode.boardObject.getPossibleCaptures(maxPlayer)):
                    return self.minmaxAlphaBeta(currentNode, 3, alpha, beta, maxPlayer)
            if currentNode.isGameOver(maxPlayer):
                if maxPlayer:
                    return -math.inf, currentNode
                else:
                    return math.inf, currentNode
            if maxPlayer:
                return currentNode.evaluationOfNode(), currentNode
            else:
                return currentNode.evaluationOfNodeAggressive(), currentNode
        #if it is white's turn
        if maxPlayer:
            children = currentNode.getAllPossibleMoves(MAX)
            #starting evaluation value to get the maximum possible evaluation
            maxScore = -math.inf
            bestNode = None
            #return max of callin minmax on all the children
            for child in children:
                evaluationForChild, childItself = self.minmaxAlphaBeta(child,depthOfAnalysis-1,alpha,beta,False)
                maxScore = max(maxScore,evaluationForChild)
                alpha = max(alpha, evaluationForChild)
                if maxScore == evaluationForChild:
                    bestNode = child
                if beta <= alpha:
                    break
            return (maxScore, bestNode)
        #if it is black's turn
        else:
            children = currentNode.getAllPossibleMoves(MIN)
            #starting evaluation value to get the maximum possible evaluation
            minScore = math.inf
            bestNode = None
            for child in children:
                evaluationForChild, childItself = self.minmaxAlphaBeta(child,depthOfAnalysis-1,alpha,beta,True)
                minScore = min(minScore,evaluationForChild)
                beta = min(beta,evaluationForChild)
                if minScore == evaluationForChild:
                    bestNode = child
                if beta <= alpha:
                    break
            return (minScore,bestNode)
