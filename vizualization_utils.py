import pandas as pd
import matplotlib.pyplot as plt


def vizualize_synth(
        result: pd.DataFrame,
        region: str,
        variable: str,
        year: int):
    with plt.style.context('dark_background'):
        plt.figure(figsize=(20, 9))
        plt.plot(result['year'], result['Observed'], label='Observed')
        plt.plot(result['year'], result['Synthetic'], label='Synthetic')
        plt.vlines(x=year, ymin=0,
                   ymax=result.Observed.max() * 1.02
                   if result.Observed.max() > result.Synthetic.max()
                   else result.Synthetic.max()*1.02,
                   linestyle='dashed', label='SEZ creation')
        plt.title(f"Synthetic Control Assessment for {region}", fontsize=20)
        plt.ylabel(variable, fontsize=17)
        plt.xlabel('Year', fontsize=17)
        plt.xticks(fontsize=15)
        plt.legend(loc='upper left', fontsize=15)


def vizualize_post_pre(variable_dict: dict, variable_name: str, colors: list):
    with plt.style.context('dark_background'):
        plt.figure(figsize=(20, 8))
        plt.bar(x=variable_dict['x'],
                height=variable_dict['height'], color=colors)
        plt.xticks(rotation=30, ha='right', fontsize=19)

        legend_elements = [plt.Line2D([0], [0], marker='o',
                                      color='w', label='Treated units',
                                      markerfacecolor='cyan', markersize=15),
                           plt.Line2D([0], [0], marker='o', color='w',
                                      label='Placebo units',
                                      markerfacecolor='green', markersize=15),
                           ]

        plt.title(f'MAE Post/Pre relation for {variable_name}', fontsize=23)
        plt.legend(handles=legend_elements, loc='upper right', fontsize=19)
