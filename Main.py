# -*- coding: utf-8 -*-
"""
Created on Fri May 15 21:03:20 2020

@author: Raúl
"""
from flask import Flask
from flask import render_template
from flask import request
from MinMax import MinMaxAlgorithm
from Piece import Piece
from Board import CheckersBoard
from TreeNode import TreeNode
import copy
from CheckersGame import CheckersGame

app = Flask(__name__)

check = CheckersGame()
check.play()
startingBoard = check.currentBoardState

@app.route('/')
def start(startValue="starting game..."):
    return render_template('index.html',startValue=startValue,boardState=startingBoard)

@app.route('/newmove/', methods=['POST'])
def newmove(startValue="After your turn"):
    originX = int(request.form.get('originX', ''))
    originY = int(request.form.get('originY', ''))
    destX = int(request.form.get('destX', ''))
    destY = int(request.form.get('destY', ''))
    newMove = originX + originY + destX + destY
    check.computerTurn()
    #check.playerTurn(originX,originY,destX,destY)
    currentBoard = check.currentBoardState
    return render_template('index.html',startValue=startValue,boardState=currentBoard)



if __name__ == '__main__':
    app.run()
