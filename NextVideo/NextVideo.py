from FileDB import FileDB
import datetime

'''
NextVideo business logic API.
'''

class NextVideo:

    def __init__(self, userID):
        """Constructor"""
        self.userID = userID
        self._loadUserData()

    # Public interface methods
    def listAllSeries(self):
        return self.allList 

    def listCarryOnWatchList(self):
        return self.watchList

    def getNextEpisode(self,seriesID):
        userObj = self.watchListDict[seriesID]
        curSeasonNum = userObj['currentSeasonNumber']
        curEpisodeNum = userObj['nextEpisodeNumber']
        seasonData = self._loadSeasonData(seriesID, curSeasonNum)
        episodeData = self._getEpisodeData(seasonData, curEpisodeNum)
        userObj["url"] = episodeData["url"]
        return userObj

    def playEpisodeNum(self,seriesID):
        # Actually this will be triggered from the play event on the ui
        # but all we are doing here is updating the lastWatchedDate field
        # This field is important because it determined which series will appear first in the list of ones to watch.
        
        dtStr = datetime.datetime.today().strftime('%Y-%m-%d %H.%M.%S')
        self._updateUserData(seriesID, 'lastWatchedDate', dtStr)
        self._saveUserData()

    def incEpisodeNum(self,seriesID, incNum = 1):
        userObj = self.watchListDict[seriesID]
        curSeasonNum = int(userObj['currentSeasonNumber'])
        curEpisodeNum = int(userObj['nextEpisodeNumber'])
        curEpisodeNum = curEpisodeNum + incNum
        self._updateUserData(seriesID, 'nextEpisodeNumber', curEpisodeNum)
        try:
            userObj = self.getNextEpisode(seriesID)
        except:
            # No more episode this season
            curSeasonNum = curSeasonNum + self._incByOne(incNum)
            if curSeasonNum < 1:
                curSeasonNum = 1
            curEpisodeNum = self._incOrDecSeasonStart(seriesID, curSeasonNum, self._incByOne(incNum))
            self._updateUserData(seriesID, 'currentSeasonNumber', curSeasonNum)
            self._updateUserData(seriesID, 'nextEpisodeNumber', curEpisodeNum)
            try:
                userObj = self.getNextEpisode(seriesID)
            except: 
                # No more seasons for this series
                # For time being let's just wrap around to first season again
                curSeasonNum = 1
                curEpisodeNum = 1
                self._updateUserData(seriesID, 'currentSeasonNumber', curSeasonNum)
                self._updateUserData(seriesID, 'nextEpisodeNumber', curEpisodeNum)
        self._saveUserData()

    @staticmethod
    def _incByOne(incNum):
        if incNum > 0:
            return 1
        else:
            return -1

    def _incOrDecSeasonStart(self, seriesID, curSeasonNum, incNum):
        if incNum == 1:
            return 1
        else:
            seasonData = self._loadSeasonData(seriesID, curSeasonNum)
            return len(seasonData)


    def decEpisodeNum(self, seriesID):
        self.incEpisodeNum(seriesID,incNum=-1)

    def incSeasonNum(self, seriesID):
        # increment by a big number to force a season update
        self.incEpisodeNum(seriesID,incNum=100)
        

    def decSeasonNum(self, seriesID):
        # decrement by a big number to force a season update
        self.incEpisodeNum(seriesID,incNum=-100)

    # Private implementation methods   

    def _loadUserData(self):
        uid = self.userID
        dbObj = FileDB()

        # Get all series List
        self.allList = dbObj.getYAML("AllSeriesList")
        allDict = {}
        for it in self.allList:
            seriesID = it["seriesID"]
            allDict[seriesID] = it

        # Get user data dict(seriesID, currentSeasonNumber, nextEpisodeNumber, lastWatchedDate )
        watchListKeys = dbObj.getSubKeys(uid)
        
        watchList = []
        for key in watchListKeys:
            userObj = dbObj.getObj(key)
            watchList.append(userObj)
        watchList.sort(key=lambda x: x["lastWatchedDate"] , reverse=True) # x.lastWatchedDate
        
        # Supplement information on user watchList with global details in allDict
        consideredList = {}
        extendedWatchList = []
        for it in watchList:
            seriesID = it["seriesID"]
            globDetails = allDict[seriesID]
            it["name"] = globDetails["name"]
            it["image"] = globDetails["image"]
            extendedWatchList.append(it)
            consideredList[seriesID] = True
        
        # At the moment as part of MVP include any missing global items onto the user watchList
        # May change this in future to require users to add Series they want to watch
        for it in self.allList:
            seriesID = it["seriesID"]
            if not seriesID in consideredList:
                it['currentSeasonNumber'] = 1
                it['nextEpisodeNumber'] = 1
                it['lastWatchedDate'] = "1900-01-01"
                extendedWatchList.append(it)
        
        # print("EXTENDED WATCH LIST")
        # print(extendedWatchList)
        self.watchList = extendedWatchList
        watchListDict = {}
        for it in extendedWatchList:
            seriesID = it["seriesID"]
            watchListDict[seriesID] = it
        self.watchListDict = watchListDict


    def _loadSeasonData(self, seriesID, curSeasonNum):
        dbObj = FileDB()
        key = seriesID + str(curSeasonNum)
        seasonData = dbObj.getYAML(key)
        return seasonData

    def _getEpisodeData(self, seasonData, curEpisodeNum):
        curEpisodeNum = int(curEpisodeNum)
        maxLen = len(seasonData)
        if curEpisodeNum > maxLen:
            raise ValueError("Episode Index out of range")
        elif curEpisodeNum < 1:
            raise ValueError("Episode Index out of range")
        return seasonData[curEpisodeNum-1]

    def _updateUserData(self, seriesID, key, value):
        userObj = self.watchListDict[seriesID]
        userObj[key] = value
        self.watchListDict[seriesID] = userObj

    def _saveUserData(self):
        uid = self.userID
        dbObj = FileDB()
        for key in self.watchListDict:
            it = self.watchListDict[key]
            seriesID = it["seriesID"]
            key = uid + "/" + seriesID
            dbObj.storeJSON(key, it)


        
