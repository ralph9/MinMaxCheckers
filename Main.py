# -*- coding: utf-8 -*-
"""
Created on Fri May 15 21:03:20 2020

@author: Raúl
"""
from flask import Flask
from flask import render_template, request, redirect, url_for
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
    return redirect(url_for("usermove"))
    #return render_template('index.html',startValue=startValue,boardState=startingBoard)

@app.route('/usermove/',methods=["POST","GET"])
def usermove(startValue="Your turn"):
    currentBoard = check.currentBoardState
    if not request.form.get('originX','') == '':
        originX = int(request.form.get('originX', ''))
        originY = int(request.form.get('originY', ''))
        destX = int(request.form.get('destX', ''))
        destY = int(request.form.get('destY', ''))
        moveCoordinates = str(originX) + str(originY) + str(destX) + str(destY)
        print("coordinates:")
        print(moveCoordinates)
        print("checked")
        if check.currentNode.currentTurnWhite:
            check.playerTurn(originX,originY,destX,destY)
            return redirect(url_for("compmove"))
        currentBoard = check.currentBoardState
        return render_template('indexPlayer.html',startValue=startValue,boardState=currentBoard)
    else:
        return render_template('index.html',startValue=startValue,boardState=currentBoard)

@app.route('/compmove/', methods=['POST',"GET"])
def compmove(startValue="The computer is thinking"):
    check.computerTurn()
    currentBoard = check.currentBoardState
    return redirect(url_for("usermove"))



if __name__ == '__main__':
    app.run()
