import dash
from dash import dcc, html, Output, Input
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# Load the dataset from the csv file
csv_file_path = './World Energy Consumption.csv'
energy_df = pd.read_csv(csv_file_path)

# extract only the years and countries that there is data for
regions = ['Non-OECD (EI)', 'World', 'Upper-middle-income-countries', 'High-income-countries', 'European Union (27)', 'OECD (EI)', 'High-income countries', 'North America', 'North America (EI)', 'Asia', 'Asia Pacific (EI)', 'Upper-middle-income countries', 'CIS (EI)', 'Eastern Africa (EI)', 'Europe (EI)', 'Europe', 'South America', 'South and Central America (EI)', 'Lower-middle-income countries', 'Africa', 'Africa (EI)', 'Middle East (EI)', 'Central America (EI)']
years_df = energy_df[energy_df['biofuel_consumption'].notnull() & energy_df['fossil_fuel_consumption'].notnull() & energy_df['coal_consumption'].notnull() & energy_df['gas_consumption'].notnull() & energy_df['hydro_consumption'].notnull() & energy_df['nuclear_consumption'].notnull() & energy_df['oil_consumption'].notnull() & energy_df['other_renewable_consumption'].notnull() & energy_df['solar_consumption'].notnull()]
all_groups = years_df['country'].unique()
countries = [item for item in all_groups if item not in regions]

# not countries list:
groups = [regions, countries]    

energy_categories = []
for col in energy_df.columns:
    if "consumption" in col:
        energy_categories.append(col)

#find maximum energy consumption for slider
max_consumption = 0

min_year = years_df['year'].min()
max_year = years_df['year'].max()

other_options = ['gdp', 'population', 'energy_per_capita', 'energy_per_gdp']

dropdown1=html.Div(className="child1_1_1",children=[dcc.Dropdown(id='energy_type',options=energy_categories, value=energy_categories[0])], style=dict(width="100%"))
slider1=html.Div(className="child1_1_2",children=[html.Label('Select Energy Consumption Range (Terawatt Hours)', style={'font-weight': 'bold'}),dcc.RangeSlider(id='consumption_range',min=0,max=max_consumption,value=[0, max_consumption],marks={str(num): str(num/1000) for num in range(0, max_consumption + 1, 2500)}, step=500)], style=dict(width="100%"))
dropdown2=html.Div(className="child3_1_1",children=[dcc.Dropdown(id='country_selection',options=all_groups, value=all_groups[0])], style=dict(width="100%"))
slider2=html.Div(className="child1_1_3",children=[html.Label('Select Year Range', style={'font-weight': 'bold'}), dcc.RangeSlider(id='year_range',min=min_year,max=max_year,value=[min_year, max_year],marks={str(num): str(num) for num in range(0, max_year + 1, 5)}, step=1)], style=dict(width="100%"))
slider3=html.Div(className="child1_2_1",children=[html.Label('Select Year', style={'font-weight': 'bold'}), dcc.Slider(id='years',min=min_year,max=max_year,value=max_year,marks={str(num): str(num) for num in range(0, max_year + 1, 5)}, step=1)], style=dict(width="100%"))
checklist1=html.Div(className="child1_1_4",children=[html.Label('Select Type', style={'font-weight': 'bold'}), dcc.Checklist(id='group_type',options=['regions','countries'],value=['regions'])],style=dict(width=150))
checklist2=html.Div(className="child3_1_2",children=[html.Label('Select Type', style={'font-weight': 'bold'}), dcc.Checklist(id='group_type2',options=['regions','countries'],value=['regions'])],style=dict(width=150))
radio1=html.Div(className="child3_1_2",children=[html.Label('Select Option', style={'font-weight': 'bold'}), dcc.RadioItems(id='radio1',options=other_options,value=other_options[0])],style=dict(width=150))

#radio1=html.Div(className="child2_1_1",children=[dcc.RadioItems(id='radio', options=[], value="", inline=True)])

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div(className="parent", children=[
    html.H2("Energy Consumption by Year, Countries/Regions, Per Individual Energy Type", className="grouped-children-title"),
    html.Div(className='child-group1', children=[
        html.Div(className="child1",children=[html.Div([dropdown1,slider1,slider2,checklist1], className="child1_1"),html.Div(dcc.Graph(id='graph1'), className="child1_2")]),
        html.Div(className="child2",children=[html.Div([slider3], className="child2_1"),html.Div(dcc.Graph(id='graph2'), className="child2_2")])]
    ),
    html.H2("Energy Consumption by Year, Energy Types, Per Individual Country/Region", className="grouped-children-title2"),
    html.Div(className="child3",children=[html.Div([dropdown2], className="child3_1"),html.Div(dcc.Graph(id='graph3'), className="child3_2")]),
    html.H2("Further Classification of Energy Consumption per Countries/Regions", className="grouped-children-title"),
    html.Div(className="child4",children=[html.Div([radio1], className="child4_1"),html.Div(dcc.Graph(id='graph4'), className="child4_2")])

])