def _testUserData():
    dbObj = FileDB()
    dbObj.clearDB()
    dict1 = {'seriesID': 'GOT', 'currentSeasonNumber': 1, 'nextEpisodeNumber': '1', 'lastWatchedDate':"2020-11-14"}
    dbObj.storeJSON("mark/GOT", dict1)
    dict1 = {'seriesID': 'Billions', 'currentSeasonNumber': 1, 'nextEpisodeNumber': '1', 'lastWatchedDate':"2018-11-14"}
    dbObj.storeJSON("mark/Billions", dict1)

def main():
    _testUserData()
    # pylint: disable=W0612
    nv = NextVideo("mark")
    allSeries = nv.listAllSeries()
    print("All Series:")
    print(allSeries)
    print("My WatchList:")
    myWatchList = nv.listCarryOnWatchList()
    print(myWatchList)
    print("Next Episode:")
    nextEpisode = nv.getNextEpisode("GOT")
    print(nextEpisode)
    print("Increment Episode")
    for i in range(39):
        nv.incEpisodeNum("GOT")
        nextEpisode = nv.getNextEpisode("GOT")
        print(nextEpisode)
    print("Decrement Episode")
    for i in range(40):
        nv.decEpisodeNum("GOT")
        nextEpisode = nv.getNextEpisode("GOT")
        print(nextEpisode)
    print("Increment Season")
    for i in range(3):
        nv.incSeasonNum("GOT")
        nextEpisode = nv.getNextEpisode("GOT")
        print(nextEpisode)
    print("Decrement Season")
    for i in range(5):
        nv.decSeasonNum("GOT")
        nextEpisode = nv.getNextEpisode("GOT")
        print(nextEpisode)


if __name__ == '__main__':
    print("Running Next Video Test")
    main()
            
