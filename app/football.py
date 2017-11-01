from flask import Flask, render_template, url_for, redirect, request, flash
from crudClass import Team
import sqlite3, os, smtplib, itertools, random, datetime

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
        flash("You Just Added " + request.form.get("teamName", None) + " in league")
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

            cursor1 = conn.execute("SELECT PLAYER_NAME  FROM PLAYER ").fetchall()
            z = [dict(zip(["playerName"], line)) for line in cursor1]
            for line in cursor:
                list1.append(dict(zip(b, line)))
            conn.close()
            return render_template("index.html", teamNamess=list1, player_list=z)
        elif request.method == "POST":
            conn = sqlite3.connect("football.db")
            cursor1 = conn.execute("SELECT TEAM_NAME, PLAYER_ID FROM PLAYER WHERE PLAYER_NAME =? ",
                                   (request.form.get("searchBox", None),)).fetchone()

            conn.close()
            print("cursor1 is none")
            if not (cursor1 is None):
                return redirect(url_for("viewPlayer", teamName=cursor1[0], playerId=cursor1[1]))
            else:
                return render_template("error.html")

    except Exception as e:
        print(e)
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
        return render_template("allTeam.html", teamInformation=list1, len=len(list1))
    except Exception as e:
        return render_template("allTeam.html")


@app.route("/team_view/<string:teamName>")
def viewTeam(teamName):
    conn = sqlite3.connect("football.db")
    conn.execute('PRAGMA FOREIGN_KEYS = ON ')
    cursor = conn.execute("SELECT  * FROM TEAM WHERE TEAM_NAME =?", (teamName,)).fetchone()
    cursor1 = conn.execute("SELECT PLAYER_NAME , JERSEY_NUMBER FROM PLAYER WHERE PLAYER.TEAM_NAME=? ", (teamName,))
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
    z = [dict(zip(["playerName", "jerseyNum"], line)) for line in cursor1]
    conn.close()
    return render_template("teaminfo.html", teamdata=teamInfo, playerData=z)


@app.route("/team_delete/<string:teamName>", methods=["POST"])
def deleteTeam(teamName):
    if request.method == "POST":
        conn = sqlite3.connect("football.db")
        conn.execute('PRAGMA FOREIGN_KEYS = ON ')
        conn.execute("DELETE FROM TEAM WHERE TEAM_NAME=?", (teamName,))
        conn.commit()
        conn.close()
        flash("You Just Deleted a Team " + teamName)
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
        return render_template("teamplayers.html", teamPlayersData=list1, teamNamee=list1[0]["teamName"],
                               len=len(list1))

    except:
        return render_template("teamplayers.html", teamNamee=teamName, len=0)
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
        flash("You Just Added " + request.form.get("playerName", None) + " in " + teamName)
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
        flash("You Just Updated " + request.form.get("playerName", None) + " Information", "message")
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
        flash("you just deleted a player from " + teamName, "message")
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
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("aniketcr777@gmail.com", "aniketcr777")

    msg = "Thanks for your valuable feedback. \n" \
          "Warm regards \n" \
          "Football Database Management Team"
    server.sendmail("aniketcr777@gmail.com", receviermail, msg)
    server.quit()


