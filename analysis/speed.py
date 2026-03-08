import pandas as pd

def get_speed_trace(session) -> dict:
    try:
        fastest = session.laps.pick_fastest()
        if fastest is None:
            return {}

        tel = fastest.get_car_data().add_distance()
        tel = tel.dropna(subset=['Distance', 'Speed'])

        return {
            'driver':   str(fastest['Driver']),
            'team':     str(fastest['Team']),
            'lapTime':  int(fastest['LapTime'].total_seconds() * 1000)
                        if pd.notna(fastest['LapTime']) else 0,
            'trace': {
                'distance': [round(float(d), 1) for d in tel['Distance'].tolist()],
                'speed':    [round(float(s), 1) for s in tel['Speed'].tolist()],
                'throttle': [round(float(t), 1) if pd.notna(t) else 0.0
                             for t in tel['Throttle'].tolist()],
                'brake':    [int(b) if pd.notna(b) else 0
                             for b in tel['Brake'].tolist()],
            }
        }
    except Exception:
        return {}