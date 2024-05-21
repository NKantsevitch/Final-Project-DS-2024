import streamlit as st
import pandas as pd
import numpy as np

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


def load_data():
    df_food = pd.read_csv('Data/Processed/df_food.csv')
    df_sector = pd.read_csv('Data/Processed/df_sector_imputed.csv')
    df_import = pd.read_csv('Data/Processed/df_import.csv')
    return df_food, df_sector, df_import

df_food, df_sector, df_import = load_data()

sorted_locs = ['Canada', 'Alberta', 'British Columbia', 'Manitoba', 'New Brunswick',
 'Newfoundland and Labrador', 'Nova Scotia', 'Ontario', 'Prince Edward Island', 'Quebec',
 'Saskatchewan']

sorted_sectors = ['Accommodation and food services',
 'Agriculture',
 'Business, building and other support services',
 'Construction',
 'Educational services',
 'Finance, insurance, real estate, rental and leasing',
 'Forestry, fishing, mining, quarrying, oil and gas',
 'Goods-producing sector',
 'Health care and social assistance',
 'Information, culture and recreation',
 'Manufacturing',
 'Other services (except public administration)',
 'Professional, scientific and technical services',
 'Public administration',
 'Services-producing sector',
 'Total, all industries',
 'Transportation and warehousing',
 'Wholesale and retail trade']

