import numpy as np
import pandas as pd

def filter_data(
    df,
    input_race=None,
    input_region=None,
    input_sex=None,
    input_state=None,
    input_time=None):

    # Filter on race -> Looks at len instead of correct syntax since the syntax depends on what the user clicks on first
    if input_race is None or input_race == [] or len(input_race) == 2:
        df_local = df
    elif input_race == ['White']:
        df_local = df[df['Race']=='White']
    else:
        df_local = df[df['Race']!='White']

    # Filter on sex
    if input_sex is None or input_sex == []:
        df_local = df_local
    else:
        df_local = df_local[df_local['Sex'].isin(input_sex)]

    # Filter on region
    if input_region is None or input_region == []:
        df_local = df_local
    else:
        df_local = df_local[df_local['Region'].isin(input_region)]

    # Filter on state
    if input_state is None or input_state == []:
        df_local = df_local
    else:
        df_local = df_local[df_local['State'].isin(input_state)]


    if input_time is None:
        df_local = df_local
    else:
        range_years = [year for year in range(input_time[0], input_time[1]+1)]
        df_local = df_local[df_local['Year'].isin(range_years)]
        df_local = df_local.groupby(['State', 'State Code']).sum().reset_index()
        df_local['Executions scaled'] = np.log(df_local["Executions"]+1)
        # df_local = df_local[df_local['Year']==input_time]

    return df_local


def build_hierarchical_dataframe(df, levels, value_column):
    """
    Build a hierarchy of levels for Sunburst or Treemap charts.

    Levels are given starting from the bottom to the top of the hierarchy,
    ie the last level corresponds to the root.
    """
    df_all_trees = pd.DataFrame(columns=['id', 'parent', 'value'])
    for i, level in enumerate(levels):
        df_tree = pd.DataFrame(columns=['id', 'parent', 'value'])
        dfg = df.groupby(levels[i:]).sum()
        dfg = dfg.reset_index()
        df_tree['id'] = dfg[level].copy()
        if i < len(levels) - 1:
            df_tree['parent'] = dfg[levels[i+1]].copy()
        else:
            df_tree['parent'] = 'All'
        df_tree['value'] = dfg[value_column]
        df_all_trees = df_all_trees.append(df_tree, ignore_index=True)
    total = pd.Series(dict(id='All', parent='',
                              value=df[value_column].sum()
                          ))
    df_all_trees = df_all_trees.append(total, ignore_index=True)

    df_all_trees["color"] = [1 if df_all_trees.loc[i,"id"].startswith("White")
                            else 0.5 if df_all_trees.loc[i,"id"].startswith("All")
                            else 0 for i in range(len(df_all_trees))]

    df_all_trees = df_all_trees[df_all_trees["id"]!= df_all_trees["parent"]]

    return df_all_trees
