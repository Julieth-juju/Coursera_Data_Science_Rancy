#!/usr/bin/env python
# coding: utf-8

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/d51iMGfp_t0QpO30Lym-dw/automobile-sales.csv'
)

app = dash.Dash(__name__)

dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

year_list = list(range(1980, 2024))

app.layout = html.Div([
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 24}
    ),

    html.Div([
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            placeholder='Select a report type',
            value='Yearly Statistics'
        )
    ], style={'width': '50%', 'margin': 'auto'}),

    html.Div([
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            placeholder='Select a year',
            value=1980
        )
    ], style={'width': '50%', 'margin': 'auto', 'marginTop': '10px'}),

    html.Div(id='output-container', className='chart-grid')
])


@app.callback(
    Output('select-year', 'disabled'),
    Input('dropdown-statistics', 'value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    return True


@app.callback(
    Output('output-container', 'children'),
    [Input('dropdown-statistics', 'value'),
     Input('select-year', 'value')]
)
def update_output_container(selected_statistics, selected_year):

    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]

        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(figure=px.line(
            yearly_rec,
            x='Year',
            y='Automobile_Sales',
            title="Average Automobile Sales fluctuation over Recession Period"
        ))

        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(figure=px.bar(
            average_sales,
            x='Vehicle_Type',
            y='Automobile_Sales',
            title="Average Automobile Sales by Vehicle Type during Recessions"
        ))

        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(figure=px.pie(
            exp_rec,
            values='Advertising_Expenditure',
            names='Vehicle_Type',
            title='Total Advertising Expenditure Share by Vehicle Type during Recessions'
        ))

        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(figure=px.bar(
            unemp_data,
            x='unemployment_rate',
            y='Automobile_Sales',
            color='Vehicle_Type',
            labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
            title='Effect of Unemployment Rate on Vehicle Type and Sales'
        ))

        return [
            html.Div(
                className='chart-item',
                children=[html.Div(children=R_chart1), html.Div(children=R_chart2)],
                style={'display': 'flex'}
            ),
            html.Div(
                className='chart-item',
                children=[html.Div(children=R_chart3), html.Div(children=R_chart4)],
                style={'display': 'flex'}
            )
        ]

    if selected_statistics == 'Yearly Statistics' and selected_year:
        yearly_data = data[data['Year'] == selected_year]

        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(
            yas,
            x='Year',
            y='Automobile_Sales',
            title='Yearly Automobile Sales'
        ))

        mas = data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(figure=px.line(
            mas,
            x='Month',
            y='Automobile_Sales',
            title='Total Monthly Automobile Sales'
        ))

        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(
            avr_vdata,
            x='Vehicle_Type',
            y='Automobile_Sales',
            title='Average Vehicles Sold by Vehicle Type in the year {}'.format(selected_year)
        ))

        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(
            exp_data,
            values='Advertising_Expenditure',
            names='Vehicle_Type',
            title='Total Advertisment Expenditure for Each Vehicle'
        ))

        return [
            html.Div(
                className='chart-item',
                children=[html.Div(children=Y_chart1), html.Div(children=Y_chart2)],
                style={'display': 'flex'}
            ),
            html.Div(
                className='chart-item',
                children=[html.Div(children=Y_chart3), html.Div(children=Y_chart4)],
                style={'display': 'flex'}
            )
        ]

    return None


if __name__ == '__main__':
    app.run(debug=True)
