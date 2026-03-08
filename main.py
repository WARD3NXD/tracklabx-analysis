import os
import fastf1
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from analysis.positions  import get_position_changes
from analysis.laptimes   import get_lap_comparison
from analysis.pitstops   import get_pit_strategy
from analysis.tyres      import get_tyre_degradation
from analysis.speed      import get_speed_trace
from analysis.telemetry  import get_fastest_lap_telemetry

# Local cache directory — always writable on Render free tier
CACHE_DIR = os.path.join(os.path.dirname(__file__), 'fastf1_cache')
os.makedirs(CACHE_DIR, exist_ok=True)
fastf1.Cache.enable_cache(CACHE_DIR)

app = FastAPI(title="TrackLabX Analysis API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://tracklabx.vercel.app",
        "http://localhost:3000"
    ],
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/analysis/{year}/{round_number}")
async def get_race_analysis(year: int, round_number: int):
    try:
        session = fastf1.get_session(year, round_number, 'R')
        session.load(
            laps=True,
            telemetry=True,
            weather=True,
            messages=False
        )
        return {
            "year":        year,
            "round":       round_number,
            "raceName":    session.event['EventName'],
            "circuit":     session.event['Location'],
            "date":        str(session.event['EventDate']),
            "positions":   get_position_changes(session),
            "lapTimes":    get_lap_comparison(session),
            "pitStrategy": get_pit_strategy(session),
            "tyreDeg":     get_tyre_degradation(session),
            "speedTrace":  get_speed_trace(session),
            "telemetry":   get_fastest_lap_telemetry(session),
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )