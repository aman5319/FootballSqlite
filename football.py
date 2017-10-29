from flask import Flask, render_template, url_for, redirect, request
from crudClass import Team
import sqlite3, os

app = Flask(__name__)


@app.route('/test')
def hello_world():
    return "working Success"


@app.route("/editTeam/<string:teamName>/", methods=["GET", "POST"])
def editTeam(teamName):
    conn = sqlite3.connect("./football/football.db")
    if request.method == "GET":
        cursor = conn.execute("SELECT  * FROM TEAM WHERE TEAM_NAME=?", (teamName,)).fetchone()
        print(os.getcwd())
        b = ["teamName",
             "teamLogo",
             "squadPic",
             "founded",
             "homeGround",
             "teamCost",
             "teamWebsite",
             "teamOwner",
             "teamCoach",
             "teamSponsor",
             "country",
             "about"]
        teamInfo = dict(zip(b, cursor))
        print(teamInfo)
        conn.close()
        return render_template("teamEditForm.html", teamInfo=teamInfo)

    elif request.method == "POST":
        t = Team(teamName)
        about = request.form.get("teamAbout", None)
        if about == "" or about == " ":
            about = "This team is prominent team in league"
        t.insert_team(teamLogo=request.form.get("teamLogo", None),
                      squadpic=request.form.get("squadPic", None),
                      founded=request.form.get("founded", None),
                      homeground=request.form.get("homeGround", None),
                      teamcost=eval(request.form.get("teamCost", 0)),
                      teamWebsite=request.form.get("teamWebsite", None),
                      teamowner=request.form.get("teamOwner", None),
                      teamcoach=request.form.get("teamCoach", None),
                      sponser=request.form.get("teamSponsor", None),
                      country=request.form.get("country", None),
                      about=about,
                      operation="update")
        print(request.form)
        return redirect(url_for("showTeam"))


@app.route("/addTeam/", methods=["POST", "GET"])
def addTeam():
    if request.method == 'POST':

        about = request.form.get("teamAbout", None)
        if about == "" or about == " ":
            about = "This team is prominent team in league"
        t = Team(request.form.get("teamName", None))
        t.insert_team(teamLogo=request.form.get("teamLogo", None),
                      squadpic=request.form.get("squadPic", None),
                      founded=request.form.get("founded", None),
                      homeground=request.form.get("homeGround", None),
                      teamcost=eval(request.form.get("teamCost", 0)),
                      teamWebsite=request.form.get("teamWebsite", None),
                      teamowner=request.form.get("teamOwner", None),
                      teamcoach=request.form.get("teamCoach", None),
                      sponser=request.form.get("teamSponsor", None),
                      country=request.form.get("country", None),
                      about=about,
                      operation="insert")
        return redirect(url_for("showTeam"))
    else:
        return render_template("teamAddForm.html")


@app.route("/", methods=["GET", "POST"])
def teamInfo():
    if request.method == "GET":
        conn = sqlite3.connect("./football/football.db")
        cursor = conn.execute("SELECT  TEAM_NAME FROM TEAM ")
        b = ["teamName"]
        list1 = []
        for line in cursor:
            list1.append(dict(zip(b, line)))
        conn.close()
        return render_template("index.html", teamNamess=list1)
    elif request.method == "POST":
        pass


@app.route("/showTeam/")
def showTeam():
    conn = sqlite3.connect("./football/football.db")
    cursor = conn.execute("SELECT * FROM TEAM ")
    b = ["teamName",
         "teamLogo",
         "squadPic",
         "founded",
         "homeGround",
         "teamCost",
         "teamWebsite",
         "teamOwner",
         "teamCoach",
         "teamSponsor",
         "country",
         "about"]
    list1 = []
    for line in cursor:
        list1.append(dict(zip(b, line)))
    conn.close()
    return render_template("allTeam.html", teamInformation=list1)


@app.route("/team_view/<string:teamName>")
def viewTeam(teamName):
    conn = sqlite3.connect("./football/football.db")
    cursor = conn.execute("SELECT  * FROM TEAM WHERE TEAM_NAME=?", (teamName,)).fetchone()
    b = ["teamName",
         "teamLogo",
         "squadPic",
         "founded",
         "homeGround",
         "teamCost",
         "teamWebsite",
         "teamOwner",
         "teamCoach",
         "teamSponsor",
         "country",
         "about"]
    teamInfo = dict(zip(b, cursor))
    conn.close()
    return render_template("teaminfo.html", teamdata=teamInfo)


@app.route("/team_delete/<string:teamName>", methods=["POST"])
def deleteTeam(teamName):
    if request.method == "POST":
        print(request.url ,"  " , teamName)
        conn = sqlite3.connect("./football/football.db")
        conn.execute("DELETE FROM TEAM WHERE TEAM_NAME=?", (teamName,))
        conn.commit()
        conn.close()
        return redirect(url_for("showTeam"))


