# app.py
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

# Import dataset
df = pd.read_csv(r'Imports_Exports_Dataset.csv')

# Random Sample from the dataset
df_sample = df.sample(n=3001, random_state=55011)

# Sidebar for filters
st.sidebar.title("Filters")

# Category filter
categories = df_sample['Category'].unique()
selected_categories = st.sidebar.multiselect("Select Categories", options=categories, default=categories)

# Import/Export filter
import_export_options = df_sample['Import_Export'].unique()
selected_import_export = st.sidebar.multiselect("Select Import/Export", options=import_export_options, default=import_export_options)

# Payment Terms filter
payment_terms = df_sample['Payment_Terms'].unique()
selected_payment_terms = st.sidebar.multiselect("Select Payment Terms", options=payment_terms, default=payment_terms)

# Filter the dataframe based on selections
filtered_df = df_sample[
    (df_sample['Category'].isin(selected_categories)) &
    (df_sample['Import_Export'].isin(selected_import_export)) &
    (df_sample['Payment_Terms'].isin(selected_payment_terms))
]

# Title of the dashboard
st.title("Imports and Exports Dashboard")

# Check if filtered_df is not empty
if not filtered_df.empty:
    # Create the first row for the first two charts
    col1, col2 = st.columns(2)

    with col1:
        # Count the number of Import and Export transactions in the filtered data
        transaction_counts = filtered_df['Import_Export'].value_counts()

        # Plot the pie chart for imports and exports
        st.markdown('## Percentage of Import and Export Transactions')  # Changed to markdown for title
        fig2, ax2 = plt.subplots(figsize=(3, 2))  # Adjusted size for better fit
        ax2.pie(transaction_counts, labels=transaction_counts.index, autopct='%1.1f%%', startangle=90, colors=['skyblue', 'lightgreen'])
        ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig2)

    with col2:
        # Count the occurrences of each payment mode in the filtered data
        payment_mode_counts = filtered_df['Payment_Terms'].value_counts()

        # Plot a horizontal bar chart for payment modes
        st.markdown('## Most Preferred Payment Modes')  # Changed to markdown for title
        fig1, ax1 = plt.subplots(figsize=(3, 2))  # Adjusted size for better fit
        colors = plt.cm.viridis(np.linspace(0, 1, len(payment_mode_counts)))
        payment_mode_counts.plot(kind='barh', color=colors, ax=ax1)

        # Add labels and title for payment modes
        ax1.set_title('Most Preferred Payment Modes', fontsize=10)
        ax1.set_xlabel('Number of Transactions', fontsize=10)
        ax1.set_ylabel('Payment Mode', fontsize=10)

        # Show the plot for payment modes
        st.pyplot(fig1)

    # Create the second row for the next two charts
    col3, col4 = st.columns(2)

    with col3:
        # Plot a stacked bar chart
        st.markdown('## Transactions by Category')  # Changed to markdown for title
        category_transaction_counts = filtered_df.groupby(['Category', 'Import_Export']).size().unstack()
        fig3, ax3 = plt.subplots(figsize=(3, 2))  # Adjusted size
        category_transaction_counts.plot(kind='bar', stacked=True, ax=ax3, color=['skyblue', 'lightgreen'])

        # Add labels and title for stacked bar chart
        ax3.set_title('Transactions by Category', fontsize=10)
        ax3.set_xlabel('Category', fontsize=10)
        ax3.set_ylabel('Number of Transactions', fontsize=10)
        ax3.legend(title='Transaction Type')

        # Show the plot for stacked bar chart
        st.pyplot(fig3)

    with col4:
        # Plot the line graph for average transaction value by month
        st.markdown('## Average Value of Transactions by Month')  # Changed to markdown for title
        filtered_df['Date'] = pd.to_datetime(filtered_df['Date'], format='%d-%m-%Y')
        filtered_df['Month'] = filtered_df['Date'].dt.month
        monthly_avg_value = filtered_df.groupby(['Month', 'Import_Export'])['Value'].mean().unstack()
        fig4, ax4 = plt.subplots(figsize=(3, 2))  # Adjusted size

        # Plot each import and export line
        for column in monthly_avg_value.columns:
            ax4.plot(monthly_avg_value.index, monthly_avg_value[column], marker='o', label=column)

        # Add labels and title for line graph
        ax4.set_title('Average Value of Transactions by Month', fontsize=10)
        ax4.set_xlabel('Month', fontsize=10)
        ax4.set_ylabel('Average Transaction Value', fontsize=10)
        ax4.grid(True)
        ax4.legend(title='Transaction Type')  # Add legend to distinguish between imports and exports

        # Show the plot for average transaction value
        st.pyplot(fig4)

    # Create a single column for the map below the charts
    st.markdown('## Total Import and Export Values by Country')
    # Group the data by country and import/export status from filtered data
    country_values = filtered_df.groupby(['Country', 'Import_Export'])['Value'].sum().reset_index()

    # Pivot the data for plotting
    country_values_pivot = country_values.pivot(index='Country', columns='Import_Export', values='Value').fillna(0)

    # Create a new column for total value
    country_values_pivot['Total'] = country_values_pivot.sum(axis=1)

    # Create a map chart
    fig5 = px.choropleth(country_values_pivot,
                          locations=country_values_pivot.index,
                          locationmode='country names',  # Use country names
                          color='Total',  # Color based on total value
                          hover_name=country_values_pivot.index,
                          color_continuous_scale=px.colors.sequential.Plasma,
                          labels={'Total': 'Total Value (in USD)'})

    # Update layout for larger size
    fig5.update_layout(width=1200, height=600)  # Adjust width and height as desired

    # Show the figure for choropleth map
    st.plotly_chart(fig5)

else:
    st.warning("No data available for the selected filters. Please select at least 1 item from each filter.")
