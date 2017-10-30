from flask import Flask, render_template, url_for, redirect, request, flash
from crudClass import Team
import sqlite3, os, smtplib

app = Flask(__name__)

app.secret_key = "!@#$%^&*()a-=afs;'';312$%^&*k-[;.sda,./][p;/'=-0989#$%^&0976678v$%^&*(fdsd21234266OJ^&UOKN4odsbd#$%^&*(sadg7(*&^%32b342gd']"


@app.route('/test')
def hello_world():
    return "working Success"


@app.route("/editTeam/<string:teamName>/", methods=["GET", "POST"])
def editTeam(teamName):
    conn = sqlite3.connect("football.db")
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
        if about.strip() == "":
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
        flash("You Just Edited a Team  " + teamName, "message")
        return redirect(url_for("showTeam"))


@app.route("/addTeam/", methods=["POST", "GET"])
def addTeam():
    if request.method == 'POST':

        about = request.form.get("teamAbout", None)
        if about.strip() == "":
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
        flash("You Just Added " + request.form.get("teamName", None) + "in league")
        return redirect(url_for("showTeam"))
    else:
        return render_template("teamAddForm.html")


@app.route("/", methods=["GET", "POST"])
def teamInfo():
    try:
        if request.method == "GET":
            conn = sqlite3.connect("football.db")
            cursor = conn.execute("SELECT  TEAM_NAME FROM TEAM ")
            b = ["teamName"]
            list1 = []
            for line in cursor:
                list1.append(dict(zip(b, line)))
            conn.close()
            return render_template("index.html", teamNamess=list1)
        elif request.method == "POST":
            pass
    except:
        return render_template("index.html")


@app.route("/showTeam/")
def showTeam():
    try:
        conn = sqlite3.connect("football.db")
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
    except:
        return render_template("allTeam.html")


@app.route("/team_view/<string:teamName>")
def viewTeam(teamName):
    conn = sqlite3.connect("football.db")
    conn.execute('PRAGMA FOREIGN_KEYS = ON ')
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
        print(request.url, "  ", teamName)
        conn = sqlite3.connect("football.db")
        conn.execute('PRAGMA FOREIGN_KEYS = ON ')
        conn.execute("DELETE FROM TEAM WHERE TEAM_NAME=?", (teamName,))
        conn.commit()
        conn.close()
        flash("You Just Deleted a Team" + teamName)
        return redirect(url_for("showTeam"))


@app.route("/teamPlayers/<string:teamName>")
def teamPlayers(teamName):
    conn = sqlite3.connect("football.db")
    conn.execute('PRAGMA FOREIGN_KEYS = ON ')
    cursor = conn.execute("SELECT  * FROM PLAYER WHERE TEAM_NAME =?", (teamName,))
    try:
        b = ["teamName", "playerId", "playerName", "country", "playerAge", "playerPhoto",
             "playerDate", "numberOfGoals", "playerPosition", "playerCost",
             "playerJerseyNum", "about"]
        list1 = []
        for cursor1 in cursor:
            list1.append(dict(zip(b, cursor1)))
        return render_template("teamplayers.html", teamPlayersData=list1, teamNamee=list1[0]["teamName"])

    except:
        return render_template("teamplayers.html", teamNamee=teamName)
    finally:
        conn.close()


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
                       about=about,
                       operation="insert",
                       oldPlayerid="")
        return redirect(url_for("teamPlayers", teamName=teamName))
    elif request.method == "GET":
        return render_template("playerAddForm.html")


@app.route("/editplayers/<string:teamName>/<int:playerId>", methods=["GET", "POST"])
def editPlayers(teamName, playerId):
    if request.method == "POST":
        t = Team(teamName)
        about = request.form.get("about", None)
        if about.strip() == "":
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
                       oldPlayerid=playerId)
        return redirect(url_for("teamPlayers", teamName=teamName))
    elif request.method == "GET":
        conn = sqlite3.connect("football.db")
        conn.execute('PRAGMA FOREIGN_KEYS = ON ')
        cursor = conn.execute("SELECT * FROM PLAYER WHERE PLAYER_ID =?", (playerId,)).fetchone()
        mydict = {"Goalkeeper": "Goalkeeper",
                  "Right full back": "Right full back",
                  "Left full back": " Left full back",
                  "Right half back": "Right half back",
                  "Centre half back": "Centre half back",
                  "Left half back": "Left half back"}

        b = ["teamName", "playerId", "playerName", "country", "playerAge", "playerPhoto",
             "playerDate", "numberOfGoals", "playerPosition", "playerCost",
             "playerJerseyNum", "about"]
        abc = dict(zip(b, cursor))
        return render_template("playerEditForm.html", teamPlayerData=abc, mydict=mydict, target=abc["playerPosition"])


