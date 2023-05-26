import json
import pandas as pd
import numpy as np
import SparseSC
from sklearn.metrics import mean_absolute_error as MAE


def calculate_post_pre_mae_relations(synths_for_placebo, synths_for_each_region, sezs_region_and_year):
    _ = list(synths_for_placebo.keys())[0]
    for variable in synths_for_placebo[_].keys():
        # calcualte MAE and write it to the main results dict
        if variable != 'treatment_year':
            for rname in synths_for_each_region.keys():
                df = synths_for_each_region[rname][variable]['res_df']
                treatment_year = synths_for_each_region[rname]['treatment_year']
                mae_pre = MAE(
                    df[df['year'] <= treatment_year]['Observed'].values, 
                    df[df['year'] <= treatment_year]['Synthetic'].values
                )
                mae_post = MAE(
                    df[df['year'] > treatment_year]['Observed'].values, 
                    df[df['year'] > treatment_year]['Synthetic'].values
                )
                rel = mae_post / mae_pre
                synths_for_each_region[rname][variable]['mae_pre'] = mae_pre
                synths_for_each_region[rname][variable]['mae_post'] = mae_post
                synths_for_each_region[rname][variable]['rel'] = rel

            for rname in synths_for_placebo.keys():
                df = synths_for_placebo[rname][variable]['res_df']
                treatment_year = synths_for_placebo[rname]['treatment_year']
                mae_pre = MAE(
                    df[df['year'] <= treatment_year]['Observed'].values, 
                    df[df['year'] <= treatment_year]['Synthetic'].values
                )
                mae_post = MAE(
                    df[df['year'] > treatment_year]['Observed'].values, 
                    df[df['year'] > treatment_year]['Synthetic'].values
                )
                rel = mae_post / mae_pre
                synths_for_placebo[rname][variable]['mae_pre'] = mae_pre
                synths_for_placebo[rname][variable]['mae_post'] = mae_post
                synths_for_placebo[rname][variable]['rel'] = rel
    # and also write it to the separarte dict (for vizualization purposes)        
    post_pre_relations = {}
    for variable in synths_for_placebo[_].keys():
        if variable != 'treatment_year':
            x = []
            heigth = []
            for rname in synths_for_each_region.keys():
                x.append(rname)
                heigth.append(synths_for_each_region[rname][variable]['rel'])
            for rname in synths_for_placebo.keys():
                heigth.append(synths_for_placebo[rname][variable]['rel'])
                x.append(rname)
            post_pre_relations[variable] = {'x': x, 'height': heigth}
    return post_pre_relations


def try_calculate_p_values(filename: str, sezs_region_and_year: list | tuple, synths_for_each_region: dict, DATAFRAMES: dict):
    with open(f"./results/{filename}", 'w') as f:

        for rname, year in sezs_region_and_year:
            print(f'Calculating for {rname, year}')
            f.write(rname)
            f.write('\n')
            for variable in synths_for_each_region[rname].keys():
                if variable != 'treatment_year':
                    f.write(variable)
                    f.write('\n')
                    # if variable == 'grp':
                    #     colnames = np.arange(1990, 2022)
                    # else:
                    #     colnames = np.arange(1990, 2020)
                    df = DATAFRAMES[variable]
                    # df = pd.DataFrame(np.hstack((
                    #     synths_for_each_region[rname][variable]['synth'].features, 
                    #     synths_for_each_region[rname][variable]['synth'].targets)), columns=colnames)
                    ## Creating unit treatment_periods
                    unit_treatment_periods = np.full((df.values.shape[0]), np.nan)
                    unit_treatment_periods[synths_for_each_region[rname][variable]['synth'].treated_units] =\
                    [idx for idx, colname in enumerate(df.columns) if colname > year][0]

                    try:
                        ## fitting estimate effects method
                        sc = SparseSC.estimate_effects(
                            outcomes = df.values,  
                            unit_treatment_periods = unit_treatment_periods, 
                            max_n_pl=50, # Number of placebos
                            level=0.9 # Level for confidence intervals
                        )
                        f.write(str(sc))
                        f.write('\n\n')
                        f.write(f"Estimated effect of SEZ is {np.round(sc.pl_res_post.effect_vec.effect[-1])}, \
                                with a p-value of  {np.round(sc.pl_res_post.effect_vec.p[-1],2)}")            
                        f.write('\n\n')
                    except Exception as e:
                        print(f"{e} occured for {rname}, {variable}")
                        f.write(f"{e} occured for {rname}, {variable}")
                        f.write('\n\n')


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
