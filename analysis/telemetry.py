def get_fastest_lap_telemetry(session) -> dict:
    fastest = session.laps.pick_fastest()
    if fastest is None:
        return {}

    try:
        tel = fastest.get_car_data().add_distance()
        driver = fastest['Driver']
        team = fastest['Team']

        sampled = tel.iloc[::5]

        return {
            'driver': driver,
            'team': team,
            'lapTime': int(fastest['LapTime'].total_seconds() * 1000),
            'telemetry': {
                'distance': [round(float(d), 1) for d in sampled['Distance'].tolist()],
                'speed': [round(float(s), 1) for s in sampled['Speed'].tolist()],
                'throttle': [round(float(t), 1) for t in sampled['Throttle'].tolist()],
                'brake': [int(b) for b in sampled['Brake'].tolist()],
                'gear': [int(g) for g in sampled['nGear'].tolist()],
                'rpm': [int(r) for r in sampled['RPM'].tolist()],
            }
        }
    except Exception:
        return {}