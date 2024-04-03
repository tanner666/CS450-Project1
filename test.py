import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Assuming df is your DataFrame and it has a 'year' column and a 'value' column

# Load the dataset (replace with your actual data loading)
csv_file_path = './Midterm/World Energy Consumption.csv'
df = pd.read_csv(csv_file_path)

app = dash.Dash(__name__)

# Find the range of years in the dataset
min_year = df['year'].min()
max_year = df['year'].max()

app.layout = html.Div([
    dcc.RangeSlider(
        id='year-range-slider',
        min=min_year,
        max=max_year,
        value=[min_year, max_year],  # default value to include the whole range
        marks={str(year): str(year) for year in range(min_year, max_year + 1, 5)},  # marking every 5 years for example
        step=1
    ),
    dcc.Graph(id='line-chart')
])


@app.callback(
    Output('line-chart', 'figure'),
    [Input('year-range-slider', 'value')]
)
def update_chart(selected_years):
    # Filter the dataframe based on the selected year range
    filtered_df = df[(df['year'] >= selected_years[0]) & (df['year'] <= selected_years[1])]
    
    # Update the figure by re-plotting with the filtered dataframe
    figure = px.line(filtered_df, x='year', y='value', title='Energy Consumption Over Selected Years')
    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
