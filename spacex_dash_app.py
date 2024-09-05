# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
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
                                 dcc.Dropdown(id='site-dropdown',
                                              options=[
                                                  {'label': 'All Sites', 'value': 'ALL'},
                                                  {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                  {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                  {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                  {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                              ],
                                              value='ALL',
                                              placeholder="Select a Launch Site",
                                              searchable=True
                                              ),
                                 html.Div(dcc.Graph(id='success-pie-chart')),
                                 html.Br(),

                                 html.P("Payload range (Kg):"),
                                  # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={0: '0',
                                        100: '100'},
                                    value=[min_payload, max_payload]),
                                 html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])
def get_scatter_plot(entered_site, payload_range):
    # Filter dataframe by payload range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= payload_range[0]) & 
                            (spacex_df['Payload Mass (kg)'] <= payload_range[1])]
    
    # Check if all sites or a specific site
    if entered_site == 'ALL':
        # Create scatter plot for all sites
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title='Correlation between Payload and Success for All Sites')
    else:
        # Filter dataframe for the selected site
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        # Create scatter plot for the selected site
        fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                         color='Booster Version Category',
                         title=f'Correlation between Payload and Success for site {entered_site}')

    return fig

# Callback function for pie chart
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, 
                     values='class',  # Correct column for pie chart values
                     names='Launch Site',  # Correct column for pie chart labels
                     title='Total Successful Launches by Site')
    else:
        # Filter the dataframe for the selected site
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, 
                     names='class', 
                     title=f'Total Success Launches for site {entered_site}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
