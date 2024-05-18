import streamlit as st
import pandas as pd
import numpy as np

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
#import plotly.io as pio

import datetime as datetime


#@st.cache_data # To prevent data from being loaded for every step

def load_data():
    df_food = pd.read_csv('Data/Processed/df_food.csv')
    df_sector = pd.read_csv('Data/Processed/df_sector_imputed.csv')
    return df_food, df_sector

df_food, df_sector = load_data()

df_sector.drop(columns="Unemployment ('000s)", inplace=True)

def convert_to_datetime(df):
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df_food = convert_to_datetime(df_food)
df_sector = convert_to_datetime(df_sector)

sorted_locs = ['Canada', 'Alberta', 'British Columbia', 'Manitoba', 'New Brunswick',
 'Newfoundland and Labrador', 'Nova Scotia', 'Ontario', 'Prince Edward Island', 'Quebec',
 'Saskatchewan']

def show_predict_page2():
    
    st.title(" Canadian Food Prices and Unemployment Rates")

    st.write( """ #### Visualizing Unemployment Rates by Sector and Food Price
             """)
    
    #Plot 1

    
    selected_sectors = st.multiselect('Select Sector(s):', df_sector['Sector'].unique())

    if not selected_sectors:  # If nothing selected, show all sectors
        filtered_df = df_sector
    else:
        filtered_df = df_sector[df_sector['Sector'].isin(selected_sectors)]

       # Group sector by sector and date
    grouped_sector = filtered_df.groupby(['Date', 'Sector'])['Unemployment Rate'].mean().unstack().reset_index()

    # Group food prices by date
    grouped_food = df_food.groupby('Date')['Price'].mean().reset_index()

    trace_sector = go.Figure()
    for column in grouped_sector.columns[1:]:
        trace_sector.add_trace(go.Scatter(x=grouped_sector['Date'], 
                                        y=grouped_sector[column], mode='lines', 
                                        name=column))

    trace_food = go.Figure()
    trace_food.add_trace(go.Scatter(x=grouped_food['Date'], 
                                    y=grouped_food['Price'], 
                                    mode='lines', 
                                    line=dict(color='white'), 
                                    name='Price'))

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    for trace in trace_sector.data:
        fig.add_trace(trace)
    fig.add_trace(trace_food.data[0], secondary_y=True)

    fig.update_layout(
        height=500,
        width=900,
        title='Unemployment Rate and Food Price by Sector',
        xaxis=dict(tickangle=45),
        legend_title='Sector'
    )

    st.plotly_chart(fig)

    st.markdown("----")
    

    #Plot 2

    st.write( """ #### Visualizing Unemployment Rates by Sector and Location
             """)

    #Select Sector
    sector = st.selectbox('Select Sector:', df_sector['Sector'].unique())

    filtered_df = df_sector[df_sector['Sector'] == sector]

    #Select :Location
    location = st.selectbox('Select Location:', sorted_locs)

    filtered_df2 = filtered_df[filtered_df['Location'] == location]

    # Drop Down Select Dates
    date_options = [date.strftime('%Y-%m') for date in df_sector['Date'].unique()]
    start_date = st.selectbox('Select Date 1:', options=date_options)
    end_date = st.selectbox('Select Date 2:', options=date_options)

    # Convert start and end dates to datetime
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    #New DF for selected Date Range
    filtered_df = filtered_df2[(filtered_df2['Date'] >= start_date) & (filtered_df2['Date'] <= end_date)]

    #Group by Date and Location
    grouped_data = filtered_df.groupby(['Date', 'Sector'])['Unemployment Rate'].mean().unstack().reset_index()

    # Plot
    fig1 = px.line(grouped_data, x='Date', y=grouped_data.columns[1:], 
              #title='Unemployment Rate by Sector'
              )
    
    fig1.update_layout(
        xaxis_title='Date',
        yaxis_title='Unemployment Rate',
        legend_title=dict(text='Sector', font=dict(size=16)),
        xaxis=dict(
            tickmode='linear',
            tick0=grouped_data['Date'].min(),
            dtick='M6',
            tickformat='%Y-%m'
        ),
        xaxis_tickangle=-45,
        margin=dict(l=40, r=40, t=180, b=40),
        height=600,
        legend=dict(
        orientation='h',  # Horizontal orientation
        yanchor='bottom',  # Anchor to the bottom of the plot
        y=1,  # Adjust the distance from the plot
        xanchor='right',
        x=1)
    )

    st.plotly_chart(fig1)

    

    
