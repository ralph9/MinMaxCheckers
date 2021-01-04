# -*- coding: utf-8 -*-
"""
Created on Fri May 15 21:03:20 2020

@author: Raúl
"""
from flask import Flask
from flask import render_template
from flask import request
from flask import redirect, url_for
from flask import jsonify
from flask import copy_current_request_context
from MinMax import MinMaxAlgorithm
from Piece import Piece
from Board import CheckersBoard
from TreeNode import TreeNode
import copy
from CheckersGame import CheckersGame
import threading
import os


app = Flask(__name__)
#app.config['SERVER_NAME']='https://0.0.0.0:5000'
#port = int(os.environ.get("PORT", 5000))
#app.run(host='0.0.0.0', port=port, debug=True)
#app.config['DEBUG'] = True
#app.run(host="0.0.0.0",port=5000)
#port = int(os.environ.get('PORT', 33507))
#waitress.serve(app, port=port)

check = CheckersGame()
check.play()
startingBoard = check.currentBoardState
computerIsDone = False
MAX_BOARD_DIMENSION = 7;
currentBoard = None

@app.route('/')
def start():
    return redirect(url_for("usermove"))


@app.route('/usermove/',methods=["POST","GET"])
def usermove(startValue="Your turn"):
    global computerIsDone, currentBoard
    computerIsDone = False
    currentBoard = check.currentBoardState
    if not request.form.get('originX','') == '':
        originX = int(request.form.get('originX', ''))
        originY = int(request.form.get('originY', ''))
        destX = int(request.form.get('destX', ''))
        destY = int(request.form.get('destY', ''))
        coordinatesAreValid = check_coordinates(originX, originY,destX,destY)
        if not coordinatesAreValid:
            startValue = "Move not possible, try again"
            return render_template('index.html',startValue=startValue,boardState=currentBoard,vars="")
        moveCoordinates = str(originX) + str(originY) + str(destX) + str(destY)
        #calculate if move is possible and redirect to usermove again if not valid with a new startvalue
        print("coordinates:")
        print(moveCoordinates)
        if check.currentNode.currentTurnWhite:
            check.playerTurn(originX,originY,destX,destY,check.currentNode)
            return redirect(url_for("compmove"))
        currentBoard = check.currentBoardState
    else:
        print("direct red")
        return render_template('index.html',startValue=startValue,boardState=currentBoard,vars="")

def check_coordinates(oX,oY,dX,dY):
    if oX > MAX_BOARD_DIMENSION or oY > MAX_BOARD_DIMENSION or dX > MAX_BOARD_DIMENSION or dY > MAX_BOARD_DIMENSION:
        return False
    if oX < 0 or oY < 0 or dX < 0 or dY < 0:
        return False
    return True


@app.route('/compmove/', methods=['POST',"GET"])
def compmove(startValue="The computer is thinking"):
    global currentBoard
    currentBoard = check.currentBoardState
    if computerIsDone == False:
        return
    if check.currentNode.currentTurnWhite:
        return render_template('index.html',startValue="Your turn",boardState=currentBoard,vars="")
    #crear thread con computer turn y renderizar template entre tanto
    thComp = threading.Thread(target=computer_move_processing)
    thComp.start()
    return render_template('computerThinking.html',startValue=startValue,boardState=currentBoard,vars="startedThink")


@app.route('/compmove/')
def computer_move_processing(startValue="Your turn"):
    global currentBoard, computerIsDone
    if computerIsDone == False:
        check.computerTurn(check.currentNode)
        currentBoard = check.currentBoardState
        computerIsDone = True


@app.route('/compdone/', methods=["POST"])
def compdone():
    if computerIsDone:
        return "DONE"
    return "NOT DONE"


if __name__ == '__main__':
    app.run()
