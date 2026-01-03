import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px

# Load data
df = pd.read_csv("processed_sales.csv")
df["date"] = pd.to_datetime(df["date"])

app = dash.Dash(__name__)

app.layout = html.Div(
    style={
        "fontFamily": "Arial",
        "backgroundColor": "#f4f6f9",
        "padding": "30px"
    },
    children=[

        html.H1(
            "Soul Foods Pink Morsel Sales Visualiser",
            style={
                "textAlign": "center",
                "color": "#2c3e50"
            }
        ),

        html.P(
            "Use the controls below to explore region-specific sales trends "
            "and understand how sales changed over time.",
            style={
                "textAlign": "center",
                "color": "#555",
                "marginBottom": "30px"
            }
        ),

        # Controls container
        html.Div(
            style={
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "10px",
                "boxShadow": "0 4px 8px rgba(0,0,0,0.1)",
                "marginBottom": "30px"
            },
            children=[

                html.Label(
                    "Select Region",
                    style={"fontWeight": "bold"}
                ),

                dcc.RadioItems(
                    id="region-radio",
                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "North", "value": "north"},
                        {"label": "East", "value": "east"},
                        {"label": "South", "value": "south"},
                        {"label": "West", "value": "west"},
                    ],
                    value="all",
                    inline=True,
                    style={"marginBottom": "20px"}
                ),

                html.Label(
                    "Select Date Range",
                    style={"fontWeight": "bold"}
                ),

                dcc.DatePickerRange(
                    id="date-range",
                    start_date=df["date"].min(),
                    end_date=df["date"].max(),
                    display_format="YYYY-MM-DD"
                )
            ]
        ),

        # Chart container
        html.Div(
            style={
                "backgroundColor": "white",
                "padding": "20px",
                "borderRadius": "10px",
                "boxShadow": "0 4px 8px rgba(0,0,0,0.1)"
            },
            children=[
                dcc.Graph(id="sales-line-chart")
            ]
        )
    ]
)


@app.callback(
    Output("sales-line-chart", "figure"),
    Input("region-radio", "value"),
    Input("date-range", "start_date"),
    Input("date-range", "end_date"),
)
def update_chart(region, start_date, end_date):

    # 🔐 Safety checks (VERY IMPORTANT)
    if not start_date or not end_date:
        return px.line(title="Please select a valid date range")

    filtered_df = df[
        (df["date"] >= start_date) &
        (df["date"] <= end_date)
    ]

    if region != "all":
        filtered_df = filtered_df[filtered_df["region"] == region]

    # If no data after filtering
    if filtered_df.empty:
        return px.line(title="No data available for selected filters")

    filtered_df = filtered_df.sort_values("date")

    fig = px.line(
        filtered_df,
        x="date",
        y="sales",
        title="Pink Morsel Sales Over Time",
        labels={
            "date": "Date",
            "sales": "Total Sales ($)"
        }
    )

    # Price increase marker
    fig.add_vline(
    x=pd.Timestamp("2021-01-15"),
    line_dash="dash",
    line_color="red"
    
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    return fig



if __name__ == "__main__":
    app.run(debug=True)
