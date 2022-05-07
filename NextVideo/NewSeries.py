import sys, os
import os.path
import yaml  
import re
from urllib.request import urlopen

'''
NewSeries functions to create the YAML file data needed by a series.
'''
class NewSeries:
    def createYAMLfromTVHOMEUrl(self, seriesID, seasonNum, url):
        if isHttpURL(url):
            urlData = _getHttpURL(url)
        else:
            urlData = _getStrFromFile(url)

        episodeList = self._extractVideoLinks(urlData)
        # print("Debug problem")
        # print(episodeList)
        str_list = ["---\n"]
        for i, ep in enumerate(episodeList): 
            str_list.append("-\n")
            str_list.append("  episode: {0}\n".format(i+1))
            str_list.append("  url: {0}\n".format(ep))

        outStr = ''.join(str_list)
        self._saveToYAMLFile(seriesID, seasonNum, outStr)

    def _extractVideoLinks(self, searchStr):
        regExpStr = r'href="/play.php.*"'
        matches = re.findall(regExpStr, searchStr, re.M)
        urlPathList = []
        for it in matches:
            modIt = it[6:]
            modIt = modIt[:-1]
            modIt = "http://tvhome.cc" + modIt
            if modIt.endswith("|1"):
                modIt = modIt[0:len(modIt)-2]
            if not modIt.endswith("|2"):
                urlPathList.append(modIt)
        return urlPathList[::-1]
   
    def _saveToYAMLFile(self, seriesID, seasonNum, outStr):
        pathname = os.path.dirname(sys.argv[0]) 
        pathname += "/YAML_FILES/" + seriesID + str(seasonNum) + ".yml"
        
        if os.path.isfile(pathname):
            print("Error file already exists - aborting!:" + pathname)
            return

        try:
            with open(pathname, 'w') as fp:
                fp.write(outStr)
                fp.close()
        except:
            print("Error opening file:" + pathname)

def isHttpURL(url):
    return (url.find("http:") > -1)

def _getStrFromFile(relFilePath):
    pathname = os.path.dirname(sys.argv[0]) 
    pathname += "/" + relFilePath
    try:
        with open(pathname, 'r') as fp:
            return fp.read()
    except:
        print("Error opening file:" + pathname)

def _getHttpURL(url):
    f = urlopen(url)
    urlData = f.read()
    return str(urlData)

