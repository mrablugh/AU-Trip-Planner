from fastapi import FastAPI, Response
from convert import fetch_transloc_vehicles, build_gtfs_rt

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "status": "online",
        "service": "AU Shuttle GTFS-RT Feed Generator",
        "feed_url": "/gtfs-rt.pb"
    }

@app.get("/gtfs-rt.pb")
def get_gtfs_rt_feed():
    vehicles = fetch_transloc_vehicles()
    binary_data = build_gtfs_rt(vehicles)
    return Response(content=binary_data, media_type="application/x-protobuf")