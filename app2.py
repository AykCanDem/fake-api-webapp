from os import read
from flask import Flask
from flask_restful import Api, Resource, abort
from flask import request
from flask import render_template
from flask import redirect
import json

app = Flask(__name__)
api = Api(app)


def read_data():

    data = []

    with open("data.json", "r") as d:
        data = json.load(d)["players"]

    return data


data = read_data()

@app.route("/")
def home():
    
    return render_template("/index.html", data=data)




@app.route("/players/<int:player_id>", methods=["GET"])
def get(player_id):

    for player in data:
        if player["player_id"] == player_id:
            return player


@app.route("/players", methods=["POST"])
def post():
    maxpi = 0
    for player in data:
        print(player)
        if player["player_id"] > maxpi:
            maxpi = player["player_id"]

    name = request.form["name"]
    age = request.form["age"]
    id = maxpi+1

    new_player = {"name" : name, "age" : age, "player_id" : id}
    data.append(new_player)
    print("new_player: ", new_player)
    print("data: ", data)
    return redirect("/")





if __name__ == '__main__':

    app.run(debug=True)


