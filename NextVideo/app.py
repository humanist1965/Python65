from NextVideo import NextVideo
from flask import Flask
from flask import render_template
from flask_cors import CORS
from flask import request
import json
app = Flask(__name__)
CORS(app) # Will allow the below API to be accessed from any source

# --------------------------------------------------------
# define the webserver API routes

@app.route("/")
def help():
    return render_template('help.html')
   
@app.route("/Series")
def listAllSeries():
    uid = getUserID()
    nv = NextVideo(uid)
    return json.dumps(nv.listAllSeries()) 

@app.route("/WatchList")
def listCarryOnWatchList():
    uid = getUserID()
    nv = NextVideo(uid)
    return json.dumps(nv.listCarryOnWatchList())

@app.route("/Series/<seriesID>")
def getNextEpisode(seriesID):
    uid = getUserID()
    nv = NextVideo(uid)
    return json.dumps(nv.getNextEpisode(seriesID))

@app.route("/Series/<seriesID>/Play", methods=['GET', 'POST'])
def playEpisodeNum(seriesID):
    uid = getUserID()
    nv = NextVideo(uid)
    nv.playEpisodeNum(seriesID)
    nv.incEpisodeNum(seriesID)
    return json.dumps(nv.getNextEpisode(seriesID))

@app.route("/Series/<seriesID>/Inc", methods=['GET', 'POST'])
def incEpisodeNum(seriesID):
    uid = getUserID()
    nv = NextVideo(uid)
    nv.incEpisodeNum(seriesID)
    return json.dumps(nv.getNextEpisode(seriesID))

@app.route("/Series/<seriesID>/Dec", methods=['GET', 'POST'])
def decEpisodeNum(seriesID):
    uid = getUserID()
    nv = NextVideo(uid)
    nv.decEpisodeNum(seriesID)
    return json.dumps(nv.getNextEpisode(seriesID))

@app.route("/Series/<seriesID>/IncSeason", methods=['GET', 'POST'])
def incSeasonNum(seriesID):
    uid = getUserID()
    nv = NextVideo(uid)
    nv.incSeasonNum(seriesID)
    return json.dumps(nv.getNextEpisode(seriesID))

@app.route("/Series/<seriesID>/DecSeason", methods=['GET', 'POST'])
def decSeasonNum(seriesID):
    uid = getUserID()
    nv = NextVideo(uid)
    nv.decSeasonNum(seriesID)
    return json.dumps(nv.getNextEpisode(seriesID))

def getUserID():
    uid = request.args.get('UID')
    if uid == "NONE":
        uid = "Guest"
    uid = uid.lower()
    return uid

