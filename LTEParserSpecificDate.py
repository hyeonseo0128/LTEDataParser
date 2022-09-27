import json
import csv
import requests

HOST = 'gcs.iotocean.org:7579'
CSEbase = 'Mobius'

DroneName = "KETI_SKT_LTE"
targetDate = "20220926T000000"

cinList = []
data = []
DefineKeys = ['Carrier', 'lat', 'lon', 'alt', 'RSRP', 'RSRQ', 'RSSI']


def GetDataList():
    global HOST
    global CSEbase
    global DroneName
    global targetDate
    global cinList

    dataUrl = "http://" + HOST + "/" + CSEbase + "/KETI_MUV/Mission_Data/" + DroneName + "/msw_lte/LTE?rcn=4&ty=4&cra=" \
              + str(targetDate)

    payload = {}
    headers = {
        'Accept': 'application/json',
        'X-M2M-RI': '12345',
        'X-M2M-Origin': 'SOrigin'
    }

    try:
        response = requests.request("GET", dataUrl, headers=headers, data=payload)
        cinList = json.loads(response.text)['m2m:rsp']['m2m:cin']

        parseLTEData(List=cinList)
        # print(cinList)

    except Exception as e:
        print(e)


def parseLTEData(List):
    global targetDate
    global data

    for i in range(len(List)):  # parse of specific date
        ct = List[len(List) - 1 - i].get('ct')
        if ct[0:8] == targetDate[0:8]:
            con = List[len(List) - 1 - i].get('con')
            Carrier = con.get('Carrier')
            Latitude = con.get('lat')
            Longitude = con.get('lon')
            Altitude = con.get('alt')
            RSRP = con.get('RSRP')
            RSRQ = con.get('RSRQ')
            RSSI = con.get('RSSI')
            parseData = [ct[0:8], Carrier, Latitude, Longitude, Altitude, RSRP, RSRQ, RSSI]
            saveCSV(Data=parseData)
    print('==Finish Parse LTE Data==')

def saveCSV(Data):
    global DefineKeys
    global targetDate
    global writer


    with open(DroneName + '-' + targetDate[0:8] + ".csv", 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(Data)


if __name__ == '__main__':
    with open(DroneName + '-' + targetDate[0:8] + ".csv", 'w') as file:
        writer = csv.writer(file)
        writer.writerow(DefineKeys)
    GetDataList()