@app.route("/deleteplayers/<string:teamName>/<int:playerId>", methods=["POST"])
def deletePlayers(teamName, playerId):
    if request.method == "POST":
        conn = sqlite3.connect("football.db")
        conn.execute('PRAGMA FOREIGN_KEYS = ON ')

        conn.execute('''DELETE FROM PLAYER WHERE PLAYER_ID =?''', (playerId,))
        conn.commit()
        conn.close()
        return redirect(url_for("teamPlayers", teamName=teamName))


@app.route("/viewPlayer/<string:teamName>/<int:playerId>")
def viewPlayer(teamName, playerId):
    conn = sqlite3.connect("football.db")
    conn.execute('PRAGMA FOREIGN_KEYS = ON ')

    cursor = conn.execute('''SELECT * FROM PLAYER WHERE PLAYER_ID =?''', (playerId,)).fetchone()
    b = ["teamName", "playerId", "playerName", "country", "playerAge", "playerPhoto",
         "playerDate", "numberOfGoals", "playerPosition", "playerCost",
         "playerJerseyNum", "about"]
    abc = dict(zip(b, cursor))
    cursorLogo = conn.execute('''SELECT TEAM_LOGO_URL FROM TEAM , PLAYER WHERE PLAYER_ID =? AND TEAM.TEAM_NAME =?''',
                              (playerId, teamName)).fetchone()
    conn.close()
    return render_template("playerinfo.html", playerData=abc, logo=cursorLogo[0])


@app.route("/feedback/", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        conn = sqlite3.connect("football.db")
        presentation = request.form.get("presentation", None)
        idea = request.form.get("idea", None)
        objective = request.form.get("objective", None)
        suggestion = request.form.get("review", None) if request.form.get("review",
                                                                          None).strip() != "" else "No Suggestions"

        b = {"Excellent": 100, "Good": 75, "Satisfactory": 50, "Bad": 25}
        presentation_count = b[presentation]
        idea_count = b[idea]
        objective_count = b[idea]

        conn.execute(
            '''INSERT  INTO  FEEDBACK(NAME, EMAIL, PRESENTATION, IDEA, OBJECTIVES, SUGGESTION, PRESENTATION_COUNT, IDEA_COUNT, OBJECTTIVES_COUNT)
                    VALUES (?,?,?,?,?,?,?,?,?)''',
            (request.form.get("name", None),
             request.form.get("email", None),
             presentation, idea, objective, suggestion,
             presentation_count, idea_count, objective_count)
        )
        conn.commit()
        conn.close()
        sendmail(request.form.get("email", None))
        return redirect(url_for("teamInfo"))
    elif request.method == "GET":
        return render_template("feedback.html")


@app.route("/showfeedBack/")
def showFeedback():
    conn = sqlite3.connect("football.db")
    cursor = conn.execute("SELECT NAME,EMAIL,PRESENTATION,IDEA,OBJECTIVES,SUGGESTION FROM FEEDBACK")
    cursor1 = conn.execute(
        "SELECT sum(PRESENTATION_COUNT)/COUNT(*) AS pcount ,sum(IDEA_COUNT)/COUNT(*) AS icount ,sum(OBJECTTIVES_COUNT)/COUNT(*) AS ocount , count(*) AS Tcount FROM FEEDBACK").fetchone()
    list1 = []
    b1 = ["pcount", "icount", "ocount", "Tcount"]
    b = ["name", "email", "presentation", "idea", "objective", "review"]
    for line in cursor:
        list1.append(dict(zip(b, line)))
    conn.close()
    return render_template("feedbackshow.html", feedback=list1, stat=dict(zip(b1, cursor1))) if len(
        list1) != 0 else "No Feedback in database"


@app.errorhandler(404)
def handleerror(e):
    return render_template("error.html")


def sendmail(receviermail):
    pass


@app.route("/matchFixture", methods=["GET", "POST"])
def matchFixture():
    return render_template("matchFixture.html")


@app.route("/topTeam")
def topTeam():
    return render_template("topTeam.html")


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)
