import os
import wfdb
import os.path
from wfdb import processing, show_ann_labels
from IPython.display import display
import scipy.stats

#1 SECOND == 250 TIMEUNITS
#sampfrom=10000
i = 30
while i < 53:
    if i == 40:
        i = 41
    elif i == 42:
        i = 43
    elif i == 49:
        i = 50

    #Usable for either .atr or .ari files
    fileAtr = str(i)+'.atr'
    fileAri = str(i)+'.ari'
    if os.path.isfile(fileAtr):
        annType = 'atr'
    elif os.path.isfile(fileAri):
        annType = 'ari'
    else:
        print("ann file not found")

    recordNum = str(i)
    print(i)
    record = wfdb.io.rdrecord(recordNum)
    ann = wfdb.rdann(recordNum, annType)
    spl_word = 'vfon: '

    #isolate VFONSET time
    display(record.__dict__["comments"])
    vfonset = record.__dict__["comments"]
    spltVfonset = vfonset[1]
    print(spltVfonset)
    partVfonset = spltVfonset.partition(spl_word)
    print(partVfonset[2])
    finalVfonset = partVfonset[2]
    lastVfonset = finalVfonset.split(":")
    print(lastVfonset)

    #convert the hour, minute, and second time of the VFON into ints
    hourTime = int(lastVfonset[0])
    print(hourTime)
    minuteTime = int(lastVfonset[1])
    print(minuteTime)
    secondTime = int(lastVfonset[2])
    print(secondTime)

    #1 SECOND == (roughly) 250 TIMEUNITS
    #convert seconds to native timescale
    vfonTime = (250*secondTime)+(250*60*minuteTime)+(250*60*60*hourTime)-(250*60*1)
    print(vfonTime)
    vfoffTime = (250*secondTime)+(250*60*minuteTime)+(250*60*60*hourTime)

    vfrecord = wfdb.io.rdrecord(recordNum, sampfrom=vfonTime, sampto=vfoffTime)
    vfann = wfdb.rdann(recordNum, annType, sampfrom=vfonTime, sampto=vfoffTime)

    #sig, fields = wfdb.rdsamp(recordNum, sampfrom=vfonTime, sampto=vfoffTime, channels=[0, 1])
    #wfdb.wrsamp('ecg-record', fs=250, units=['mV', 'mV'], sig_name=['I', 'II'], p_signal=sig, fmt=['16', '16'])
    #cutRecord = wfdb.rdrecord('ecg-record')
    #wfdb.plot_wfdb(cutRecord)

    #Create new cut file and run xqrs on it
    sig, fields = wfdb.rdsamp(recordNum, sampfrom=vfonTime, sampto=vfoffTime)
    newrecordNum = str(i)+'new'
    wfdb.wrsamp(newrecordNum, fs=250, units=['mV', 'mV'], sig_name=['I', 'II'], p_signal=sig, fmt=['16', '16'])
    xqrs = processing.XQRS(sig=sig[:, 0], fs=fields['fs'])
    xqrs.detect()
    display(xqrs.__dict__)
    #wfdb.plot_items(signal=sig, ann_samp=[xqrs.qrs_inds])

    #numpy.savetxt("foo.csv", array, delimiter=",")

    i = i+1
    #wfdb.plot_wfdb(vfrecord)
