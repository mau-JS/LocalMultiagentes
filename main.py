# TC2008B. Sistemas Multiagentes y Gráficas Computacionales
# Python flask server to interact with Unity. Based on the code provided by Sergio Ruiz.
# Octavio Navarro. November 2022

from flask import Flask, request, jsonify
from boids.boid import Boid
import numpy as np
import os
import mesa
import random
import matplotlib
import pandas as pd
from agent import *
from model import *

numeroAgente = 0
def updatePositions(flock):
    global numeroAgente
    numeroAgente += 1
    positions = []
    for boid in flock:
        boid.apply_behaviour(flock)
        boid.update()
        boid.edges()
        positions.append((boid.id, boid.position))
    return positions

def positionsToJSON(positions):
    posDICT = []
    for id, p in positions:
        pos = {
            "boidId" : str(id),
            "x" : float(p.x),
            "y" : float(p.z),
            "z" : float(p.y)
        }
        posDICT.append(pos)
    return jsonify({'positions':posDICT})

# Size of the board:
width = 30
height = 30

# Set the number of agents here:
flock = []

app = Flask("Boids example")

@app.route('/', methods=['POST', 'GET'])
def boidsPosition():
    if request.method == 'GET':
        positions = updatePositions(flock)
        return positionsToJSON(positions)
    elif request.method == 'POST':
        return "Post request from Boids example\n"

@app.route('/init', methods=['POST', 'GET'])
def boidsInit():
    global flock
    if request.method == 'GET':
        # Set the number of agents here:
        a = CarModel(5,30,30)
        flock = [Boid(*vec[id], width, height, id) for id in range(5)]

        return jsonify({"num_agents":5, "w": 30, "h": 30})
    elif request.method == 'POST':
        return "Post request from init\n"

if __name__=='__main__':
    app.run(host="localhost", port=8585, debug=True)