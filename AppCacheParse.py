"""
AppCacheParse.py
Author: Cassie Doemel
Intent: AppCacheXXXXXXXXXXXXXXXXXX.txt to csv for readability for my research
Current Iteration: Collects and parses artifact from host Windows machine. 
Run from your desired output directory. Will create WinSearchAppCache folder 
with subdirectory of the POSIX timestamp at run time. Directory will contain 
raw AppCache file, SettingsCache file, and the cacheOutput.csv parsed data.
Future: Create CLI args to allow for parse-only or mounted directory selection.
"""

from pathlib import Path
import json
import csv
import os
import shutil
from datetime import datetime


homeDir = Path.home()
p = str(homeDir)
dt = datetime.now()
ts = datetime.timestamp(dt)
appCacheLoc = p + '\\AppData\\Local\\Packages\\Microsoft.Windows.Search_cw5n1h2txyewy\\LocalState\\DeviceSearchCache'
outputPath = Path.cwd() / 'WinSearchAppCache' / str(ts)

#   TODO create command-line arguments to run against whatever is needed

def file_exists(file):
    with open(file) as appCache:
        data = json.load(appCache)
        outputFile = str(outputPath) + "\\cacheOutput.csv"
        cacheOutput = open(outputFile, 'w')     # Creates the output file
        csv_writer = csv.writer(cacheOutput)
        count = 0
        for d in data:
            if count == 0:                      # Writes the 0 row as headers
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
            for item in dValues:                # Writes the rest as values
                vKeys = list(item.keys())
                for v in vKeys:
                    if v.startswith("Value"):   # Strips off "Type: "
                        dData.append(item[v])
            csv_writer.writerow(dData)
    print("Parsed data printed to " + outputFile)
    appCache.close()                            # Closes the file so it can be viewed.


def find_app_cache(username):
    try:
        shutil.copytree(appCacheLoc, outputPath)    # Copies AppCache & SettingsCache
        print("Host folder copied to " + str(outputPath))
        for folderName, subfolders, filenames in os.walk(outputPath):
            for filename in filenames:
                if "AppCache" in str(filename):
                    cachefile = Path(outputPath) / filename
                    file_exists(cachefile)

    except Exception as inst:
        print(type(inst), " - ", inst.args)

def target_host():
    if str(homeDir.anchor)[0].isalpha():    # checking for C: at root
        username = homeDir.parts[2]         # pulling the username - was needed in previous iterations TODO remove
        find_app_cache(username)
    else:
        print("This is intended to target the host machine by locating C: drive.")

print("Running WinSearchAppCache...     Start time: ", dt)
target_host()
dt = datetime.now()
print("WinSearchAppCache Complete!     End time: ", dt)
