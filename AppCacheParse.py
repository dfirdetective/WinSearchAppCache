'''This will not work right now as I haven't added navigation to the right folder. 
I was just running tests to view the data in different samples from the same folder
with a known name.
'''

import json
import csv

filename = "AppCache.txt"

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
#        csv_writer.writerow(d.values())
        dValues = list(d.values())
        dData = []
        for item in dValues:
            vKeys = list(item.keys())   #vKeys: ['Value', 'Type'] Type seems to just mean alpha(12) or numeric(5)
            for v in vKeys:
                if v.startswith("Value"):
                    dData.append(item[v])
        csv_writer.writerow(dData)
appCache.close()