@app.route("/teamPlayers/<string:teamName>")
def teamPlayers(teamName):
    a = db.info.find_one({"teamName": teamName}, {"_id": 0, "players": 1, "teamName": 1})
    return render_template("teamplayers.html", teamPlayersData=a)


@app.route("/addplayers/<string:teamName>", methods=["GET", "POST"])
def addPlayers(teamName):
    if request.method == "POST":
        t = Team(teamName)
        about = request.form.get("about", None)
        if about == "" or about == " ":
            about = "This Player is a prominent Player in " + teamName

        t.insertPlayer(playername=request.form.get("playerName", None),
                       country=request.form.get("country", None),
                       age=request.form.get("playerAge", None),
                       dateofbirth=request.form.get("playerDateOfBirth", None),
                       numberofgoals=request.form.get("numberOfGoals", None),
                       photo=request.form.get("playerPhoto", None),
                       playerposition=request.form.get("playerPosition", None),
                       playercost=request.form.get("playerCost", None),
                       jerseynum=request.form.get("playerJerseyNum", 0),
                       about=about, operation="insert",
                       oldPlayerName="dsada")
        return redirect(url_for("teamPlayers", teamName=teamName))
    elif request.method == "GET":
        return render_template("playerAddForm.html")


@app.route("/editplayers/<string:teamName>/<string:playerName>", methods=["GET", "POST"])
def editPlayers(teamName, playerName):
    if request.method == "POST":
        t = Team(teamName)
        about = request.form.get("about", None)
        if about == "" or about == " ":
            about = "This Player is a prominent Player in " + teamName

        t.insertPlayer(playername=request.form.get("playerName", None),
                       country=request.form.get("country", None),
                       age=request.form.get("playerAge", None),
                       dateofbirth=request.form.get("playerDateOfBirth", None),
                       numberofgoals=request.form.get("numberOfGoals", None),
                       photo=request.form.get("playerPhoto", None),
                       playerposition=request.form.get("playerPosition", None),
                       playercost=request.form.get("playerCost", None),
                       jerseynum=request.form.get("playerJerseyNum", 0),
                       about=about,
                       operation="update",
                       oldPlayerName=playerName)
        return redirect(url_for("teamPlayers", teamName=teamName))
    elif request.method == "GET":

        mydict = {"Goalkeeper": "Goalkeeper",
                  "Right full back": "Right full back",
                  "Left full back": " Left full back",
                  "Right half back": "Right half back",
                  "Centre half back": "Centre half back",
                  "Left half back": "Left half back"}
        a = db.info.aggregate([
            {"$unwind": "$players"},
            {"$match": {"teamName": teamName, "players.playerName": playerName}},
            {"$project": {"players": 1, "_id": 0}}
        ], useCursor=False)
        abc = ""
        for ab in a:
            abc = ab["players"]
        return render_template("playerEditForm.html", teamPlayerData=abc, mydict=mydict, target=abc["playerPosition"])


@app.route("/deleteplayers/<string:teamName>/<string:playerName>", methods=["POST"])
def deletePlayers(teamName, playerName):
    if request.method == "POST":
        db.info.update_one({"teamName": teamName}, {"$pull": {"players": {"playerName": playerName}}})
        return redirect(url_for("teamPlayers", teamName=teamName))


@app.route("/viewPlayer/<string:teamName>/<string:playerName>")
def viewPlayer(teamName, playerName):
    a = db.info.aggregate([
        {"$unwind": "$players"},
        {"$match": {"teamName": teamName, "players.playerName": playerName}},
        {"$project": {"players": 1, "_id": 0, "teamLogo": 1}}
    ], useCursor=False)
    abc = ""
    logo = ""
    for ab in a:
        logo = ab["teamLogo"]
        abc = ab["players"]
    return render_template("playerinfo.html", playerData=abc, logo=logo)


@app.route("/feedback/", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        db.feedback.insert_one(dict(
            name=request.form.get("name", None),
            email=request.form.get("email", None),
            presentation=request.form.get("presentation", None),
            idea=request.form.get("idea", None),
            objective=request.form.get("objective", None),
            review=request.form.get("review", None)
        ))
        return redirect(url_for("teamInfo"))
    elif request.method == "GET":
        return render_template("feedback.html")


@app.route("/showfeedBack/")
def showFeedback():
    return render_template("feedbackshow.html", feedback=db.feedback.find({}))


@app.route("/matchFixture", methods=["GET", "POST"])
def matchFixture():
    return render_template("matchFixture.html")


@app.route("/topTeam")
def topTeam():
    return render_template("topTeam.html")


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)
