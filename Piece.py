# -*- coding: utf-8 -*-
"""
Created on Fri May  1 20:58:56 2020

@author: Raúl
"""

MAX = "white"
MIN = "black"

class Piece:
    isKing = False
    isBlack = None
    
    #constructor for the piece class, indicating the color of the piece
    #initially all the pieces are not kings
    def __init__(self,color):    
        if color == MIN:
            self.isBlack = True
        elif color == MAX:
            self.isBlack = False
            