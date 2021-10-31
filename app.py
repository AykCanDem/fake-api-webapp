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
    with open("data.json", "r") as d:
        data = json.load(d)

    return data

data = read_data()

admin_mode = 0





@app.route("/")
def home():
    return render_template("/index.html", data=read_data()["players"], admin_mode=admin_mode)



@app.route("/reset", methods = ["POST"])
def reset():
    if request.method == "POST":
        with open("init_data.json", "r") as d:
            global data 
            data = json.load(d)

        with open("data.json", "w") as file:
            json.dump(data, file)

    return redirect("/")
    #return render_template("/index.html", data=data["players"])


@app.route("/switch_mode", methods = ["POST"])
def switch_mode():
    global admin_mode
    if admin_mode == 1:
        admin_mode = 0
    else:
        admin_mode = 1

    return redirect("/")
    #return render_template("/index.html", data=data["players"])


class Players(Resource):

    def next_id(self):
        maxid = 0
        for player in data["players"]:
            if player["player_id"] > maxid:
                maxid = player["player_id"]
        return maxid+1

    #return all players in the list
    def get(self):
        players_list = read_data()
        return players_list

    def post(self):

        #if request coming from cURL request.json
        #if request coming from form submit request.form
        req = request.json if request.json != None else request.form

        name = req["name"]
        team = req["team"]
        id = self.next_id()

        new_player = {"name" : name, "team" : team, "player_id" : id}
        print("POST: new_player:" , new_player)

        #update players list
        data["players"].append(new_player)

        #update json file
        with open("data.json", "w") as file:
            json.dump(data, file)


  
        return redirect("/")

class Player(Resource):
    
    def get(self, player_id):
        print(data)
        print(type(data))
        for player in data["players"]:
            if player["player_id"] == player_id:
                return player

    def put(self, player_id):
        req = request.json

        request_player = {"player_id":player_id, "name":req["name"], "team":req["team"]}

        #update existing player
        for i,player in enumerate(data["players"]):
            if player["player_id"] == request_player["player_id"]:
                data["players"][i] = request_player

                #update json file
                with open("data.json", "w") as file:
                    json.dump(data, file)
                return 200, "OK"
        else:
            #create new player
            #update players list
            data["players"].append(request_player)

            #update json file
            with open("data.json", "w") as file:
                json.dump(data, file)
                return 200, OK


    def delete(self, player_id):

        for i,player in enumerate(data["players"]):
            if player["player_id"] == player_id:
                del data["players"][i]

                #update json file
                with open("data.json", "w") as file:
                    json.dump(data, file)
                return "deleted"
        else:
            return 204

api.add_resource(Player, "/players/<int:player_id>")
api.add_resource(Players, "/players")

if __name__ == '__main__':

    app.run(debug=True)


