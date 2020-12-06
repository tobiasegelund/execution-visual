import numpy as np

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
        df_local['Executions Scaled'] = np.log(df_local["Executions"]+1)
        # df_local = df_local[df_local['Year']==input_time]

    return df_local