def show_explore_page():
    st.title("Economic Situation in Canada: Food Prices, US Imports and Unemployment Rates")

    #Plot 1

    st.write( """ ### Food Prices *2017 to 2024*
             """)
    
    df_food.set_index('Date', inplace=False)
    
    grouped_data = df_food.groupby(['Date', 'Location'])['Price'].mean().unstack().reset_index()

    grouped_data = grouped_data[['Date'] + sorted_locs]

    fig1 = px.line(grouped_data, x='Date', y=grouped_data.columns[1:], 
                   color_discrete_sequence=px.colors.qualitative.Alphabet,
                   title='Average Price of Food by Location Over Time')

    fig1.update_layout(
        xaxis_title='Date',
        yaxis_title='Average Price',
        legend_title=dict(text='Location (select to isolate)', font=dict(size=16)),
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

    # Plot 2

    st.write( """ ### Imports From USA to Canada *2017 to 2024*
             """)
    
    grouped_data = df_import.groupby(['Date', 'Location'])["Dollar Value ('000s')"].mean().unstack().reset_index()

    grouped_data = grouped_data[['Date'] + sorted_locs]

    # Create a line plot using Plotly
    fig2 = px.line(grouped_data, x='Date', y=grouped_data.columns[1:], 
              color_discrete_sequence=px.colors.qualitative.Alphabet,
              title='Average Import Value by Location Over Time')

    # Update layout
    fig2.update_layout(
        xaxis_title='Date',
        yaxis_title='Average Import Value',
        legend_title='Location (select to isolate)',
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

    st.plotly_chart(fig2)


    st.markdown("----")

        # Pie Chart 1

    st.write( """ ### US Imports by Category
                """)


    selected_location = st.selectbox('Select Location:', sorted_locs)

    selected_year = st.selectbox('Select Year:', pd.to_datetime(df_import['Date']).dt.year.unique())

    filtered_df = df_import[(pd.to_datetime(df_import['Date']).dt.year == selected_year) &
                            (df_import['Location'] == selected_location)]

    avg_import = filtered_df.groupby('Category')["Dollar Value ('000s')"].mean()

    color_mapping = {
        'Animal or vegetable oils': '#636EFA',  # Blue
        'Live animals or animal products': '#EF553B',  # Red
        'Processed food and beverages' : '#ADD8E6', # Light Blue
        'Vegetable products' : '#228B22' #Green
    }

    category_colors = [color_mapping[category] for category in avg_import.index]

    fig_pie = go.Figure(data=[go.Pie(labels=avg_import.index, values=avg_import.values, 
                                     marker=dict(colors=category_colors))])

    fig_pie.update_layout(title=f'Import Distribution by Category for {selected_location}', 
                           height=600, width=800)

    st.plotly_chart(fig_pie)

    st.markdown("----")

    # Plot 3

    st.write( """ ### Unemployment Rates *2017 to 2024*
                """)
        
    grouped_data = df_sector.groupby(['Date', 'Location'])['Unemployment Rate'].mean().unstack().reset_index()

    grouped_data = grouped_data[['Date'] + sorted_locs]
        
    fig3 = px.line(grouped_data, x='Date', y=grouped_data.columns[1:], 
              color_discrete_sequence=px.colors.qualitative.Alphabet,
              title='Average Unemployment Rate by Location Over Time')

    fig3.update_layout(
            xaxis_title='Date',
            yaxis_title='Average Unemployment Rate (%)',
            legend_title=dict(text='Location (select to isolate)', font=dict(size=16)),
            xaxis=dict(
                tickmode='linear',
                tick0=grouped_data['Date'].min(),
                dtick='M6',
                tickformat='%Y-%m'),
            margin=dict(l=40, r=40, t=200, b=40),
            height=600,
            legend=dict(
            orientation='h',  # Horizontal orientation
            yanchor='bottom',  # Anchor to the bottom of the plot
            y=1,  # Adjust the distance from the plot
            xanchor='right',
            x=1)
        )

    st.plotly_chart(fig3)

    st.markdown("----")

    # Pie Chart 2

    st.write( """ ### Unemployment Rates By Sector
                """)

    unemployment_location = st.selectbox('Select Location: ', df_sector['Location'].unique())

    unemployment_year = st.selectbox('Select Year: ', pd.to_datetime(df_sector['Date']).dt.year.unique())


    filtered_df = df_sector[(df_sector['Location'] == unemployment_location) & 
                            (pd.to_datetime(df_sector['Date']).dt.year == unemployment_year) &
                            (df_sector['Sector'] != 'Total, all industries')]
    
    unique_sectors = sorted(filtered_df['Sector'].unique())

    unemployment_sector = st.selectbox('Select Sector:', unique_sectors)

    sector_avg_unemployment = filtered_df.groupby('Sector')["Unemployment ('000s)"].mean()
    sector_avg_unemployment_rate = filtered_df.groupby('Sector')["Unemployment Rate"].mean()

    pull_values = {sector: 0 for sector in unique_sectors}

    pull_values[unemployment_sector] = 0.2

    pull_values_list = list(pull_values.values())

    colors = px.colors.qualitative.Plotly[:len(sector_avg_unemployment)]

    fig_pie2 = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])

    fig_pie2.add_trace(go.Pie(labels=sector_avg_unemployment.index, 
                          values=sector_avg_unemployment.values,
                          marker=dict(colors=colors), pull=pull_values_list,
                          hoverinfo='label+value'
                         ), 1, 1)
                                  #sort=False #does not work

    fig_pie2.add_trace(go.Pie(labels=sector_avg_unemployment_rate.index, 
                          values=sector_avg_unemployment_rate.values,
                          marker=dict(colors=colors), pull=pull_values_list,
                          hoverinfo='label+percent'
                         ), 1, 2)     


    fig_pie2.update_layout(title=f'Unemployment Rate Distribution by Sector for {unemployment_location}',
                           annotations= [dict(text="Disrtibution of<br>Unemployed Individuals ('000s)", 
                                              x=0.08, y=.87, showarrow=False), 
                                         dict(text='Distribution of<br>Unemployment Rates', 
                                              x=0.87, y=.87, showarrow=False)], 
                           height=600, width=950)

    #st.write("Average Unemployment ('000s):", sector_avg_unemployment)
    #st.write("Average Unemployment Rate:", sector_avg_unemployment_rate)

    st.plotly_chart(fig_pie2)

        
        
