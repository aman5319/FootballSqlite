import sqlite3, os


class Team:
    def __init__(self, teamName1):
        self.teamName = teamName1
        self.conn = sqlite3.connect("./football/football.db")

    def insert_team(self, teamLogo, country, squadpic, founded, homeground, teamcost, teamowner, sponser, teamcoach,
                    teamWebsite, about, operation):
        self.teamLogo = teamLogo
        self.country = country
        self.squadpic = squadpic
        self.founded = founded
        self.homeground = homeground
        self.teamcost = teamcost
        self.teamowner = teamowner
        self.sponser = sponser
        self.teamcoach = teamcoach
        self.teamWebsite = teamWebsite
        self.teamAbout = about

        if operation == "insert":
            self.conn.execute('''INSERT INTO TEAM(TEAM_NAME ,
                                                    TEAM_LOGO_URL ,
                                               SQUAD_PIC_URL ,
                                                  FOUNDED_ON    ,
                                                  HOMEGROUND    ,
                                                  TEAM_COST     ,
                                                  TEAM_WEBSITE  ,
                                                  TEAM_OWNER    ,
                                                  TEAM_COACH    ,
                                                  TEAM_SPONSER  ,
                                                  COUNTRY       ,
                                                  ABOUT)
                                                  VALUES (?,?,?,?,?,?,?,?,?,?,?,?)''',
                              (self.teamName,
                               self.teamLogo,
                               self.squadpic,
                               self.founded,
                               self.homeground,
                               self.teamcost,
                               self.teamWebsite,
                               self.teamowner,
                               self.teamcoach,
                               self.sponser,
                               self.country,
                               self.teamAbout))

            self.conn.commit()
            self.conn.close()
        elif operation == "update":
            self.conn.execute("""UPDATE TEAM SET
                                                TEAM_LOGO_URL=? ,
                                               SQUAD_PIC_URL=?,
                                                  FOUNDED_ON=?   ,
                                                  HOMEGROUND=? ,
                                                  TEAM_COST=?,
                                                  TEAM_WEBSITE=?  ,
                                                  TEAM_OWNER=?    ,
                                                  TEAM_COACH=?    ,
                                                  TEAM_SPONSER=?  ,
                                                  COUNTRY=?       ,
                                                  ABOUT=? WHERE TEAM_NAME=?""",
                              (self.teamLogo,
                               self.squadpic,
                               self.founded,
                               self.homeground,
                               self.teamcost,
                               self.teamWebsite,
                               self.teamowner,
                               self.teamcoach,
                               self.sponser,
                               self.country,
                               self.teamAbout, self.teamName))
            self.conn.commit()
            self.conn.close()
