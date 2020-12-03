import pandas as pd

df = pd.read_csv('./data/executions.csv')

available_region = df['Region'].unique()
available_states = df['State'].unique()
# available_countys = df['County'].unique()
available_victim_types = [
    'Number of Victims',
    'Number of White Male Victims',
    'Number of Other Male Victims',
    'Number of White Female Victims',
    'Number of Other Female Victims',
]
available_years = [
    year for year in range(df['Year'].min(), df['Year'].max()+1)
]
