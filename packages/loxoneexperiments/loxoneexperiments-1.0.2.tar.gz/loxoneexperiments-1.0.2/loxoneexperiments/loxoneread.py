'''
Created on 15. 4. 2020

@author: ppavlu
'''
import requests
import time
import pathlib

def GetURLContent (URL,USERNAME,USERPWD):
    '''
    Gives back the web-response structure from the URL
    '''
    r=None
    try:
        r=requests.get(URL, auth=(USERNAME,USERPWD))
    except (IOError):
        print ("Access to network server failed: ",URL)
    return r

def GetTimeStamp():
    ts=time.time()
    return ts

def AddToLogFile(folder,log,text):
    #Create the log directory in case it does not exist
    pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
    #write one-line entry to the logfile. If not existing, create it
    fname=folder+"\\"+log
    with open(fname,"a") as fh:
        fh.write(text+"\n")

def GetValue(line):
    valueSegmentStart=line.find('value=')
    valueSegmentEnd=line.find('Code=')
    valueSegment=line[valueSegmentStart:valueSegmentEnd-1]
    #print('>>'+valueSegment+'<<')
    valStart=valueSegment.find('"')+1
    #valEnd=valueSegment.rfind('"')-2
    valEnd=len(valueSegment)
    while not valueSegment[valEnd-1].isdigit():
        valEnd=valEnd-1
    valString=valueSegment[valStart:valEnd]
    #print('>>'+valString+'<<')
    if valString.isalnum():
        value=int(valString)
    else:
        value=float(valString)
    return value

def GetData(MINISERVERREADURL, DATAID, USERNAME, USERPWD):
    print("Reading current value for: ", DATAID)
    buildURL=MINISERVERREADURL+"io/"+DATAID
    # print(buildURL)
    result=GetURLContent(buildURL, USERNAME, USERPWD)
    response=None
    if (result != None):
        if result.ok:
            #data=GetValue(DATAID, result.text)
            #print(result.ok, result.text)
            response=(GetTimeStamp(),GetValue(result.text))
        else:
            print("Error reading data from server")
    return response

if __name__ == '__main__':
    pass