#define callback for energy consumption range slider
@app.callback(
    Output('consumption_range', 'max'),
    Output('consumption_range', 'value'),
    Output('consumption_range', 'marks'),
    [Input('energy_type', 'value')]
)
def update_slider_max(energy_type):
    max_consumption = int(energy_df[energy_type].max())
    marks = {str(num): str(num/1000) + "k" for num in range(0, max_consumption + 1, int(max_consumption/10))}
    return max_consumption, [0, max_consumption], marks

#graph1                                                             value = value we select
@app.callback(Output('graph1','figure'), [Input('consumption_range', "value"), Input('energy_type', "value"),  Input('year_range',"value"), Input("group_type","value")])
def myfunc(consumption_range, energy_type, year_range, group_type): #two inputs, so return two output
    #avg_y = energy_df.groupby(x_axis_col)[y_axis_col].mean().reset_index()
    filtered_df = energy_df[(energy_df[energy_type] >= consumption_range[0]) & (energy_df[energy_type] <= consumption_range[1])]
    filtered_df = filtered_df[(filtered_df['year'] >= year_range[0]) & (filtered_df['year'] <= year_range[1])]
    if "regions" in group_type and "countries" not in group_type:
        filtered_df = filtered_df[filtered_df['country'].isin(regions)]
    elif "countries" in group_type and "regions" not in group_type:
        filtered_df = filtered_df[filtered_df['country'].isin(countries)]
        
    figure = px.line(filtered_df, x='year', y=energy_type, color='country')
    formatted_title = energy_type.replace('_', ' ').title() + " (Terawatt Hours)"
    figure.update_layout(yaxis_title=formatted_title, height=700, xaxis_title="Year")    
    return figure

#graph2 (pie chart)                                                         
@app.callback(Output('graph2','figure'), [Input('energy_type', "value"), Input('years',"value"), Input('group_type','value')])
def myfunc(energy_type, year, group_type): 
    # filter df for one year and only for countries with data
    filtered_df = energy_df[(energy_df['year'] == year)]
    if "regions" in group_type and "countries" not in group_type:
        filtered_df = filtered_df[filtered_df['country'].isin(regions)]
    elif "countries" in group_type and "regions" not in group_type:
        filtered_df = filtered_df[filtered_df['country'].isin(countries)]
    # Find countries with value < 1% of world total and sum their values
    total_world_consumption = filtered_df[energy_type].sum()
     # Calculate each country's percentage of world consumption
    filtered_df['percentage_of_world'] = (filtered_df[energy_type] / total_world_consumption) * 100
    
    # Find countries with their percentage of world consumption < 2% and sum their values
    small_percentage_df = filtered_df[filtered_df['percentage_of_world'] < 1]
    others_sum = small_percentage_df[energy_type].sum()
    
    # Remove these countries from the original df
    filtered_df = filtered_df[filtered_df['percentage_of_world'] >= 1]
    
    # Remove the temporary 'percentage_of_world' column as it's no longer needed
    filtered_df = filtered_df.drop(columns=['percentage_of_world'])
    
    # If there are any values to add to 'Others', do so
    if others_sum > 0:
        others_row = pd.DataFrame({'country': ['Others'], energy_type: [others_sum]})
        filtered_df = pd.concat([filtered_df, others_row], ignore_index=True)

    figure = go.Figure(data=[go.Pie(labels=filtered_df['country'], values=filtered_df[energy_type])])
    formatted_title = "Percentage of world " + energy_type.replace('_', ' ') + " in " + str(year)
    figure.update_layout(height=400, autosize=False, title=formatted_title)    

        
    return figure

#Define callback function for graph 3
@app.callback(Output('graph3','figure'), [Input('country_selection', "value"),  Input('year_range',"value")])
def myfunc(country, year_range): #two inputs, so return two output
    filtered_df = energy_df[energy_df['country'] == country]
    filtered_df = filtered_df[(filtered_df['year'] >= year_range[0]) & (filtered_df['year'] <= year_range[1])]
    # Transforming the DataFrame to a long format
    long_df = pd.melt(filtered_df, id_vars=['year'], var_name='energy_type', value_name='energy_consumption', value_vars=[col for col in filtered_df.columns if col not in ['year', 'country'] and "consumption" in col])
    figure2 = px.line(long_df, x='year', y="energy_consumption", color='energy_type')
    figure2.update_layout(yaxis_title="Energy Consumption in Terawatt Hours", height=700, xaxis_title="Year")    
    return figure2

#Define callback function for graph 4
@app.callback(Output('graph4','figure'), [Input('radio1',"value")])
def myfunc(radio_option): #two inputs, so return two output
    filtered_df = energy_df[energy_df['country'].isin(countries)]
    filtered_df = filtered_df[filtered_df[radio_option].notnull()]
    # Transforming the DataFrame to a long format
    figure = px.line(filtered_df, x='year', y=radio_option, color='country')
    figure.update_layout(yaxis_title=radio_option.title(), height=700, xaxis_title="Year")    
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
