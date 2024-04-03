import dash
from dash import dcc, html, Output, Input
import pandas as pd
import plotly.express as px
# Load the dataset from the csv file
csv_file_path = './Midterm/World Energy Consumption.csv'
energy_df = pd.read_csv(csv_file_path)

# Get the data columns
columns_to_use = ['fossil_fuel_consumption', 'country']
#fuel_df = pd.read_csv(csv_file_path, usecols=columns_to_use)
years_df = energy_df[energy_df['biofuel_consumption'].notnull() & energy_df['fossil_fuel_consumption'].notnull() & energy_df['coal_consumption'].notnull() & energy_df['gas_consumption'].notnull() & energy_df['hydro_consumption'].notnull() & energy_df['nuclear_consumption'].notnull() & energy_df['oil_consumption'].notnull() & energy_df['other_renewable_consumption'].notnull() & energy_df['solar_consumption'].notnull()]

countries_with_fuel_data = years_df['country'].unique()

# Print out the countries
#for country in filtered_df['year'].unique():
 #   print(country)\
    
energy_categories = ['biofuel_consumption', 'fossil_fuel_consumption', 'coal_consumption', 'gas_consumption', 'hydro_consumption', 'nuclear_consumption', 'oil_consumption', 'other_renewable_consumption', 'solar_consumption', 'wind_consumption']

#find maximum energy consumption for slider
max_consumption = 0

min_year = years_df['year'].min()
max_year = years_df['year'].max()

dropdown1=html.Div(className="child1_1_1",children=[dcc.Dropdown(id='energy_type',options=energy_categories, value=energy_categories[0])], style=dict(width="100%"))
dropdown2=html.Div(className="child1_1_2",children=[html.Label('Select Energy Consumption Range (Terawatt Hours)', style={'font-weight': 'bold'}),dcc.RangeSlider(id='consumption_range',min=0,max=max_consumption,value=[0, max_consumption],marks={str(num): str(num/1000) for num in range(0, max_consumption + 1, 2500)}, step=500)], style=dict(width="100%"))
slider2=html.Div(className="child1_1_3",children=[html.Label('Select Year Range', style={'font-weight': 'bold'}), dcc.RangeSlider(id='year_range',min=min_year,max=max_year,value=[min_year, max_year],marks={str(num): str(num) for num in range(0, max_year + 1, 5)}, step=1)], style=dict(width="100%"))
radio1=html.Div(className="child2_1_1",children=[dcc.RadioItems(id='radio', options=[], value="", inline=True)])

app = dash.Dash(__name__)

app.layout = html.Div(className="parent", children=[
    html.Div(className="child1",children=[html.Div([dropdown1,dropdown2,slider2], className="child1_1"),html.Div(dcc.Graph(id='graph1'), className="child1_2")]),
    html.Div(className="child2",children=[html.Div(radio1, className="child2_1"),html.Div(dcc.Graph(id='graph2'), className="child2_2")])
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
@app.callback([Output('graph1','figure'), Output('radio', 'options')], [Input('consumption_range', "value"), Input('energy_type', "value")],  Input('year_range',"value"))
def myfunc(consumption_range, energy_type, year_range): #two inputs, so return two output
    #avg_y = energy_df.groupby(x_axis_col)[y_axis_col].mean().reset_index()
    filtered_df = energy_df[(energy_df[energy_type] >= consumption_range[0]) & (energy_df[energy_type] <= consumption_range[1])]
    filtered_df = filtered_df[(filtered_df['year'] >= year_range[0]) & (filtered_df['year'] <= year_range[1])]
    figure = px.line(filtered_df, x='year', y=energy_type, color='country')
    formatted_title = energy_type.replace('_', ' ').title() + " (Terawatt Hours)"
    figure.update_layout(yaxis_title=formatted_title, height=700, xaxis_title="Year")    
    return figure, energy_df['year'].unique()

#Define callback function for graph 2
@app.callback(Output('graph2', 'figure'),[Input('radio', 'value'),Input('x-axis-dropdown', 'value'),Input('y-axis-dropdown', 'value')])
def update_graph(selected_value,x_attr,y_attr):
    if(len(selected_value)==0):
        return {}
    filtered_df=energy_df[energy_df[x_attr]==selected_value]
    figure = px.scatter(filtered_df, x=filtered_df.reset_index().index, y=y_attr)
    figure.update_layout(plot_bgcolor="#f7f7f7")
    figure.update_xaxes(showticklabels=False)
    figure.update_traces(marker=dict(size=10,color='gray',opacity=0.8))
    figure.add_shape(type="line", x0=0, x1=filtered_df.reset_index().index.max(), y0=filtered_df[y_attr].mean(), y1=filtered_df[y_attr].mean(), line=dict(color="#77a3ba", width=2))
    print(figure.layout.xaxis)
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
