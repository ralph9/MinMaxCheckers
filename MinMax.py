# -*- coding: utf-8 -*-
"""
Created on Sun May  3 17:18:38 2020

@author: Raúl
"""
import math

MAX = "white"
MIN = "black"


class MinMaxAlgorithm:

        
    def minmax(self,currentNode,depthOfAnalysis,maxPlayer):
        if currentNode.isGameOver(maxPlayer) or depthOfAnalysis == 0:
            if depthOfAnalysis == 0:
                #######
                #THE MOST PRIMITIVE QUIESCENT SEARCH
                #if there are captures in the current position, it can be considered
                #an unstable one, therefore, we should explore it in more depth
                #to guarantee that the evaluation score is more realistic
                if len(currentNode.boardObject.getPossibleCaptures(maxPlayer)):
                    return self.minmax(currentNode, 3, maxPlayer)
            if currentNode.isGameOver(maxPlayer):
                if maxPlayer:
                    return math.inf, currentNode
                else:
                    return -math.inf, currentNode
            return currentNode.evaluationOfNode(), currentNode
        #if it is white's turn
        if maxPlayer:
            children = currentNode.getAllPossibleMoves(MAX)
            #starting evaluation value to get the maximum possible evaluation
            maxScore = -math.inf
            bestNode = None
            #return max of callin minmax on all the children
            for child in children:
                evaluationForChild, childItself = self.minmax(child,depthOfAnalysis-1,False)
                maxScore = max(maxScore,evaluationForChild)
                if maxScore == evaluationForChild:
                    bestNode = child
            return (maxScore, bestNode)
        #if it is black's turn
        else:
            children = currentNode.getAllPossibleMoves(MIN)
            #starting evaluation value to get the minimum possible evaluation
            minScore = math.inf
            bestNode = None
            #in this case return min
            for child in children:
                evaluationForChild, childItself = self.minmax(child,depthOfAnalysis-1,True)
                minScore = min(minScore,evaluationForChild)
                if minScore == evaluationForChild:
                    bestNode = child
            return (minScore,bestNode)
