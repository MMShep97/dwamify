from whereami import predict
from whereami import predict_proba
from whereami.predict import predictfuk
import statistics
import ast
import operator
import time

from flask import Flask, jsonify
from flask_cors import CORS
from multiprocessing import Process, Manager, Value
from ctypes import c_char_p
import logging

#### VARIABLES #################################
posters = ["sy", "daniel", "ben", "table", "oven", "fridge"]
distances_x = {"sy": 136.5, "daniel": 38.5, "ben": 38.5, "table": 260, "oven": 137, "fridge": 255}
distances_y = {"sy": 36.5, "daniel": 36.5, "ben": 110, "table": 79, "oven": 162, "fridge": 190}
data = [[],[],[],[],[],[],[],[]]
od = False

##################################################

# Two values sent to Marco
postername = "default"
xcoord = 1.23
ycoord = 1.23

manager = Manager()
poster_name = manager.Value(c_char_p, 'gorf')
x_coord = Value('d', 1.23)
y_coord = Value('d', 1.23)

def get_x_coord(pred):
	global xcoord
	b = pred["sy"]*distances_x["sy"] + pred["daniel"]*distances_x["daniel"] + pred["ben"]*distances_x["ben"] + pred["table"]*distances_x["table"] + pred["oven"]*distances_x["oven"] + pred["fridge"]*distances_x["fridge"]
	xcoord = b
	return b

def get_y_coord(pred):
	global ycoord
	b = pred["sy"]*distances_y["sy"] + pred["daniel"]*distances_y["daniel"] + pred["ben"]*distances_y["ben"] + pred["table"]*distances_y["table"] + pred["oven"]*distances_y["oven"] + pred["fridge"]*distances_y["fridge"]
	ycoord = b
	return b

def get_predictions():
	global postername
	global xcoord
	global ycoord
	return postername, xcoord, ycoord

def predict_loop(poster_name, x_coord, y_coord):
    first = True
    chances_left = 4
    global postername
    global xcoord
    global ycoord

    while (True):
        time.sleep(1)
        x = predictfuk()
        x = ast.literal_eval(x)
        print(x)
        postername = max(x.items(), key=operator.itemgetter(1))[0]
        poster_name.value = postername
        print("POSTERNAME: ", postername)

        od = False
        data = []

        if first or chances_left == 0:
            chances_left = 4
            prev_x = x
            first = False
            continue

        data.append(prev_x["sy"] - x["sy"])
        data.append(prev_x["daniel"] - x["daniel"])
        data.append(prev_x["ben"] - x["ben"])
        data.append(prev_x["oven"] - x["oven"])
        data.append(prev_x["table"] - x["table"])
        data.append(prev_x["fridge"] - x["fridge"])

        for i in range(len(data)):
            if data[i] >= 0.4 or data[i] <= -0.4:
                print("outlier detected", posters[i])
                od = True
                break
        if od:
            chances_left = chances_left - 1
            continue

        print("no outlier detected")
        prev_x = x
        print("x coord: ", get_x_coord(x))
        print("y coord: ", get_y_coord(x))
        x_coord.value = get_x_coord(x)
        y_coord.value = get_y_coord(x)


        #if poo == "s":
        #	for i in range(8):
        #		print(posters[i])
        #		print(round(statistics.stdev(data[i]),2), "     ", round(statistics.mean(data[i]),2))

        #print(predict_proba())

####### START OF SERVER #################################

DEBUG = True

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app= Flask(__name__)
app.config.from_object(__name__)

CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/active-poster', methods=['GET'])
def send_active_poster():
	return jsonify( {
		'name': poster_name.value,
		'xCoord': x_coord.value,
		'yCoord': y_coord.value
	})

if __name__ == '__main__':
    p = Process(target=predict_loop, args=(poster_name, x_coord, y_coord))
    p.start()
    app.run(host='0.0.0.0', port= 5000, use_reloader=False)
    p.join()
    print("IN MAIN: ", postername)

######## END OF SERVER #################################
