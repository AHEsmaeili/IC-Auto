from datetime import datetime, timedelta
import pymice as pm
import numpy as np
import pytz


def gtimeline(data, name,filedir):

    # Duration of the experiment file
    start = data.getStart().replace(hour = 8, minute = 0, second = 0, microsecond = 0, tzinfo = None)
    end = data.getEnd().replace(hour = 20, minute = 0, second = 0 , microsecond = 0, tzinfo = None)

    # Creating phases
    timeranges = []
    for i in range(int((end-start).total_seconds()/43200)+1):
        timeranges.append(start + i*timedelta(hours = 12))
    ziptimes = zip(timeranges[0:-1],timeranges[1:])

    # Writing to .ini file
    f = open(name[:name.rfind(".")] + '.ini', 'w+')
    for ind, val in enumerate(ziptimes):
        if ind % 2 == 0:
            pind = ind//2 + 1
        if val[0].hour == 8: # Start of light phase
            f.write("[%dL]\n" %pind)
        elif val[0].hour == 20: # Start of dark phase
            f.write("[%dD]\n" %pind)
        f.write("starT= %s\n" %str(val[0]))
        f.write("end = %s\n" %str(val[1]))
        f.write("tzinfo = Etc/GMT-3\n\n") # Timezone information
    f.close()