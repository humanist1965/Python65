from NextVideo import NextVideo
from flask import Flask
import json
app = Flask(__name__)

# --------------------------------------------------------
# define the webserver API routes

@app.route("/")
def help():
    return "<h1>NextVideo API</h1>2222"

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

@app.route("/Series/<seriesID>/Inc")
def incEpisodeNum(seriesID):
    nv = NextVideo("mark")
    nv.incEpisodeNum(seriesID)
    return json.dumps(nv.getNextEpisode(seriesID))

@app.route("/Series/<seriesID>/Dec")
def decEpisodeNum(seriesID):
    nv = NextVideo("mark")
    nv.decEpisodeNum(seriesID)
    return json.dumps(nv.getNextEpisode(seriesID))

@app.route("/Series/<seriesID>/IncSeason")
def incSeasonNum(seriesID):
    nv = NextVideo("mark")
    nv.incSeasonNum(seriesID)
    return json.dumps(nv.getNextEpisode(seriesID))

@app.route("/Series/<seriesID>/DecSeason")
def decSeasonNum(seriesID):
    nv = NextVideo("mark")
    nv.decSeasonNum(seriesID)
    return json.dumps(nv.getNextEpisode(seriesID))



