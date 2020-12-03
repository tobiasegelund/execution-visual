import pandas as pd

df = pd.read_csv('./data/executions.csv')

available_region = df['Region'].unique()
available_states = df['State'].unique()
available_countys = df['County'].unique()
available_victim_types = [
    'Number of Victims',
    'Number of White Male Victims',
    'Number of Black Male Victims',
    'Number of Latino Male Victims',
    'Number of Asian Male Victims ',
    'Number of Native American Male Victims',
    'Number of Other Race Male Victims',
    'Number of White Female Victims',
    'Number of Black Female Victims',
    'Number of Latino Female Victims',
    'Number of Asian Female Victims',
    'Number of Native American Female Victims',
    'Number of Other Race Female Victims'
]
available_years = [
    year for year in range(df['Year'].min(), df['Year'].max()+1)
]
