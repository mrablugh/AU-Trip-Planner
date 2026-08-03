from fastapi import FastAPI, Response
from convert import fetch_transloc_vehicles, build_gtfs_rt

app = FastAPI()

@app.get("/gtfs-rt.pb")
def get_gtfs_rt_feed():
    vehicles = fetch_transloc_vehicles()
    binary_data = build_gtfs_rt(vehicles)
    return Response(content=binary_data, media_type="application/x-protobuf")