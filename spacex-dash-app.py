# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(
    children=[
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 40},
        ),

        # TASK 1: Dropdown for Launch Site selection
        dcc.Dropdown(
            id="site-dropdown",
            options=[
                {"label": "All Sites", "value": "ALL"},
                *[
                    {"label": site, "value": site}
                    for site in sorted(spacex_df["Launch Site"].unique())
                ],
            ],
            value="ALL",
            placeholder="Select a Launch Site here",
            searchable=True,
        ),

        html.Br(),

        # TASK 2: Pie chart
        html.Div(dcc.Graph(id="success-pie-chart")),
        html.Br(),

        html.P("Payload range (Kg):"),

        # TASK 3: Range Slider for payload
        dcc.RangeSlider(
            id="payload-slider",
            min=min_payload,
            max=max_payload,
            step=1000,
            marks={int(min_payload): str(int(min_payload)), int(max_payload): str(int(max_payload))},
            value=[min_payload, max_payload],
        ),

        # TASK 4: Scatter plot
        html.Div(dcc.Graph(id="success-payload-scatter-chart")),
    ]
)

# TASK 2: Callback for pie chart
@app.callback(
    Output("success-pie-chart", "figure"),
    Input("site-dropdown", "value")
)
def get_pie_chart(entered_site):
    if entered_site == "ALL":
        # Total successful launches for all sites
        df_success = (
            spacex_df[spacex_df["class"] == 1]["Launch Site"]
            .value_counts()
            .reset_index()
        )
        df_success.columns = ["Launch Site", "Successes"]

        fig = px.pie(
            df_success,
            values="Successes",
            names="Launch Site",
            title="Total Successful Launches by Site",
        )
        return fig
    else:
        # Success vs Failed for a specific site
        df_site = spacex_df[spacex_df["Launch Site"] == entered_site]
        outcome = df_site["class"].value_counts().reset_index()
        outcome.columns = ["class", "count"]
        outcome["Outcome"] = outcome["class"].map({1: "Success", 0: "Failure"})

        fig = px.pie(
            outcome,
            values="count",
            names="Outcome",
            title=f"Total Launch Outcomes for site {entered_site}",
        )
        return fig

# TASK 4: Callback for scatter chart
@app.callback(
    Output("success-payload-scatter-chart", "figure"),
    [Input("site-dropdown", "value"), Input("payload-slider", "value")]
)
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range

    df_filtered = spacex_df[
        (spacex_df["Payload Mass (kg)"] >= low) &
        (spacex_df["Payload Mass (kg)"] <= high)
    ]

    if entered_site != "ALL":
        df_filtered = df_filtered[df_filtered["Launch Site"] == entered_site]
        title = f"Correlation between Payload and Success for site {entered_site}"
    else:
        title = "Correlation between Payload and Success for all sites"

    fig = px.scatter(
        df_filtered,
        x="Payload Mass (kg)",
        y="class",
        color="Booster Version Category",
        title=title,
    )
    return fig

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
