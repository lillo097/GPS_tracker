import json
import time

with open('/Users/liviobasile/Documents/Machine Learning/gitRepos/GPS_tracker/lib/gps_data_2secs.json', encoding='utf8') as f:
    for row in f:
        data = json.loads(row)
        latitiude = float(data['latitude'])
        longitude = float(data['longitude'])
        altitude = float(data['altitude'])
        speed = float(data['speed'])



