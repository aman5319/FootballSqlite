from flask import Flask, render_template, url_for, redirect, request
from crudClass import Team
import sqlite3 , os


app = Flask(__name__)


@app.route('/test')
def hello_world():
    return "working Success"


@app.route("/editTeam/<string:teamName>/", methods=["GET", "POST"])
def editTeam(teamName):
    conn = sqlite3.connect("./football/football.db")
    if request.method == "GET":
        cursor = conn.execute("SELECT  * FROM TEAM WHERE TEAM_NAME=?" , (teamName , )).fetchone()
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
        return render_template("teamEditForm.html",teamInfo=teamInfo)

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
        return redirect(url_for("hello_world"))


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
        return redirect(url_for("hello_world"))
    else:
        return render_template("teamAddForm.html")


if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=5000)
