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




class Players(Resource):

    def next_id(self):
        maxid = 0
        for player in data:
            if player["player_id"] > maxid:
                maxid = player["player_id"]
        return maxid+1


    def post(self):

        #if request coming from cURL request.json
        #if request coming from form submit request.form
        req = request.json if request.json != None else request.form
        
        name = req["name"]
        age = req["age"]
        id = self.next_id()

        new_player = {"name" : name, "age" : age, "player_id" : id}
        print("POST: new_player:" , new_player)
        data.append(new_player)
        #print("new_player: ", new_player)
        #print("data: ", data)
        return redirect("/")

class Player(Resource):
    
    def get(self, player_id):
        print(data)
        print(type(data))
        for player in data:
            if player["player_id"] == player_id:
                return player




api.add_resource(Player, "/players/<int:player_id>")
api.add_resource(Players, "/players")

if __name__ == '__main__':

    app.run(debug=True)


