import pandas as pd
import base64

encoded_image = base64.b64encode(open("./icons/right-arrow.png", 'rb').read())
encoded_image2 = base64.b64encode(open("./icons/down-arrow.png", 'rb').read())

df = pd.read_csv('./data/executions.csv')
df_map = pd.read_csv('./data/map_data.csv')
df_map_timeline = pd.read_csv('./data/timeline_map_data.csv')

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


available_regions_states = {
    'West': ['Utah', 'Nevada', 'Wyoming', 'Arizona', 'California', 'Washington', 'Idaho', 'Montana', 'Oregon', 'Colorado', 'New Mexico'],
    'South': ['Florida', 'Virginia', 'Texas', 'Alabama', 'Mississippi',
       'Louisiana', 'Georgia', 'North Carolina', 'South Carolina',
       'Arkansas', 'Oklahoma', 'Delaware', 'Maryland', 'Kentucky',
       'Tennessee'],
    'Midwest': ['Indiana', 'Missouri', 'Illinois', 'Nebraska', 'Ohio',
       'South Dakota'],
    'Northeast': ['Pennsylvania', 'Connecticut'],
    'Federal': ['Federal']
}