@app.route("/matchFixture", methods=["GET", "POST"])
def matchFixture():
    deleteMatchRelated()
    conn = sqlite3.connect("football.db")
    count = conn.execute("SELECT count(*) FROM TEAM").fetchone()[0]
    print(count)
    if count % 2 == 0:
        # fetch all teamname
        team = conn.execute("SELECT TEAM_NAME FROM TEAM").fetchall()
        print(team)
        # create a list of teamname
        team1 = [y for x in team for y in x]
        print(team1)
        # permutation of team in teamN
        list1 = list(itertools.permutations(team1, r=2))

        # date format
        c = datetime.date(2017, 11, 23)

        date1 = c.isoformat()
        # itearation of permutation

        conn.close()
        for x in list1:
            y = list(x)
            y.append(date1)
            print(y)
            conn1 = sqlite3.connect("football.db")
            conn1.execute("INSERT INTO MATCH_FIXTURE(TEAM1,TEAM2,MATCH_DATE) VALUES (?,?,?)",
                          tuple(y))
            conn1.commit()

            conn1.close()

        conn2 = sqlite3.connect("football.db")
        countTuple = conn2.execute("SELECT MATCH_ID FROM MATCH_FIXTURE").fetchall()
        count2 = [y for x in countTuple for y in x]
        conn2.close()
        location = {"Birminghan": "Old Trafford", "North London": "Stamford Bridge", "Everton": "Ainfield"}
        for x in count2:
            randomLocation = random.choice(list(location.keys()))
            conn3 = sqlite3.connect("football.db")
            conn3.execute("INSERT INTO MATCH_VENUE(MATCH_ID, LOCATION, STADIUM) VALUES (?,?,?)",
                          (x, randomLocation, location[randomLocation],))
            conn3.commit()
            conn3.close()

        conn4 = sqlite3.connect("football.db")
        cursor = conn4.execute(
            "SELECT MATCH_DATE , TEAM1 , TEAM2 , LOCATION , STADIUM   FROM MATCH_FIXTURE ,MATCH_VENUE WHERE MATCH_VENUE.MATCH_ID=MATCH_FIXTURE.MATCH_ID").fetchall()
        b = ["date", "team1", "team2", "location", "stadium"]
        list1 = []
        for x in cursor:
            list1.append(dict(zip(b, x)))
        conn4.close()
        return render_template("matchFixture.html", fixture=list1, date=list1[0]['date'])
    else:
        conn.close()
        return "<h1>You need to have even number of Teams</h1>"


def deleteMatchRelated():
    conn11 = sqlite3.connect("football.db")
    conn11.execute("DELETE FROM MATCH_VENUE")
    conn11.execute("DELETE FROM MATCH_FIXTURE ")
    conn11.commit()
    conn11.close()


@app.route("/topTeam")
def topTeam():
    conn111 = sqlite3.connect("football.db")
    count = conn111.execute("SELECT count(*) FROM TEAM").fetchone()[0]
    print(count)
    conn111.close()
    if count % 2 == 0:
        conn = sqlite3.connect("football.db")
        cursor = conn.execute(
            "SELECT PLAYER_NAME ,NUMBER_OF_GOALS  FROM PLAYER ORDER BY NUMBER_OF_GOALS DESC ").fetchall()
        b = ["playerName", "goals"]
        topPlayers = [dict(zip(b, line)) for line in cursor]
        conn.close()

        conn1 = sqlite3.connect("football.db")
        conn1.execute("DELETE FROM MATCH_RESULT")
        conn1.commit()
        conn1.close()

        conn2 = sqlite3.connect("football.db")
        team = conn2.execute("SELECT TEAM_NAME FROM TEAM").fetchall()
        print(team)
        # create a list of teamname
        team1 = [y for x in team for y in x]
        print(team1)
        # permutation of team in teamN
        list1 = list(itertools.permutations(team1, r=2))

        conn2 = sqlite3.connect("football.db")
        countTuple = conn2.execute("SELECT MATCH_ID FROM MATCH_FIXTURE").fetchall()
        count2 = [y for x in countTuple for y in x]
        conn2.close()

        for i, x in enumerate(list1):
            list111 = list(x)
            random.shuffle(list111)
            list12 = count2[i]
            print(type(list12))
            counnection = sqlite3.connect("football.db")
            counnection.execute("INSERT INTO MATCH_RESULT(MATCH_ID, WIN, LOSE) VALUES (?,?,?)",
                                (list12, list111[0], list111[1]))
            counnection.commit()
            counnection.close()
        conn122 = sqlite3.connect("football.db")
        cursor = conn122.execute("SELECT WIN,count(WIN) FROM MATCH_RESULT GROUP BY WIN ORDER BY count(WIN)DESC")
        b = ["win", "count"]
        topTeam = [dict(zip(b, line)) for line in cursor]
        return render_template("topTeam.html", players=topPlayers, team=topTeam)
    else:
        return "<h1>You need to have even number of Teams</h1>"


@app.route("/matchResult")
def matchResult():
    conn = sqlite3.connect("football.db")
    cursor = conn.execute("SELECT WIN , LOSE FROM MATCH_RESULT")
    b = ["win", "lose"]
    list1 = [dict(zip(b, line)) for line in cursor]
    conn.close()
    return render_template("matchResult.html", result=list1)


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)
