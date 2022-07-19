"""
This is a v2 test.
Intent: Parse app data from within AppCacheXXXXXXXXXXXXXXXXXX.txt
"""

from pathlib import Path
import json
import csv
import os
import shutil

homeDir = Path.home()
p = str(homeDir)
appCacheLoc = p + '\\AppData\\Local\\Packages\\Microsoft.Windows.Search_cw5n1h2txyewy\\LocalState\\DeviceSearchCache'
outputPath = Path.cwd() / 'WinSearchAppCache'


def file_exists(file):
    with open(file) as appCache:
        data = json.load(appCache)
        outputFile = str(outputPath) + "\\cacheOutput.csv"
        cacheOutput = open(outputFile, 'w')
        csv_writer = csv.writer(cacheOutput)
        count = 0
        for d in data:
            if count == 0:
                header = list(d.keys())
                writehead = []
                for x in header:
                    if x[0:7] == "System.":
                        y = x[7:]
                        writehead.append(y)
                csv_writer.writerow(writehead)
                count += 1
            dValues = list(d.values())
            dData = []
            for item in dValues:
                vKeys = list(item.keys())
                for v in vKeys:
                    if v.startswith("Value"):
                        dData.append(item[v])
            csv_writer.writerow(dData)
    print("Parsed data printed to " + outputFile)
    appCache.close()


def find_app_cache(username):
    try:
        shutil.copytree(appCacheLoc, outputPath)
        print("Host folder copied to " + str(outputPath))
        for folderName, subfolders, filenames in os.walk(outputPath):
            for filename in filenames:
                if "AppCache" in str(filename):
                    cachefile = Path(outputPath) / filename
                    file_exists(cachefile)

    except:
        print("Error. File or folder not found.")


def target_host():
    if str(homeDir.anchor)[0].isalpha():
        username = homeDir.parts[2]
        find_app_cache(username)
    else:
        print("This is intended to target the host machine by locating C: drive.")

print("Running WinSearchAppCache...")
target_host()
print("WinSearchAppCache Complete!")
