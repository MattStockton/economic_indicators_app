import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from fredapi import Fred
from datetime import datetime, timedelta
import os
import requests
from bs4 import BeautifulSoup

# Set page configuration
st.set_page_config(page_title="Economic Indicators Dashboard", layout="wide")

# Custom CSS for enterprise styling with improved readability
st.markdown("""
<style>
    .reportview-container {
        background-color: #1e1e1e;
        color: #ffffff;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3 {
        color: #ffffff;
    }
    .stSelectbox, .stCheckbox {
        background-color: #2d2d2d;
        color: #ffffff;
        border-radius: 5px;
        padding: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
    }
    .stPlotlyChart {
        background-color: #2d2d2d;
        border-radius: 5px;
        padding: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
    }
    .css-1d391kg {
        padding-top: 3.5rem;
    }
    .stCheckbox > label > div[role="checkbox"] {
        background-color: #4a4a4a !important;
    }
    .stCheckbox > label {
        color: #ffffff !important;
    }
    .stSelectbox > div > div {
        background-color: #4a4a4a !important;
        color: #ffffff !important;
    }
    .stSelectbox > label {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize FRED API
fred = Fred(api_key=os.getenv('FRED_API_KEY'))

@st.cache_data
def get_sp500_symbols():
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'class': 'wikitable sortable'})
    symbols = []
    sectors = {}
    for row in table.findAll('tr')[1:]:
        symbol = row.findAll('td')[0].text.strip()
        company = row.findAll('td')[1].text.strip()
        sector = row.findAll('td')[3].text.strip()
        symbols.append(f"{symbol} - {company}")
        sectors[symbol] = sector
    return symbols, sectors

@st.cache_data
def get_stock_data(ticker, start_date, end_date):
    stock = yf.Ticker(ticker)
    df = stock.history(start=start_date, end=end_date)
    df['Monthly_Return'] = df['Close'].pct_change(periods=30)
    return df.resample('M').last()

@st.cache_data
def get_sector_etf(sector):
    sector_etfs = {
        "Information Technology": "XLK",
        "Health Care": "XLV",
        "Financials": "XLF",
        "Consumer Discretionary": "XLY",
        "Communication Services": "XLC",
        "Industrials": "XLI",
        "Consumer Staples": "XLP",
        "Energy": "XLE",
        "Utilities": "XLU",
        "Real Estate": "XLRE",
        "Materials": "XLB"
    }
    return sector_etfs.get(sector, "SPY")  # Default to S&P 500 ETF if sector not found

@st.cache_data
def get_fred_data(series_id, start_date, end_date):
    data = fred.get_series(series_id, start_date, end_date)
    df = pd.DataFrame(data, columns=['Value'])
    
    if series_id == 'GDP':
        df.index = pd.to_datetime(df.index)
        monthly_dates = pd.date_range(start=df.index.min(), end=df.index.max(), freq='MS')
        monthly_df = pd.DataFrame(index=monthly_dates, columns=['Value'])
        monthly_df.update(df)
        monthly_df['Value'] = monthly_df['Value'].interpolate(method='linear')
        df = monthly_df
    
    df['YoY_Change'] = df['Value'].pct_change(periods=12)
    return df

def create_chart(data, title, y_column):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data[y_column], mode='lines', line=dict(color='#4a9ff5')))
    fig.update_layout(
        title=title,
        height=300,
        width=400,
        paper_bgcolor='rgba(45,45,45,1)',
        plot_bgcolor='rgba(45,45,45,1)',
        font=dict(color='#ffffff'),
        xaxis=dict(showgrid=True, gridcolor='#444444'),
        yaxis=dict(showgrid=True, gridcolor='#444444')
    )
    return fig

all_metrics = {
    'GDP': 'GDP',
    'CPI': 'CPIAUCSL',
    'Unemployment Rate': 'UNRATE',
    'Industrial Production Index': 'INDPRO',
    'Consumer Sentiment': 'UMCSENT',
    'Retail Sales': 'RSAFS',
}

st.title('Economic Indicators and Stock Market Dashboard')

# Create two columns for the layout
col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("Dashboard Controls")
    
    # Fetch S&P 500 symbols and sectors
    sp500_symbols, sp500_sectors = get_sp500_symbols()

    # Allow user to select any S&P 500 stock
    selected_stock = st.selectbox('Select a S&P 500 Stock', sp500_symbols)
    selected_symbol = selected_stock.split(' - ')[0]  # Extract just the symbol

    end_date = datetime.now()
    start_date = end_date - timedelta(days=365*5)

    st.subheader("Economic Indicators")
    selected_metrics = []
    for metric, series_id in all_metrics.items():
        if st.checkbox(f'Include {metric}', key=f'checkbox_{metric}'):
            selected_metrics.append(metric)

with col2:
    stock_data = get_stock_data(selected_symbol, start_date, end_date)

    # Get sector information and fetch sector ETF data
    selected_sector = sp500_sectors[selected_symbol]
    sector_etf = get_sector_etf(selected_sector)
    sector_data = get_stock_data(sector_etf, start_date, end_date)

    # Create combined chart
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add stock price to primary y-axis
    fig.add_trace(
        go.Scatter(x=stock_data.index, y=stock_data['Close'], name=f'{selected_symbol} Stock Price', line=dict(color='#4a9ff5')),
        secondary_y=False,
    )

    # Add sector ETF price to primary y-axis
    fig.add_trace(
        go.Scatter(x=sector_data.index, y=sector_data['Close'], name=f'{selected_sector} Sector ETF ({sector_etf})', line=dict(color='#50c878')),
        secondary_y=False,
    )

    # Add FRED data YoY changes to secondary y-axis
    colors = ['#ff6b6b', '#feca57', '#48dbfb', '#ff9ff3', '#54a0ff', '#5f27cd']
    for i, metric in enumerate(selected_metrics):
        data = get_fred_data(all_metrics[metric], start_date, end_date)
        
        if not data.empty and not data['YoY_Change'].isnull().all():
            fig.add_trace(
                go.Scatter(x=data.index, y=data['YoY_Change'], name=f'{metric} YoY Change', line=dict(color=colors[i % len(colors)])),
                secondary_y=True,
            )

    fig.update_layout(
        title_text=f"Stock Price ({selected_symbol}), Sector ETF ({sector_etf}), and Economic Indicators YoY Change",
        xaxis_title="Date",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=600,
        paper_bgcolor='rgba(45,45,45,1)',
        plot_bgcolor='rgba(45,45,45,1)',
        font=dict(color='#ffffff'),
        xaxis=dict(showgrid=True, gridcolor='#444444'),
        yaxis=dict(showgrid=True, gridcolor='#444444'),
    )

    fig.update_yaxes(title_text="Price", secondary_y=False)
    fig.update_yaxes(title_text="YoY Change (%)", secondary_y=True)

    st.plotly_chart(fig, use_container_width=True)

    # Individual charts for actual values
    if selected_metrics:
        st.subheader("Individual Indicator Charts")
        chart_cols = st.columns(2)

        for i, metric in enumerate(selected_metrics):
            data = get_fred_data(all_metrics[metric], start_date, end_date)
            
            with chart_cols[i % 2]:
                if not data.empty:
                    st.plotly_chart(create_chart(data, f'{metric} Value', 'Value'), use_container_width=True)
                else:
                    st.warning(f"{metric} data is not available for the selected time range.")
    else:
        st.info("Please select at least one economic indicator to display individual charts.")

    # Display raw data in an expander
    with st.expander("View Raw Data"):
        st.subheader('Raw Data')
        st.write(f"{selected_symbol} Stock Data:", stock_data)
        st.write(f"{selected_sector} Sector ETF ({sector_etf}) Data:", sector_data)
        for metric in selected_metrics:
            st.write(f"{metric} Data:", get_fred_data(all_metrics[metric], start_date, end_date))