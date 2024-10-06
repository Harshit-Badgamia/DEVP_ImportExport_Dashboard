# app.py
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

# Import dataset
df = pd.read_csv(r"Imports_Exports_Dataset.csv")

# Random Sample from the dataset
df_sample = df.sample(n=3001, random_state=55011)

# Title of the dashboard
st.title("Imports and Exports Dashboard")

# Count the occurrences of each payment mode
payment_mode_counts = df_sample['Payment_Terms'].value_counts()

# Plot a horizontal bar chart for payment modes
st.subheader('Most Preferred Payment Modes')
fig1, ax1 = plt.subplots(figsize=(8, 6))
colors = plt.cm.viridis(np.linspace(0, 1, len(payment_mode_counts)))
payment_mode_counts.plot(kind='barh', color=colors, ax=ax1)

# Add labels and title for payment modes
ax1.set_title('Most Preferred Payment Modes')
ax1.set_xlabel('Number of Transactions')
ax1.set_ylabel('Payment Mode')

# Show the plot for payment modes
st.pyplot(fig1)

# Count the number of Import and Export transactions
transaction_counts = df_sample['Import_Export'].value_counts()

# Plot the pie chart for imports and exports
st.subheader('Percentage of Import and Export Transactions')
fig2, ax2 = plt.subplots()
ax2.pie(transaction_counts, labels=transaction_counts.index, autopct='%1.1f%%', startangle=90, colors=['skyblue', 'lightgreen'])
ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
st.pyplot(fig2)

# Group the data by Category and Import_Export, then count the number of transactions
category_transaction_counts = df_sample.groupby(['Category', 'Import_Export']).size().unstack()

# Plot a stacked bar chart
st.subheader('Transactions by Category (Stacked by Import/Export)')
fig3, ax3 = plt.subplots(figsize=(8, 6))
category_transaction_counts.plot(kind='bar', stacked=True, ax=ax3, color=['skyblue', 'lightgreen'])

# Add labels and title for stacked bar chart
ax3.set_title('Transactions by Category (Stacked by Import/Export)')
ax3.set_xlabel('Category')
ax3.set_ylabel('Number of Transactions')
ax3.legend(title='Transaction Type')

# Show the plot for stacked bar chart
st.pyplot(fig3)

# Convert 'Date' column to datetime format
df_sample['Date'] = pd.to_datetime(df_sample['Date'], format='%d-%m-%Y')

# Extract month from the date
df_sample['Month'] = df_sample['Date'].dt.month

# Group by month and Import_Export, then calculate the average transaction value
monthly_avg_value = df_sample.groupby(['Month', 'Import_Export'])['Value'].mean().unstack()

# Plot the line graph for average transaction value by month
st.subheader('Average Value of Transactions by Month')
fig4, ax4 = plt.subplots(figsize=(8, 6))

# Plot each import and export line
for column in monthly_avg_value.columns:
    ax4.plot(monthly_avg_value.index, monthly_avg_value[column], marker='o', label=column)

# Add labels and title for line graph
ax4.set_title('Average Value of Transactions by Month')
ax4.set_xlabel('Month')
ax4.set_ylabel('Average Transaction Value')
ax4.grid(True)
ax4.legend(title='Transaction Type')  # Add legend to distinguish between imports and exports

# Show the plot for average transaction value
st.pyplot(fig4)

# Group the data by country and import/export status
country_values = df_sample.groupby(['Country', 'Import_Export'])['Value'].sum().reset_index()

# Pivot the data for plotting
country_values_pivot = country_values.pivot(index='Country', columns='Import_Export', values='Value').fillna(0)

# Create a new column for total value
country_values_pivot['Total'] = country_values_pivot.sum(axis=1)

# Create a map chart
st.subheader('Total Import and Export Values by Country')
fig5 = px.choropleth(country_values_pivot,
                      locations=country_values_pivot.index,
                      locationmode='country names',  # Use country names
                      color='Total',  # Color based on total value
                      hover_name=country_values_pivot.index,
                      title='Total Import and Export Values by Country',
                      color_continuous_scale=px.colors.sequential.Plasma,
                      labels={'Total': 'Total Value (in USD)'})

# Update layout for larger size
fig5.update_layout(width=1200, height=800)  # Adjust the width and height as desired

# Show the figure for choropleth map
st.plotly_chart(fig5)
