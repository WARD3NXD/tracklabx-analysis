import pandas as pd

def get_pit_strategy(session) -> dict:
    laps = session.laps
    results = session.results.head(10)
    top10 = results['Abbreviation'].tolist()

    drivers_strategy = {}

    for driver in top10:
        driver_laps = laps.pick_drivers(driver).sort_values('LapNumber')
        if len(driver_laps) == 0:
            continue

        stints = []
        current_compound = None
        stint_start = None

        for _, lap in driver_laps.iterrows():
            if pd.isna(lap['LapNumber']):
                continue
            compound = str(lap['Compound']) if pd.notna(lap.get('Compound')) else None
            lap_num = int(lap['LapNumber'])

            if compound != current_compound:
                if current_compound is not None and stint_start is not None:
                    stints.append({
                        'compound': current_compound,
                        'startLap': stint_start,
                        'endLap':   lap_num - 1,
                        'lapCount': lap_num - stint_start,
                    })
                current_compound = compound
                stint_start = lap_num

        if current_compound and stint_start:
            max_lap = driver_laps['LapNumber'].dropna().max()
            if pd.notna(max_lap):
                stints.append({
                    'compound': current_compound,
                    'startLap': stint_start,
                    'endLap':   int(max_lap),
                    'lapCount': int(max_lap) - stint_start + 1,
                })

        finish_pos = 20
        driver_result = results[results['Abbreviation'] == driver]
        if len(driver_result) > 0 and pd.notna(driver_result['Position'].iloc[0]):
            finish_pos = int(driver_result['Position'].iloc[0])

        drivers_strategy[driver] = {
            'team':   driver_laps['Team'].iloc[0],
            'stints': stints,
            'finish': finish_pos,
        }

    total_laps = laps['LapNumber'].dropna().max()

    return {
        'drivers':   top10,
        'totalLaps': int(total_laps) if pd.notna(total_laps) else 0,
        'strategy':  drivers_strategy,
    }