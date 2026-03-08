import pandas as pd

def get_tyre_degradation(session) -> dict:
    laps = session.laps.pick_quicklaps()
    compounds = ['SOFT', 'MEDIUM', 'HARD', 'INTERMEDIATE', 'WET']
    deg_data = {}

    for compound in compounds:
        compound_laps = laps[laps['Compound'] == compound].copy()
        if len(compound_laps) < 5:
            continue

        compound_laps = compound_laps[['TyreLife', 'LapTime']].dropna()
        compound_laps['LapTimeMs'] = compound_laps['LapTime'].apply(
            lambda x: int(x.total_seconds() * 1000) if pd.notna(x) else None
        )
        compound_laps = compound_laps.dropna(subset=['LapTimeMs'])
        grouped = compound_laps.groupby('TyreLife')['LapTimeMs'].median()

        deg_data[compound] = {
            'tyreAges': [int(age) for age in grouped.index.tolist()],
            'lapTimesMs': [int(t) for t in grouped.values.tolist()],
        }

    return {'compounds': deg_data}