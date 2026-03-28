# Interactive Dasboard
#python3.11 -m pip install pandas dash
#wget "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
#python3.11 spacex-dash-app.py

# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                
                                html.Br(),
                                html.Br(dcc.Dropdown(id='site-dropdown',
                                            options=[
                                            {'label': 'All Sites', 'value': 'ALL'},
                                            {'label': 'Canaveral Launch Center', 'value': 'CCAFS LC-40'},
                                            {'label': 'Canaveral Space Launch Center', 'value': 'CCAFS SLC-40'},
                                            {'label': 'Keneddy Space Center', 'value': 'KSC LC-39A'},
                                            {'label': 'Vandenberg Space Center', 'value': 'VAFB SLC-4E'},
                                            ],
                                        value='ALL',
                                        placeholder="Select a Launch Site here",
                                        searchable=True
                                        ),),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                               
                                html.Br(),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        allsites = spacex_df.groupby('Launch Site')['class'].count().reset_index()
        fig = px.pie(allsites, values='class', title="Total Success Launchs by Site", names='Launch Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        site_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        count = site_df['class'].value_counts()
        px.pie(count, values = [count[1], count[0]], title=f"Total Success Launches for site: {entered_site}", names=['Success (1)', 'Fail (0)'])
        return fig
        

        
# Run the app
if __name__ == '__main__':
    app.run()
