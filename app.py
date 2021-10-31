from os import read
from flask import Flask
from flask_restful import Api, Resource, abort
from flask import request
from flask import render_template
from flask import redirect
import json

app = Flask(__name__)
api = Api(app)



# data.json holds up to date data
# init_data.json holds the initial table (does not change)

#default admin mode
admin_mode = 0


def read_data():
    with open("data.json", "r") as d:
        data = json.load(d)
    return data


def update_file(data, file):

    with open(file, "w") as file:
        json.dump(data, file, indent=True)


# render index.html with parameters data and admin_mode
@app.route("/")
def home():
    return render_template("/index.html", data=read_data()["players"], admin_mode=admin_mode)


# read the init_data.json file and update data.json file with its content
@app.route("/reset", methods = ["POST"])
def reset():
    if request.method == "POST":
        with open("init_data.json", "r") as d:
            data = json.load(d)
        update_file(data, "data.json")

    return redirect("/")


#switch admin mode
@app.route("/switch_mode", methods = ["POST"])
def switch_mode():
    global admin_mode
    admin_mode = not(admin_mode)

    return redirect("/")


class Players(Resource):

    def next_id(self):
        data = read_data()
        maxid = 0
        for player in data["players"]:
            if player["player_id"] > maxid:
                maxid = player["player_id"]
        return maxid+1

    #return all players in the list
    def get(self):
        players_list = read_data()
        return players_list["players"]

    def post(self):

        #if request coming from cURL request.json
        #if request coming from form submit request.form
        req = request.json if request.json != None else request.form

        name = req["name"]
        team = req["team"]
        id = self.next_id()

        new_player = {"name" : name, "team" : team, "player_id" : id}
        print("POST: new_player:" , new_player)


        data = read_data()
        #update players list
        data["players"].append(new_player)

        update_file(data, "data.json")


  
        return redirect("/")

class Player(Resource):
    
    def get(self, player_id):
        data = read_data()
        for player in data["players"]:
            if player["player_id"] == player_id:
                return player

    def put(self, player_id):
        req = request.json

        request_player = {"player_id":player_id, "name":req["name"], "team":req["team"]}
        data = read_data()
        #update existing player
        for i,player in enumerate(data["players"]):
            if player["player_id"] == request_player["player_id"]:
                data["players"][i] = request_player

                #update json file
                update_file(data, "data.json")
                return redirect("/")
        else:
            #create new player
            #update players list
            data["players"].append(request_player)

            #update json file
            update_file(data, "data.json")

        return redirect("/")


    def delete(self, player_id):
        data = read_data()
        for i,player in enumerate(data["players"]):
            if player["player_id"] == player_id:
                del data["players"][i]

                #update json file
                update_file(data, "data.json")
                return "deleted"
        else:
            return 204

api.add_resource(Player, "/players/<int:player_id>")
api.add_resource(Players, "/players")

if __name__ == '__main__':

    app.run(debug=True)