def main():
    # str1 = _getStrFromFile("tests/data/tvhome.txt")
    ns = NewSeries()
    # ns.createYAMLfromTVHOMEUrl("WestWorld",1,"TVHOME_RAW/WestWorld1.html")
    # ns.createYAMLfromTVHOMEUrl("WestWorld",2,"TVHOME_RAW/WestWorld2.html")
    # ns.createYAMLfromTVHOMEUrl("GOT",5,"TVHOME_RAW/GOT5.html")
    # ns.createYAMLfromTVHOMEUrl("GOT",6,"TVHOME_RAW/GOT6.html")
    # ns.createYAMLfromTVHOMEUrl("GOT",7,"TVHOME_RAW/GOT7.html")
    # ns.createYAMLfromTVHOMEUrl("Billions",1,"TVHOME_RAW/Billions1.html")
    # ns.createYAMLfromTVHOMEUrl("Billions",2,"TVHOME_RAW/Billions2.html")
    # ns.createYAMLfromTVHOMEUrl("Billions",3,"TVHOME_RAW/Billions3ls.html")

    # ns.createYAMLfromTVHOMEUrl("BigBang",1,"TVHOME_RAW/TBBT1.html")
    # ns.createYAMLfromTVHOMEUrl("BigBang",2,"TVHOME_RAW/TBBT2.html")
    # ns.createYAMLfromTVHOMEUrl("BigBang",3,"TVHOME_RAW/TBBT3.html")
    # ns.createYAMLfromTVHOMEUrl("BigBang",4,"TVHOME_RAW/TBBT4.html")
    # ns.createYAMLfromTVHOMEUrl("BigBang",5,"TVHOME_RAW/TBBT5.html")
    # ns.createYAMLfromTVHOMEUrl("BigBang",6,"TVHOME_RAW/TBBT6.html")
    # ns.createYAMLfromTVHOMEUrl("BigBang",7,"TVHOME_RAW/TBBT7.html")
    # ns.createYAMLfromTVHOMEUrl("BigBang",8,"TVHOME_RAW/TBBT8.html")
    # ns.createYAMLfromTVHOMEUrl("BigBang",9,"TVHOME_RAW/TBBT9.html")
    # ns.createYAMLfromTVHOMEUrl("BigBang",10,"TVHOME_RAW/TBBT10.html")
    # ns.createYAMLfromTVHOMEUrl("BigBang",11,"TVHOME_RAW/TBBT11.html")
    # ns.createYAMLfromTVHOMEUrl("BigBang",12,"TVHOME_RAW/TBBT12.html")

    # ns.createYAMLfromTVHOMEUrl("SF",1,"TVHOME_RAW/SF1.html")
    # ns.createYAMLfromTVHOMEUrl("SF",2,"TVHOME_RAW/SF2.html")
    # ns.createYAMLfromTVHOMEUrl("SF",3,"TVHOME_RAW/SF3.html")
    # ns.createYAMLfromTVHOMEUrl("SF",4,"TVHOME_RAW/SF4.html")
    # ns.createYAMLfromTVHOMEUrl("SF",5,"TVHOME_RAW/SF5.html")
    # ns.createYAMLfromTVHOMEUrl("SF",6,"TVHOME_RAW/SF6.html")
    # ns.createYAMLfromTVHOMEUrl("SF",7,"TVHOME_RAW/SF7.html")
    # ns.createYAMLfromTVHOMEUrl("SF",8,"TVHOME_RAW/SF8.html")
    # ns.createYAMLfromTVHOMEUrl("SF",9,"TVHOME_RAW/SF9.html")

    # ns.createYAMLfromTVHOMEUrl("SV",1,"TVHOME_RAW/SV1.html")
    # ns.createYAMLfromTVHOMEUrl("SV",2,"TVHOME_RAW/SV2.html")
    # ns.createYAMLfromTVHOMEUrl("SV",3,"TVHOME_RAW/SV3.html")
    # ns.createYAMLfromTVHOMEUrl("SV",4,"TVHOME_RAW/SV4.html")
    # ns.createYAMLfromTVHOMEUrl("SV",5,"TVHOME_RAW/SV5.html")
    # print(ns._extractVideoLinks(str1))

    # ns.createYAMLfromTVHOMEUrl("GLEE",1,"TVHOME_RAW/glee1.html")
    # ns.createYAMLfromTVHOMEUrl("GLEE",2,"TVHOME_RAW/glee2.html")
    # ns.createYAMLfromTVHOMEUrl("GLEE",3,"TVHOME_RAW/glee3.html")
    # ns.createYAMLfromTVHOMEUrl("GLEE",4,"TVHOME_RAW/glee4.html")
    # ns.createYAMLfromTVHOMEUrl("GLEE",5,"TVHOME_RAW/glee5.html")
    # ns.createYAMLfromTVHOMEUrl("GLEE",6,"TVHOME_RAW/glee6.html")

    # ns.createYAMLfromTVHOMEUrl("MANH",1,"TVHOME_RAW/manh1.html")
    # ns.createYAMLfromTVHOMEUrl("MANH",2,"TVHOME_RAW/manh2.html")

    # ns.createYAMLfromTVHOMEUrl("MRROBOT",1,"TVHOME_RAW/mrrobot1.html")
    # ns.createYAMLfromTVHOMEUrl("MRROBOT",2,"TVHOME_RAW/mrrobot2.html")
    # ns.createYAMLfromTVHOMEUrl("MRROBOT",3,"TVHOME_RAW/mrrobot3.html")

    # ns.createYAMLfromTVHOMEUrl("WDEAD",1,"TVHOME_RAW/wdead1.html")
    # ns.createYAMLfromTVHOMEUrl("WDEAD",2,"TVHOME_RAW/wdead2.html")
    # ns.createYAMLfromTVHOMEUrl("WDEAD",3,"TVHOME_RAW/wdead3.html")
    # ns.createYAMLfromTVHOMEUrl("WDEAD",4,"TVHOME_RAW/wdead4.html")
    # ns.createYAMLfromTVHOMEUrl("WDEAD",5,"TVHOME_RAW/wdead5.html")
    # ns.createYAMLfromTVHOMEUrl("WDEAD",6,"TVHOME_RAW/wdead6.html")
    # ns.createYAMLfromTVHOMEUrl("WDEAD",7,"TVHOME_RAW/wdead7.html")
    # ns.createYAMLfromTVHOMEUrl("WDEAD",8,"TVHOME_RAW/wdead8.html")
    # ns.createYAMLfromTVHOMEUrl("WDEAD",9,"TVHOME_RAW/wdead9.html")

    # ns.createYAMLfromTVHOMEUrl("DOWNA",1,"TVHOME_RAW/downa1.html")
    # ns.createYAMLfromTVHOMEUrl("DOWNA",2,"TVHOME_RAW/downa2.html")
    # ns.createYAMLfromTVHOMEUrl("DOWNA",3,"TVHOME_RAW/downa3.html")
    # ns.createYAMLfromTVHOMEUrl("DOWNA",4,"TVHOME_RAW/downa4.html")
    # ns.createYAMLfromTVHOMEUrl("DOWNA",5,"TVHOME_RAW/downa5.html")
    # ns.createYAMLfromTVHOMEUrl("DOWNA",6,"TVHOME_RAW/downa6.html")

    # ns.createYAMLfromTVHOMEUrl("LTOWER",1,"TVHOME_RAW/ltower1.html")

    # ns.createYAMLfromTVHOMEUrl("Billions",4,"TVHOME_RAW/Billions4.html")

    # ns.createYAMLfromTVHOMEUrl("BLLIES",1,"TVHOME_RAW/bllies1.html")
    # ns.createYAMLfromTVHOMEUrl("BLLIES",2,"TVHOME_RAW/bllies2.html")

    # ns.createYAMLfromTVHOMEUrl("WIRE",1,"TVHOME_RAW/wire1.html")
    # ns.createYAMLfromTVHOMEUrl("WIRE",2,"TVHOME_RAW/wire2.html")
    # ns.createYAMLfromTVHOMEUrl("WIRE",3,"TVHOME_RAW/wire3.html")
    # ns.createYAMLfromTVHOMEUrl("WIRE",4,"TVHOME_RAW/wire4.html")
    # ns.createYAMLfromTVHOMEUrl("WIRE",5,"TVHOME_RAW/wire5.html")

    # ns.createYAMLfromTVHOMEUrl("CURB",1,"TVHOME_RAW/curb1.html")
    # ns.createYAMLfromTVHOMEUrl("CURB",2,"TVHOME_RAW/curb2.html")
    # ns.createYAMLfromTVHOMEUrl("CURB",3,"TVHOME_RAW/curb3.html")
    # ns.createYAMLfromTVHOMEUrl("CURB",4,"TVHOME_RAW/curb4.html")
    # ns.createYAMLfromTVHOMEUrl("CURB",5,"TVHOME_RAW/curb5.html")
    # ns.createYAMLfromTVHOMEUrl("CURB",6,"TVHOME_RAW/curb6.html")
    # ns.createYAMLfromTVHOMEUrl("CURB",7,"TVHOME_RAW/curb7.html")
    # ns.createYAMLfromTVHOMEUrl("CURB",8,"TVHOME_RAW/curb8.html")
    # ns.createYAMLfromTVHOMEUrl("CURB",9,"TVHOME_RAW/curb9.html")

    # ns.createYAMLfromTVHOMEUrl("BORG",1,"TVHOME_RAW/borg1.html")
    # ns.createYAMLfromTVHOMEUrl("BORG",2,"TVHOME_RAW/borg2.html")
    # ns.createYAMLfromTVHOMEUrl("BORG",3,"TVHOME_RAW/borg3.html")
    # ns.createYAMLfromTVHOMEUrl("VIKINGS",5,"TVHOME_RAW/Vikings5.html")

    # ns.createYAMLfromTVHOMEUrl("SEXAC",1,"TVHOME_RAW/sexac1.html")
    # ns.createYAMLfromTVHOMEUrl("SEXAC",2,"TVHOME_RAW/sexac2.html")
    # ns.createYAMLfromTVHOMEUrl("SEXAC",3,"TVHOME_RAW/sexac3.html")
    # ns.createYAMLfromTVHOMEUrl("SEXAC",4,"TVHOME_RAW/sexac4.html")
    # ns.createYAMLfromTVHOMEUrl("SEXAC",5,"TVHOME_RAW/sexac5.html")
    # ns.createYAMLfromTVHOMEUrl("SEXAC",6,"TVHOME_RAW/sexac6.html")

    # ns.createYAMLfromTVHOMEUrl("SOP",1,"TVHOME_RAW/sopranos1.html")
    # ns.createYAMLfromTVHOMEUrl("SOP",2,"TVHOME_RAW/sopranos2.html")
    # ns.createYAMLfromTVHOMEUrl("SOP",3,"TVHOME_RAW/sopranos3.html")
    # ns.createYAMLfromTVHOMEUrl("SOP",4,"TVHOME_RAW/sopranos4.html")
    # ns.createYAMLfromTVHOMEUrl("SOP",5,"TVHOME_RAW/sopranos5.html")
    # ns.createYAMLfromTVHOMEUrl("SOP",6,"TVHOME_RAW/sopranos6.html")

    # ns.createYAMLfromTVHOMEUrl("BOARDW",1,"TVHOME_RAW/boardw1.html")
    # ns.createYAMLfromTVHOMEUrl("BOARDW",2,"TVHOME_RAW/boardw2.html")
    # ns.createYAMLfromTVHOMEUrl("BOARDW",3,"TVHOME_RAW/boardw3.html")
    # ns.createYAMLfromTVHOMEUrl("BOARDW",4,"TVHOME_RAW/boardw4.html")
    # ns.createYAMLfromTVHOMEUrl("BOARDW",5,"TVHOME_RAW/boardw5.html")

    # ns.createYAMLfromTVHOMEUrl("UNDO",1,"TVHOME_RAW/undo1.html")

    # ns.createYAMLfromTVHOMEUrl("MARE",1,"TVHOME_RAW/mare1.html")
    
    # ns.createYAMLfromTVHOMEUrl("WHITEC",1,"TVHOME_RAW/whitec1.html")
    # ns.createYAMLfromTVHOMEUrl("WHITEC",2,"TVHOME_RAW/whitec2.html")
    # ns.createYAMLfromTVHOMEUrl("WHITEC",3,"TVHOME_RAW/whitec3.html")
    # ns.createYAMLfromTVHOMEUrl("WHITEC",4,"TVHOME_RAW/whitec4.html")

    # ns.createYAMLfromTVHOMEUrl("VINYL",1,"TVHOME_RAW/vinyl1.html")

    # ns.createYAMLfromTVHOMEUrl("FARGO",1,"TVHOME_RAW/fargo1.html")
    # ns.createYAMLfromTVHOMEUrl("FARGO",2,"TVHOME_RAW/fargo2.html")
    # ns.createYAMLfromTVHOMEUrl("FARGO",3,"TVHOME_RAW/fargo3.html")
    # ns.createYAMLfromTVHOMEUrl("FARGO",4,"TVHOME_RAW/fargo4.html")

    # ns.createYAMLfromTVHOMEUrl("FOUNDATION",1,"TVHOME_RAW/foundation1.html")

    # ns.createYAMLfromTVHOMEUrl("THEAMERICANS",1,"TVHOME_RAW/theamericans1.html")
    # ns.createYAMLfromTVHOMEUrl("THEAMERICANS",2,"TVHOME_RAW/theamericans2.html")
    # ns.createYAMLfromTVHOMEUrl("THEAMERICANS",3,"TVHOME_RAW/theamericans3.html")
    # ns.createYAMLfromTVHOMEUrl("THEAMERICANS",4,"TVHOME_RAW/theamericans4.html")
    # ns.createYAMLfromTVHOMEUrl("THEAMERICANS",5,"TVHOME_RAW/theamericans5.html")
    # ns.createYAMLfromTVHOMEUrl("THEAMERICANS",6,"TVHOME_RAW/theamericans6.html")

    ns.createYAMLfromTVHOMEUrl("SUCCESS",1,"TVHOME_RAW/success1.html")

if __name__ == '__main__':
    main()