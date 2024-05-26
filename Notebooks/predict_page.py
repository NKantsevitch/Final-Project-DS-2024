import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio





def load_data():
    df_food = pd.read_csv('Data/Processed/df_food.csv')
    df_import = pd.read_csv('Data/Processed/df_import.csv')
    pivot_df = pd.read_csv('Data/Processed/pivot_df.csv') #used for correlation
    return df_food, df_import, pivot_df

df_food, df_import, pivot_df = load_data()

def convert_to_datetime(df):
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df_food = convert_to_datetime(df_food)
df_import = convert_to_datetime(df_import)

sorted_locs = ['Canada', 'Alberta', 'British Columbia', 'Manitoba', 'New Brunswick',
    'Newfoundland and Labrador', 'Nova Scotia', 'Ontario', 'Prince Edward Island', 'Quebec',
    'Saskatchewan']



def show_predict_page():

    st.title(" Canadian Food Prices and US Imports")

    #PLOT 1

    st.write( """ #### Compare Average Food Price Over Time by Location
             """)
    
    #Selecting Locations
    selected_locations = st.multiselect('Select Location(s):', sorted_locs)
    
    #New DF for selected location only
    filtered_df = df_food[df_food['Location'].isin(selected_locations)]

    # Calendar Select Dates
    date_options = [date.strftime('%Y-%m') for date in df_food['Date'].unique()]
    start_date = st.selectbox('Select Date 1:', options=date_options)
    end_date = st.selectbox('Select Date 2:', options=date_options)

    # Convert start and end dates to datetime
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    #New DF for selected Date Range
    filtered_df = filtered_df[(filtered_df['Date'] >= start_date) & (filtered_df['Date'] <= end_date)]

    #Group by Date and Location
    grouped_data = filtered_df.groupby(['Date', 'Location'])['Price'].mean().unstack().reset_index()

    # Plot
    fig1 = px.line(grouped_data, x='Date', y=selected_locations, 
              color_discrete_sequence=px.colors.qualitative.Alphabet,
              title='Average Price of Food by Location Over Time')
    
    fig1.update_layout(
        xaxis_title='Date',
        yaxis_title='Average Price',
        legend_title=dict(text='Location', font=dict(size=16)),
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
    

    st.markdown("----")

    #PLOT 2 - Price comparison, 2 dates

    st.write( """ #### Comparing the Price of a Food Item Over Time
             """)
    
    def compare_prices(food_item, location, date1, date2):
        # Filter the DataFrame based on the selected food item, location, and dates
        filtered_data = df_food[(df_food['Products'] == food_item) & 
                                (df_food['Location'] == location) & 
                                ((df_food['Date'] == date1) | (df_food['Date'] == date2))]
        
        # Group the filtered data by date and get the average price for the food item
        grouped_data = filtered_data.groupby('Date')['Price'].mean().reset_index()
        
        # Print the results
        st.write(f"Price for {date1.strftime('%Y-%m')}: {grouped_data.loc[grouped_data['Date'] == date1, 'Price'].item():.2f}")
        st.write(f"Price for {date2.strftime('%Y-%m')}: {grouped_data.loc[grouped_data['Date'] == date2, 'Price'].item():.2f}")

    # Dropdown list for selections
    food_item = st.selectbox('Select Food Item:', df_food['Products'].unique())
    location = st.selectbox('Select Location:', sorted_locs)

    date_options = [date.strftime('%Y-%m') for date in df_food['Date'].unique()]
    compare_start_date = st.selectbox('Select First Date:', options=date_options)
    compare_end_date = st.selectbox('Select Second Date:', options=date_options)

    # Convert start and end dates to datetime
    start_date = pd.to_datetime(compare_start_date)
    end_date = pd.to_datetime(compare_end_date)

    


    compare_prices(food_item, location, start_date, end_date)

    st.markdown("----")

        #PLOT 3 - correlation of select food categories and US Imports

    st.write( """ #### Correlation Between US Imports and Canadian Food Prices by Category
             """)
    
    def create_heatmap(start_date, end_date, location):
        filt_df = pivot_df[(pivot_df['Date'] >= start_date) & 
                           (pivot_df['Date'] <= end_date) & 
                           (pivot_df['Location'] == location)]

        corr = filt_df.drop(['Date', 'Location'], axis=1).corr()

        colorscale = px.colors.sequential.Blues

        #mask = np.triu(np.ones_like(corr, dtype=bool))

        corr_values = corr.values.round(2)

        #corr_masked = corr_values.mask(mask)

        fig3 = px.imshow(corr_values, x=corr.index, y=corr.columns, text_auto=True, color_continuous_scale=colorscale)
        
        fig3.update_layout(title=(f'Correlation Heatmap for {location}'))
        

        st.plotly_chart(fig3, theme='streamlit')

        return fig3



    start_date = st.selectbox('Select Start Date:', options=date_options)
    end_date = st.selectbox('Select End Date:', options=date_options)
    location = st.selectbox('Select Location', sorted_locs)

    create_heatmap(start_date, end_date, location)

    st.markdown("----")

    #PLOT 4

    st.write( """ #### Compare Average US Imports Over Time by Location
             """)
    
    #Selecting Locations
    select_location = st.selectbox('Select Location: ', sorted_locs)
    
    #New DF for selected location only
    filtered_df = df_import[df_import['Location'] == select_location]

    #Group by Date and Location
    grouped_data = filtered_df.groupby(['Date', 'Category'])["Dollar Value ('000s')"].mean().reset_index()

    # Plot
    fig4 = px.line(grouped_data, x='Date', y="Dollar Value ('000s')", 
              color='Category',
              title='US Imports')
    
    fig4.update_layout(
        xaxis_title='Date',
        yaxis_title='Average Imports',
        legend_title=dict(text='Category', font=dict(size=16)),
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

    st.plotly_chart(fig4)
    


    