'''
Simple Folder/File based database.

Provides features to store JSON/YAML objects in local file system based database.
'''
import sys, os

class FileDB:
    def __init__(self, dbROOT=None):
        """Constructor"""
        if dbROOT is None:
            self._getDefaultRoot()
    
    def storeJSON(self, relPath, jsonMSG):
        pass

    def getJSON(self, relPath):
        pass

    def _getDefaultRoot(self):
        print("Getting Default DB Root Path")
        print('sys.argv[0] =', sys.argv[0])             
        pathname = os.path.dirname(sys.argv[0])     
        print('path =', pathname)
        print('full path =', os.path.abspath(pathname)) 
        
        print("CWD=")
        print(os.getcwd())
        return pathname 




def main():
    dbObj = FileDB()
    dbObj.storeJSON("mark","jsonMSG")

if __name__ == '__main__':
    print("Running Main")
    main()
    