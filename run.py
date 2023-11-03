# ref: https://erikbern.com/2016/04/04/nyc-subway-math.html
# comments

from proto import gtfs_realtime_pb2
import urllib.request
import time
import traceback
from protobuf_to_dict import protobuf_to_dict
import json

start_time = time.time()

while True:
    try:

        feed = gtfs_realtime_pb2.FeedMessage()
        response = urllib.request.urlopen('http://gtfs.ovapi.nl/new/vehiclePositions.pb')
        vehicles_position = response.read()

        with open('vehicles_position.bin', mode='wb') as file_trains:
            file_trains.write(vehicles_position)

        data = open('vehicles_position.bin', 'rb').read()
        feed.ParseFromString(data)

    except:
        traceback.print_exc()
        continue

    vehicles = [protobuf_to_dict(entity.vehicle) for entity in feed.entity if entity.HasField('vehicle')]
    print('got', len(vehicles), 'vehicles')

    f = open('log.jsons', 'a')
    json.dump(vehicles, f)
    f.write('\n')
    f.close()

    # wait a minute before getting the new data
    time.sleep(60.0 - ((time.time() - start_time) % 60.0))