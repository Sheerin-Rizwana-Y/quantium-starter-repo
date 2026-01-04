import pytest
import pandas as pd
import plotly.express as px
from app import update_chart, df   # assuming your main file is app.py

#  Test: Missing date range
def test_update_chart_missing_dates():
    fig = update_chart("all", None, None)
    assert isinstance(fig, px.line().__class__)
    assert fig.layout.title.text == "Please select a valid date range"

#  Test: No data for given filters
def test_update_chart_no_data():
    # Pick a date range outside the dataset
    start_date = "1900-01-01"
    end_date = "1900-12-31"
    fig = update_chart("north", start_date, end_date)
    assert fig.layout.title.text == "No data available for selected filters"

# Test: Region filter works
def test_update_chart_region_filter():
    # Use actual min/max dates from df
    start_date = str(df["date"].min().date())
    end_date = str(df["date"].max().date())
    fig = update_chart("north", start_date, end_date)

    # Ensure figure has traces
    assert len(fig.data) > 0
    # Ensure x-axis is "date"
    assert fig.layout.xaxis.title.text == "Date"
    # Ensure y-axis is "Total Sales ($)"
    assert fig.layout.yaxis.title.text == "Total Sales ($)"

#  Test: "all" region includes multiple regions
def test_update_chart_all_regions():
    start_date = str(df["date"].min().date())
    end_date = str(df["date"].max().date())
    fig = update_chart("all", start_date, end_date)

    assert fig.layout.title.text == "Pink Morsel Sales Over Time"
    assert len(fig.data) > 0