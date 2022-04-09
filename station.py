from hashlib import sha1
import hmac
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime
import base64
import json
import math
from requests import request
from pprint import pprint
import geocoder


app_id = 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF'
app_key = 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF'

class Auth():

    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_header(self):
        xdate = format_date_time(mktime(datetime.now().timetuple()))
        hashed = hmac.new(self.app_key.encode('utf8'), ('x-date: ' + xdate).encode('utf8'), sha1)
        signature = base64.b64encode(hashed.digest()).decode()

        authorization = 'hmac username="' + self.app_id + '", ' + \
                        'algorithm="hmac-sha1", ' + \
                        'headers="x-date", ' + \
                        'signature="' + signature + '"'
        return {
            'Authorization': authorization,
            'x-date': format_date_time(mktime(datetime.now().timetuple())),
            'Accept - Encoding': 'gzip'
        }


if __name__ == '__main__':
    a = Auth(app_id, app_key)
    response = request('get', 'https://ptx.transportdata.tw/MOTC/v3/Rail/TRA/Station?$format=JSON', headers= a.get_auth_header())
    data = json.loads(response.text)
    g = geocoder.ip('me')
    positionLon = g.latlng[1]
    positionLat = g.latlng[0]
    length = 99999
    for station in data['Stations']:
        if(math.sqrt(math.pow(station['StationPosition']['PositionLon']-positionLon,2) + math.pow(station['StationPosition']['PositionLat']-positionLat,2))<length):
            length = math.sqrt(math.pow(station['StationPosition']['PositionLon']-positionLon,2) + math.pow(station['StationPosition']['PositionLat']-positionLat,2))
            stationPosition = station['StationName']['Zh_tw']
    print(stationPosition)
    
    
