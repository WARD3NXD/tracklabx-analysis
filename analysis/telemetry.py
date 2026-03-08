import pandas as pd

def get_fastest_lap_telemetry(session) -> dict:
    try:
        fastest = session.laps.pick_fastest()
        if fastest is None:
            return {}

        tel = fastest.get_car_data().add_distance()
        tel = tel.dropna(subset=['Distance', 'Speed'])
        sampled = tel.iloc[::5]

        return {
            'driver':   str(fastest['Driver']),
            'team':     str(fastest['Team']),
            'lapTime':  int(fastest['LapTime'].total_seconds() * 1000)
                        if pd.notna(fastest['LapTime']) else 0,
            'telemetry': {
                'distance': [round(float(d), 1) for d in sampled['Distance'].tolist()],
                'speed':    [round(float(s), 1) for s in sampled['Speed'].tolist()],
                'throttle': [round(float(t), 1) if pd.notna(t) else 0.0
                             for t in sampled['Throttle'].tolist()],
                'brake':    [int(b) if pd.notna(b) else 0
                             for b in sampled['Brake'].tolist()],
                'gear':     [int(g) if pd.notna(g) else 0
                             for g in sampled['nGear'].tolist()],
                'rpm':      [int(r) if pd.notna(r) else 0
                             for r in sampled['RPM'].tolist()],
            }
        }
    except Exception:
        return {}