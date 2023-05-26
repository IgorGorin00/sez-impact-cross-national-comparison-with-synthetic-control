import SparseSC
import pandas as pd


def calculate_synths(current_region_name: str, current_year: int, LIST_OF_REGIONS_WITH_SEZS: list, DATAFRAMES: dict):
    
    for rname in LIST_OF_REGIONS_WITH_SEZS:
        if rname != current_region_name:
            idx_to_drop = [val for val in list(DATAFRAMES.values())[0].index.values if val == rname]
    
    synths = {}
    for df_name, df in DATAFRAMES.items():
        print(f'\t\t Calculating for {df_name}')
        synth = SparseSC.fit(
            features=df.drop(idx_to_drop, axis=0).iloc[:,df.columns <= current_year].values,
            targets=df.drop(idx_to_drop).iloc[:,df.columns > current_year].values,
            treated_units=[idx for idx, val in enumerate(df.drop(idx_to_drop).index.values) if val == current_region_name],
            progress=0, print_path=False
        )
        treated_units=[idx for idx, val in enumerate(df.drop(idx_to_drop).index.values) if val == current_region_name]
        result = df.loc[df.index == current_region_name].T.reset_index(drop=False)
        result.columns = ["year", "Observed"]
        result['Synthetic'] = synth.predict(df.drop(idx_to_drop, axis=0).values)[treated_units,:][0]
        synths[df_name] = {'synth': synth, 'res_df': result}
    synths['treatment_year'] = current_year
    return synths



def calculate_synths_for_placebo(current_region_name: str, current_year: int, LIST_OF_REGIONS_WITH_SEZS: list, DATAFRAMES: dict):    
    '''
    basically the same as calculate_synth(), 
    but we drop all the regions, and fit() replaced with fit_fast() 
    so we will spend less time and 
    the estimations does not have to be all that accurate
    '''
    for rname in LIST_OF_REGIONS_WITH_SEZS:
        idx_to_drop = [val for val in list(DATAFRAMES.values())[0].index.values if val == rname]
    
    synths = {}
    for df_name, df in DATAFRAMES.items():
        try:
            synth = SparseSC.fit_fast(
                features=df.drop(idx_to_drop, axis=0).iloc[:,df.columns <= current_year].values,
                targets=df.drop(idx_to_drop).iloc[:,df.columns > current_year].values,
                treated_units=[idx for idx, val in enumerate(df.drop(idx_to_drop).index.values) if val == current_region_name],
                progress=0, print_path=False
            )
            treated_units=[idx for idx, val in enumerate(df.index.values) if val == current_region_name]
            result = df.loc[df.index == current_region_name].T.reset_index(drop=False)
            result.columns = ["year", "Observed"]
            result['Synthetic'] = synth.predict(df.drop(idx_to_drop, axis=0).values)[treated_units,:][0]
            synths[df_name] = {'synth': synth, 'res_df': result}
        
        # LinAlgError: Matrix is singular raises for fixed_assets so i just dont calculate for it 
        except Exception as e: 
            print(f"{e} occurred for {df_name}")
    synths['treatment_year'] = current_year
    return synths