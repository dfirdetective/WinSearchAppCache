"""
AppCacheParse.py v3
Author: Cassie Doemel
Intent: AppCacheXXXXXXXXXXXXXXXXXX.txt to csv for readability for my research
Current Iteration: Collects and parses artifact from host Windows machine.
Run from your desired output directory. Will create WinSearchAppCache folder
with subdirectory of the POSIX timestamp at run time. Directory will contain
raw AppCache file, SettingsCache file, and the two Output.csv parsed data files.

Future TODO: Create CLI args to allow for parse-only or mounted directory selection.
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


#   TODO create command-line arguments to run against whatever you want.

def acfile_exists(file):
    with open(file, encoding='utf=8') as appCache:
        data = json.load(appCache)
        outputFile = str(outputPath) + "\\" + file.stem + "-Output.csv"
        cacheOutput = open(outputFile, 'w')  # Creates the output file
        csv_writer = csv.writer(cacheOutput)
        count = 0
        for d in data:
            if count == 0:  # Writes the 0 row as headers
                header = list(d.keys())
                acwritehead = []
                for x in header:
                    if x[0:7] == "System.":
                        y = x[7:]
                        acwritehead.append(y)
                csv_writer.writerow(acwritehead)
                count += 1
            dValues = list(d.values())
            dData = []
            for item in dValues:  # Writes the rest as values
                for v in item.keys():
                    if v.startswith("Value"):  # Strips off "Type: "
                        # if v.islist, iterate over list in some way to clean it up?
                        # .strip(\r\n
                        dData.append(item[v])
            csv_writer.writerow(dData)
    print("Parsed data printed to " + outputFile)
    appCache.close()  # Closes the file so it can be viewed.


def scfile_exists(file):
    with open(file, encoding='utf=8') as scCache:
        data = json.load(scCache)
        outputFile = str(outputPath) + "\\" + file.stem + "-Output.csv"
        cacheOutput = open(outputFile, 'w')  # Creates the output file
        csv_writer = csv.writer(cacheOutput)
        count = 0
        try:
            for d in data:
                if count == 0:  # Writes the 0 row as headers
                    scwritehead = ['ParsingName', 'ActivationContext', 'SmallLogoPath', 'PageID', 'SettingID',
                                   'HostID', 'Condition', 'Comment', 'HighKeywords']
                    csv_writer.writerow(scwritehead)
                    count += 1
                dValues = list(d.values())
                dData = []
                for item in dValues:  # Writes the rest as values
                    for v in item.keys():
                        if v.startswith("Value"):  # Strips off "Type: "
                            dData.append(item[v])
                csv_writer.writerow(dData)

        except UnicodeError:
            print("Error: File closed incomplete due to Unicode error.")    # Repeated fails on Defender line
    print("Parsed data printed to " + outputFile)
    scCache.close()  # Closes the file so it can be viewed.


def find_app_cache():
    try:
        shutil.copytree(appCacheLoc, outputPath)  # Copies AppCache & SettingsCache
        print("Host folder copied to " + str(outputPath))
        for folderName, subfolders, filenames in os.walk(outputPath):
            for filename in filenames:
                cachefile = Path(outputPath) / filename
                if "AppCache" in filename:
                    acfile_exists(cachefile)
                else:
                    scfile_exists(cachefile)

    except Exception as inst:
        print(type(inst), " - ", inst.args)


def target_host():
    if str(homeDir.anchor)[0].isalpha():  # checking for root drive letter to ID as Windows
        find_app_cache()
    else:
        print("This is intended to target the host Windows machine by locating root drive at this time.")


print("Running WinSearchAppCache...     Start time: ", dt)
target_host()
dt = datetime.now()
print("WinSearchAppCache Complete!     End time: ", dt)
