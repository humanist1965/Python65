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
    ns.createYAMLfromTVHOMEUrl("Billions",1,"TVHOME_RAW/Billions1.html")
    ns.createYAMLfromTVHOMEUrl("Billions",2,"TVHOME_RAW/Billions2.html")
    ns.createYAMLfromTVHOMEUrl("Billions",3,"TVHOME_RAW/Billions3.html")
    # print(ns._extractVideoLinks(str1))

if __name__ == '__main__':
    main()