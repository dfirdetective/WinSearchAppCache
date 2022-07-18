'''This will not work intuitively right now as I haven't added 
automated collection and parsing. 

To get this to work, you will have to collect your own AppCache
file and rename to AppCache.txt or change the 
filename = "AppCache.txt" to your filename. 
'''

import json
import csv

filename = "AppCache.txt"
# TODO Automate artifact collection and parsing.

with open(filename) as appCache:
    data = json.load(appCache)

    cacheOutput = open('cacheOutput.csv', 'w')
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
            vKeys = list(item.keys())   #vKeys: ['Value', 'Type'] Type seems to just mean alpha(12) or numeric(5)
            for v in vKeys:
                if v.startswith("Value"):
                    dData.append(item[v])
        csv_writer.writerow(dData)
appCache.close()
