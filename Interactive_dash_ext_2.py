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
spacex_df['Outcome'] = spacex_df['class'].map({1: 'Success', 0: 'Fail'})

# Function to assign color to launch outcome
def assign_marker_color(launch_outcome):
    if launch_outcome == 1:
        return 'green'
    else:
        return 'red'
    
spacex_df['marker_color'] = spacex_df['class'].apply(assign_marker_color)

colors_outcome = {
    'Success': 'green',
    'Fail': 'red'
}

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

Booster_Version = (
    spacex_df
    .groupby('Booster Version Category')['class']
    .agg(['count', 'mean'])
    .reset_index()
)

Booster_Version['success_rate'] = Booster_Version['mean'] * 100


# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                html.Br(),
                                        dcc.Dropdown(id='site-dropdown',
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
                                        ),
                                html.Br(),
                                
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site success-pie-chart
                                html.Div([
                                        html.Div(dcc.Graph(id='success-booster-bar-chart')),
                                        html.Div(dcc.Graph(id='success-pie-chart'))], 
                                        style={'display': 'flex'}),
                                
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                        min=min_payload, max=max_payload, step=1000,
                                        marks={int(min_payload): str(int(min_payload)), int(max_payload):str(int(max_payload))},
                                        value=[min_payload, max_payload]),
                                
                                html.Br(),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))

                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='payload-slider', component_property='value'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(payload_range, entered_site):
    low, high = payload_range
    filtered_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)]

    if entered_site == 'ALL':
        allsites = filtered_df.groupby('Launch Site')['class'].count().reset_index()
        fig = px.pie(allsites, values='class', title="Total Success Launchs by Site", names='Launch Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        site_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        site_counts = site_df.groupby('Outcome').size().reset_index(name='counts')
        fig = px.pie(site_counts,
                values='counts',
                names='Outcome',
                title=f"Success vs Failure for {entered_site}",
                color='Outcome',
                color_discrete_map=colors_outcome)
        return fig

# TASK 5:
# Add a Add a bar chart to show the correlation between booster version and launch Sites
@app.callback(Output(component_id='success-booster-bar-chart', component_property='figure'),
               Input(component_id='payload-slider', component_property='value'),
               Input(component_id='site-dropdown', component_property='value'))

def get_bar_chart(payload_range, entered_site):
    low, high = payload_range
    filtered3_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)]

    if entered_site == 'ALL':
        allsites3 = filtered3_df.groupby('Booster Version Category')['class'].agg(['count', 'mean']).reset_index()
        allsites3['success_rate'] = allsites3['mean'] * 100
        fig = px.bar(allsites3, x='Booster Version Category', y='success_rate', title="Total Success Launchs by Booster Version Category")
    else:
        # return the outcomes bar for a selected site
        site3_df = filtered3_df[filtered3_df['Launch Site'] == entered_site]
        site4_df = site3_df.groupby('Booster Version Category')['class'].agg(['count', 'mean']).reset_index()
        site4_df['success_rate'] = site4_df['mean'] * 100
        fig = px.bar(site4_df, x='Booster Version Category', y='success_rate', 
                     title=f"Total Success Launchs by Booster Version Category for {entered_site}")
        
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    Input(component_id='payload-slider', component_property='value'),
    Input(component_id='site-dropdown', component_property='value'))

def get_scatter_chart(payload_range, entered_site):
#    print(payload_range, entered_site)
    low, high = payload_range
    filtered2_df = spacex_df[
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)]

    if entered_site == 'ALL':
        fig = px.scatter(
            filtered2_df,
            x="Payload Mass (kg)",
            y="Outcome",
            color="Launch Site",
#            size="Payload Mass (kg)",
            title="Success Rate vs Payload Mass (kg)" )
    else:
        site2_df = filtered2_df[filtered2_df['Launch Site'] == entered_site]
        fig = px.scatter(
            site2_df,
            x="Payload Mass (kg)",
            y="Outcome",
            color='Outcome',
#            size="Payload Mass (kg)",
            title=f"Success Rate vs Payload Mass (kg) for {entered_site}", 
            color_discrete_map=colors_outcome)

    return fig


# Run the app
if __name__ == '__main__':
    app.run()
