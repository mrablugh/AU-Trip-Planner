import os
import time
import requests
from google.transit import gtfs_realtime_pb2

TRANSLOC_API_KEY = os.getenv('TRANSLOC_API_KEY')
AGENCY_ID = os.getenv('AGENCY_ID')
VEHICLE_URL = f"https://transloc-api-1-2.p.rapidapi.com/vehicles.json?agencies={AGENCY_ID}"

HEADERS = {
    'X-RapidAPI-Key': TRANSLOC_API_KEY,
    'X-RapidAPI-Host': 'transloc-api-1-2.p.rapidapi.com'
}

def fetch_transloc_vehicles():
    response = requests.get(VEHICLE_URL, headers=HEADERS)
    response.raise_for_status()
    return response.json().get('data', {}).get(AGENCY_ID, [])

def build_gtfs_rt(transloc_vehicles):
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.header.gtfs_realtime_version = "2.0"
    feed.header.incrementality = gtfs_realtime_pb2.FeedHeader.FULL_DATASET
    feed.header.timestamp = int(time.time())

    for idx, tl_vehicle in enumerate(transloc_vehicles):
        entity = feed.entity.add()
        entity.id = str(tl_vehicle.get('vehicle_id', idx))
        
        vehicle_position = entity.vehicle
        vehicle_position.position.latitude = float(tl_vehicle['location']['lat'])
        vehicle_position.position.longitude = float(tl_vehicle['location']['lng'])
        vehicle_position.position.bearing = float(tl_vehicle.get('heading', 0))
        vehicle_position.position.speed = float(tl_vehicle.get('speed', 0))
        
        vehicle_position.vehicle.id = str(tl_vehicle.get('call_name', entity.id))
        vehicle_position.trip.route_id = str(tl_vehicle.get('route_id', ''))

    return feed.SerializeToString()

if __name__ == "__main__":
    vehicles = fetch_transloc_vehicles()
    gtfs_rt_binary = build_gtfs_rt(vehicles)
    
    # Save output to a directory that will be published
    os.makedirs('public', exist_ok=True)
    with open('public/au_shuttle.pb', 'wb') as f:
        f.write(gtfs_rt_binary)