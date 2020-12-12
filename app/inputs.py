import pandas as pd
import base64

encoded_image = base64.b64encode(open("./icons/fast-forward-double-right-arrows-symbol.png", 'rb').read())
github_image = base64.b64encode(open("./icons/github.png", 'rb').read())

df = pd.read_csv('./data/executions.csv')
df_map = pd.read_csv('./data/map_data.csv')
df_map_timeline = pd.read_csv('./data/timeline_map_data.csv')
df_executions_sunburst = pd.read_csv('./data/executions_data_sunburst.csv')
df_victims_sunburst = pd.read_csv('./data/victims_sunburst.csv')
state_stats = pd.read_csv('./data/state_stats.csv')
race_pop_data = pd.read_csv('./data/race_pop_data.csv')
race_victim_pop_data = pd.read_csv('./data/race_victim_pop_data.csv')

available_region = df['Region'].unique()
available_states = df['State'].unique()
available_regions_page3 = ['West', 'South', 'Midwest', 'Northeast']
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


available_regions_states = {
    'West': ['Utah', 'Nevada', 'Wyoming', 'Arizona', 'California', 'Washington', 'Idaho', 'Montana', 'Oregon', 'Colorado', 'New Mexico', 'Hawaii', 'Alaska', ],
    'South': ['Florida', 'Virginia', 'Texas', 'Alabama', 'Mississippi',
       'Louisiana', 'Georgia', 'North Carolina', 'South Carolina',
       'Arkansas', 'Oklahoma', 'Delaware', 'Maryland', 'Kentucky',
       'Tennessee', 'West Virginia'],
    'Midwest': ['Indiana', 'Missouri', 'Illinois', 'Nebraska', 'Ohio',
       'South Dakota', 'Iowa', 'Minnesota', 'Kansas', 'North Dakota', 'Michigan', 'Wisconsin'],
    'Northeast': ['Pennsylvania', 'Connecticut', 'Maine', 'New Hampshire', 'Vermont', 'Massachusetts', 'Rhode Island', 'New York', 'New Jersey'],
    'Federal': ['Federal']
}

available_regions_states_page3 = {
    'West': ['Utah', 'Nevada', 'Wyoming', 'Arizona', 'California', 'Washington', 'Idaho', 'Montana', 'Oregon', 'Colorado', 'New Mexico', 'Hawaii', 'Alaska', ],
    'South': ['Florida', 'Virginia', 'Texas', 'Alabama', 'Mississippi',
       'Louisiana', 'Georgia', 'North Carolina', 'South Carolina',
       'Arkansas', 'Oklahoma', 'Delaware', 'Maryland', 'Kentucky',
       'Tennessee', 'West Virginia'],
    'Midwest': ['Indiana', 'Missouri', 'Illinois', 'Nebraska', 'Ohio',
       'South Dakota', 'Iowa', 'Minnesota', 'Kansas', 'North Dakota', 'Michigan', 'Wisconsin'],
    'Northeast': ['Pennsylvania', 'Connecticut', 'Maine', 'New Hampshire', 'Vermont', 'Massachusetts', 'Rhode Island', 'New York', 'New Jersey'],
}
