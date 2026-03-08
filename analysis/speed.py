def get_speed_trace(session) -> dict:
    fastest = session.laps.pick_fastest()
    if fastest is None:
        return {}

    try:
        tel = fastest.get_car_data().add_distance()
        driver = fastest['Driver']
        team = fastest['Team']

        return {
            'driver': driver,
            'team': team,
            'lapTime': int(fastest['LapTime'].total_seconds() * 1000),
            'trace': {
                'distance': [round(float(d), 1) for d in tel['Distance'].tolist()],
                'speed': [round(float(s), 1) for s in tel['Speed'].tolist()],
                'throttle': [round(float(t), 1) for t in tel['Throttle'].tolist()],
                'brake': [int(b) for b in tel['Brake'].tolist()],
            }
        }
    except Exception:
        return {}