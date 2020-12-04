def filter_data(
    df,
    input_race=None,
    input_region=None,
    input_sex=None,
    input_state=None):

    # Filter on race
    if input_race == 'All' or input_race is None:
        df = df
    elif input_race == 'White':
        df = df[df['Race']=='White']
    else:
        df = df[df['Race']!='White']

    # Filter on sex
    if input_sex == 'Both' or input_sex is None:
        df = df
    else:
        df = df[df['Sex']==input_sex]

    # Filter on region
    if input_region is None:
        df = df
    else:
        df = df[df['Region']==input_region]

    # Filter on state
    if input_state is None:
        df = df
    else:
        df = df[df['State']==input_state]


    return df
