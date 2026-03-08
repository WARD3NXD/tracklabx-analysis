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
            compound = lap['Compound'] if hasattr(lap, 'Compound') else None
            lap_num = int(lap['LapNumber'])

            if compound != current_compound:
                if current_compound is not None:
                    stints.append({
                        'compound': current_compound,
                        'startLap': stint_start,
                        'endLap': lap_num - 1,
                        'lapCount': lap_num - stint_start,
                    })
                current_compound = compound
                stint_start = lap_num

        if current_compound and stint_start:
            stints.append({
                'compound': current_compound,
                'startLap': stint_start,
                'endLap': int(driver_laps['LapNumber'].max()),
                'lapCount': int(driver_laps['LapNumber'].max()) - stint_start + 1,
            })

        drivers_strategy[driver] = {
            'team': driver_laps['Team'].iloc[0],
            'stints': stints,
            'finish': int(results[results['Abbreviation'] == driver]['Position'].iloc[0])
                      if len(results[results['Abbreviation'] == driver]) > 0 else 20,
        }

    return {
        'drivers': top10,
        'totalLaps': int(laps['LapNumber'].max()),
        'strategy': drivers_strategy,
    }