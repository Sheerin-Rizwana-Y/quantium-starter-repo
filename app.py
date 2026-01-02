import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# Load processed data
df = pd.read_csv("processed_sales.csv")
df["date"] = pd.to_datetime(df["date"])

# Create Dash app
app = dash.Dash(__name__)

app.layout = html.Div(
    style={"padding": "20px"},
    children=[
        html.H1(
            "Soul Foods Sales Dashboard",
            style={"textAlign": "center"}
        ),

        html.P(
            "Explore Pink Morsel sales over time. "
            "Use the filters to answer different business questions.",
            style={"textAlign": "center"}
        ),

        # Filters
        html.Div(
            style={"display": "flex", "justifyContent": "space-between"},
            children=[
                html.Div(
                    children=[
                        html.Label("Select Region"),
                        dcc.Dropdown(
                            options=[
                                {"label": r.title(), "value": r}
                                for r in sorted(df["region"].unique())
                            ],
                            value=df["region"].unique().tolist(),
                            multi=True,
                            id="region-filter"
                        ),
                    ],
                    style={"width": "45%"}
                ),

                html.Div(
                    children=[
                        html.Label("Select Date Range"),
                        dcc.DatePickerRange(
                            start_date=df["date"].min(),
                            end_date=df["date"].max(),
                            display_format="YYYY-MM-DD",
                            id="date-range"
                        ),
                    ],
                    style={"width": "45%"}
                ),
            ]
        ),

        # Graph
        dcc.Graph(id="sales-line-chart"),
    ]
)

@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-filter", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_chart(selected_regions, start_date, end_date):
    filtered_df = df[
        (df["region"].isin(selected_regions)) &
        (df["date"] >= start_date) &
        (df["date"] <= end_date)
    ]

    fig = px.line(
        filtered_df.sort_values("date"),
        x="date",
        y="sales",
        color="region",
        labels={
            "date": "Date",
            "sales": "Total Sales ($)",
            "region": "Region"
        },
        title="Pink Morsel Sales Over Time"
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)
