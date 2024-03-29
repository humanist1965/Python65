'''
Simple Folder/File based database.

Provides features to store JSON/YAML objects in local file system based database.
'''
import json
import sys, os
import os.path
import pathlib
import shutil
import yaml  

class FileDB:
    def __init__(self, dbROOT=None):
        """Constructor"""
        if dbROOT is None:
            # self.dbROOT = self._getDefaultRoot()
            self.dbROOT = "/home/ubuntu/Python65/NextVideo"
        self.dbROOT = self._optSep(self.dbROOT) + "$$DATASTORE$$"
        self._createPathIfNeeded(self.dbROOT)
    
    def storeJSON(self, relPath, obj):
        # Assuming obj is a dict
        # with open('result.json', 'w') as fp:
        if type(obj) is str:
            # assume it is already a valid JSON string
            str1 = obj
        else:
            str1 = json.dumps(obj)
        path = self._getDefaultRoot() + self._optSep(relPath)
        self._createPathIfNeeded(path)
        # print("storeJSON path={0} JSON: {1}".format(path,str1))
        self._storeJSON(path,str1)

    def _storeJSON(self, path, jsonStr):
        with open(path + 'data.json', 'w') as fp:
            fp.write(jsonStr)

    def _optSep(self, relPath, addToEnd = True):
        if relPath[0] != "/":
            relPath = "/" + relPath
        if addToEnd == True:
            if relPath[len(relPath)-1] != "/":
                relPath = relPath + "/"
        return relPath

    def _createPathIfNeeded(self, path):
        pathlib.Path(path).mkdir(parents=True, exist_ok=True) 

    def getSubKeys(self, relPath):
        try:
            path = self._getDefaultRoot() + self._optSep(relPath)
            onlyfiles = [os.path.join(relPath, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) == False ]

            return onlyfiles
        except:
            return []

    def getJSON(self, relPath):
        path = self._getDefaultRoot() + self._optSep(relPath)
        try:
            with open(path + 'data.json', 'r') as fp:
                return fp.read()
        except:
            return ""
    
    def getObj(self, relPath):
        jsonStr = self.getJSON(relPath)
        dictRet = yaml.load(jsonStr, Loader=yaml.FullLoader)
        return dictRet

    def getYAML(self, relFilePath):
        relFilePath = self._addYamlExtIfNeeded(relFilePath)
        path = self._getYAMLRoot() + self._optSep(relFilePath, False)
        with open(path, 'r') as fp:
            try:
                dictRet = yaml.load(fp, Loader=yaml.FullLoader)
                return dictRet
            except yaml.YAMLError as exc:
                print(exc)

    def _addYamlExtIfNeeded(self,relFilePath):
        endStr = relFilePath[-4:]
        if endStr != ".yml": 
            relFilePath = relFilePath + ".yml"
        return relFilePath

    def convertToJSON(self, obj):
        jsonStr = json.dumps(obj)
        return jsonStr



    def clearDB(self):
        path = self._getDefaultRoot()
        # print("About to purge DB: {0}".format(path))
        shutil.rmtree(path)

    def _getDefaultRoot(self):

        if self._rootDBExists():
            return self.dbROOT
        else:
            print("Getting Default DB Root Path")
            print('sys.argv[0] =', sys.argv[0])             
            pathname = os.path.dirname(sys.argv[0])     
            print('path =', pathname)
            print('full path =', os.path.abspath(pathname)) 
            pathname = os.path.abspath(pathname)
            
            return pathname 

    def _getYAMLRoot(self):
        if self._rootYAMLExists():
             # pylint: disable=E0203
            return self.yamlROOT
        else:
            dbRoot = self._optSep(self._getDefaultRoot())
            yamlRoot = dbRoot + "../YAML_FILES"
            self.yamlROOT = yamlRoot
            return yamlRoot

    def _rootDBExists(self):
        try:
            self.dbROOT
            return True
        except:
            return False

    def _rootYAMLExists(self):
        try:
            self.yamlROOT
            return True
        except:
            return False
        

    def DEBUG(self):
        print("self.dbROOT = {0}".format(self.dbROOT))

   




def main():
    dbObj = FileDB()
    dbObj.clearDB()
    dict1 = {'Name': 'Zara', 'Age': 7, 'Class': 'First', 'field1':777}
    dbObj.storeJSON("/mark/sharon/andrew/ellie/John/", dict1)
    dbObj.DEBUG()
    json1 = dbObj.getJSON("/mark/sharon/andrew/ellie/John")
    print("getJSON returned: {0} ".format(json1))
    yamlObj = dbObj.getYAML("GOT3.yml")
    jsonStr = dbObj.convertToJSON(yamlObj)
    print("getYAML returned: {0} ".format(jsonStr))

if __name__ == '__main__':
    print("Running Main")
    main()
    