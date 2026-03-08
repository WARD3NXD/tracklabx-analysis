from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import fastf1
import os

fastf1.Cache.enable_cache('/cache')

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

from analysis.positions  import get_position_changes
from analysis.laptimes   import get_lap_comparison
from analysis.pitstops   import get_pit_strategy
from analysis.tyres      import get_tyre_degradation
from analysis.speed      import get_speed_trace
from analysis.telemetry  import get_fastest_lap_telemetry

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
```

Then create the analysis folder with all 6 files from the previous prompt:
```
tracklabx-analysis/
  main.py
  requirements.txt
  analysis/
    __init__.py          ← empty file, needed for Python imports
    positions.py
    laptimes.py
    pitstops.py
    tyres.py
    speed.py
    telemetry.py