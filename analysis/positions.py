import pandas as pd

def get_position_changes(session) -> dict:
    laps = session.laps[['DriverNumber', 'Driver', 'LapNumber', 'Position', 'Team']].dropna()
    drivers = laps['Driver'].unique().tolist()
    lap_numbers = sorted(laps['LapNumber'].unique().tolist())

    series = {}
    for driver in drivers:
        driver_laps = laps[laps['Driver'] == driver].sort_values('LapNumber')
        series[driver] = {
            'team': driver_laps['Team'].iloc[0] if len(driver_laps) > 0 else '',
            'positions': [
                [int(row['LapNumber']), int(row['Position'])]
                for _, row in driver_laps.iterrows()
                if pd.notna(row['LapNumber']) and pd.notna(row['Position'])
            ]
        }

    return {
        'lapNumbers': [int(l) for l in lap_numbers],
        'drivers':    drivers,
        'series':     series,
    }