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

app = Flask(__name__)
app.config['SERVER_NAME']='localhost:5000'
#app.config['DEBUG'] = True
#app.run(host="127.0.0.1",port=5000)
# with app.app_context(), app.test_request_context():
#     url = url_for('templates')


check = CheckersGame()
check.play()
startingBoard = check.currentBoardState
computerIsDone = False


@app.route('/')
def start():
    return redirect(url_for("usermove"))
    #startValue="starting game..."
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
        if check.currentNode.currentTurnWhite:
            check.playerTurn(originX,originY,destX,destY)
            return redirect(url_for("compmove"))
        currentBoard = check.currentBoardState
        #return render_template('indexPlayer.html',startValue=startValue,boardState=currentBoard)
    else:
        print("direct red")
        return render_template('index.html',startValue=startValue,boardState=currentBoard,vars="ye")

@app.route('/compmove/', methods=['POST',"GET"])
def compmove(startValue="The computer is thinking"):
    currentBoard = check.currentBoardState
    #crear thread con computer turn y renderizar template entre tanto
    thComp = threading.Thread(target=computerMoveProcessing)
    thComp.start()
    return render_template('indexPlayer.html',startValue=startValue,boardState=currentBoard,vars="startedThink")
    # check.computerTurn()
    # currentBoard = check.currentBoardState
    # return redirect(url_for("usermove"))

@app.route('/compmove/', methods=["POST"])
def computerMoveProcessing(startValue="Your turn"):
    global computerIsDone
    check.computerTurn()
    currentBoard = check.currentBoardState
    # with app.app_context():
    #     print("with context")
    #     return render_template('indexPlayer.html',startValue=startValue,boardState=currentBoard,vars="aaaaaeeeee")

    #print("computer turn over")
    #urlUser = "localhost:5000/usermove/"
    #print(urlUser)
    computerIsDone = True
    compdone()


@app.route('/compdone/', methods=["POST"])
def compdone():
    global computerIsDone
    print(computerIsDone)
    if computerIsDone:
        with app.app_context():
            print("cambio de var")
            return "DONE"
    return "NOT DONE"


if __name__ == '__main__':
    app.run()
