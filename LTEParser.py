import json
import csv
import requests
from datetime import datetime

# now = datetime.now()

HOST = 'gcs.iotocean.org:7579'
CSEbase = 'Mobius'

DroneName = "KETI_SKT_LTE"
parseDate = "20220920T000000"

cinList = []
data = []
DefineKeys = ['Carrier', 'lat', 'lon', 'alt', 'RSRP', 'RSRQ', 'RSSI']
# parseDate = "20220926T000000"
# MobileCarrier = "skt"


# ofst = 0



index = 0

# url = "http://" + HOST + "/" + MOBIUS + "/KETI_MUV/Mission_Data/" + DroneName + "/msw_" + MobileCarrier.lower() + \
#           "_lte/LTE/la"

def GetDataList():
    global HOST
    global CSEbase
    global DroneName
    global parseDate
    global cinList

    dataUrl = "http://" + HOST + "/" + CSEbase + "/KETI_MUV/Mission_Data/" + DroneName + "/msw_lte/LTE?rcn=4&ty=4&cra="\
              + str(parseDate)

    payload = {}
    headers = {
        'Accept': 'application/json',
        'X-M2M-RI': '12345',
        'X-M2M-Origin': 'SOrigin'
    }

    try:
        response = requests.request("GET", dataUrl, headers=headers, data=payload)
        cinList = json.loads(response.text)['m2m:rsp']['m2m:cin']

        parseCinCon(List=cinList)
        # print(cinList)

    except Exception as e:
        print(e)


def parseCinCon(List):
    # ct = List[len(List) - 1].__getitem__('ct')
    # print(ct[0:8])
    global parseDate
    global data

    for i in range(len(List)):  # parse of specific date
        ct = List[len(List)-1-i].__getitem__('ct')
        if ct[0:8] == parseDate[0:8]:
            con = List[len(List)-1-i].__getitem__('con')
            Carrier = json.loads(con)['Carrier']
            print(type(Carrier))


# def saveCSV():
#     global DefineKeys
#
#     with open(DroneName + '-' + now.strftime('%Y-%m-%dT%H-%M') + ".csv", 'w') as file:
#         writer = csv.writer(file)
#         writer.writerows(data)

if __name__ == '__main__':
    GetDataList()