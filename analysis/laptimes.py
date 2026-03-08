import pandas as pd

def get_lap_comparison(session) -> dict:
    laps = session.laps.pick_quicklaps()
    results = session.results.head(10)
    top10 = results['Abbreviation'].tolist()

    series = {}
    for driver in top10:
        driver_laps = laps.pick_drivers(driver).sort_values('LapNumber')
        if len(driver_laps) == 0:
            continue

        team = driver_laps['Team'].iloc[0]
        lap_data = []

        for _, lap in driver_laps.iterrows():
            try:
                if pd.notna(lap['LapTime']) and pd.notna(lap['LapNumber']):
                    lap_data.append({
                        'lap':      int(lap['LapNumber']),
                        'timeMs':   int(lap['LapTime'].total_seconds() * 1000),
                        'compound': str(lap['Compound']) if pd.notna(lap['Compound']) else 'UNKNOWN',
                    })
            except (ValueError, TypeError):
                continue

        series[driver] = {
            'team': team,
            'laps': lap_data,
        }

    return {
        'drivers': top10,
        'series':  series,
    }