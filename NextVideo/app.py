from NextVideo import NextVideo
from flask import Flask
from flask import render_template
import json
app = Flask(__name__)

# --------------------------------------------------------
# define the webserver API routes

@app.route("/")
def help():
    return render_template('help.html')
   
@app.route("/Series")
def listAllSeries():
    nv = NextVideo("mark")
    return json.dumps(nv.listAllSeries()) 

@app.route("/WatchList")
def listCarryOnWatchList():
    nv = NextVideo("mark")
    return json.dumps(nv.listCarryOnWatchList())

@app.route("/Series/<seriesID>")
def getNextEpisode(seriesID):
    nv = NextVideo("mark")
    return json.dumps(nv.getNextEpisode(seriesID))

@app.route("/Series/<seriesID>/Inc", methods=['GET', 'POST'])
def incEpisodeNum(seriesID):
    nv = NextVideo("mark")
    nv.incEpisodeNum(seriesID)
    return json.dumps(nv.getNextEpisode(seriesID))

@app.route("/Series/<seriesID>/Dec", methods=['GET', 'POST'])
def decEpisodeNum(seriesID):
    nv = NextVideo("mark")
    nv.decEpisodeNum(seriesID)
    return json.dumps(nv.getNextEpisode(seriesID))

@app.route("/Series/<seriesID>/IncSeason", methods=['GET', 'POST'])
def incSeasonNum(seriesID):
    nv = NextVideo("mark")
    nv.incSeasonNum(seriesID)
    return json.dumps(nv.getNextEpisode(seriesID))

@app.route("/Series/<seriesID>/DecSeason", methods=['GET', 'POST'])
def decSeasonNum(seriesID):
    nv = NextVideo("mark")
    nv.decSeasonNum(seriesID)
    return json.dumps(nv.getNextEpisode(seriesID))



