import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st  # Import Streamlit

# Optional: make the plots look nicer
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (10,6)

# Use the python engine and skip bad lines
df = pd.read_csv('World_population_messy.csv', engine='python', on_bad_lines='skip')

# 3. Quick look at the data
st.write("### Initial Data:")
st.write(df.head())
st.write("### Summary:")
st.write(df.info())

# 4. Remove duplicate rows
df = df.drop_duplicates()

# 5. Fix typos in Country names
df['Country'] = df['Country'].replace({'Chnia': 'China'})

# 6. Convert 'Population' column to numeric (force errors to NaN)
df['Population'] = pd.to_numeric(df['Population'], errors='coerce')

# 7. Handling Missing Values

# Fill missing Population (example: filling India population manually)
df.loc[df['Country'] == 'India', 'Population'] = 1420000000

# Fill missing Density (example: Density = Population / Area)
df['Density'] = df['Density'].fillna(df['Population'] / df['Area_km2'])

# Fill missing Area if you want (or drop rows where Area is missing)
df = df.dropna(subset=['Area_km2'])

# 8. Drop irrelevant columns
if 'Notes' in df.columns:
    df = df.drop(columns=['Notes'])

# 9. Final checks
st.write("### After Cleaning:")
st.write(df.head())
st.write("### Null values:")
st.write(df.isnull().sum())
st.write("### Summary:")
st.write(df.info())

# 10. Save the clean dataset
df.to_csv('world_population_cleaned.csv', index=False)
st.success("✅ Cleaned data saved as 'world_population_cleaned.csv'!")

# Plots (use st.pyplot instead of plt.show)
top_10 = df.sort_values(by='Population', ascending=False).head(10)
fig1, ax1 = plt.subplots()
sns.barplot(x='Population', y='Country', data=top_10, palette='viridis', ax=ax1)
ax1.set_title('Top 10 Most Populated Countries')
st.pyplot(fig1)

least_10 = df.sort_values(by='Population', ascending=True).head(10)
fig2, ax2 = plt.subplots()
sns.barplot(x='Population', y='Country', data=least_10, palette='rocket', ax=ax2)
ax2.set_title('Top 10 Least Populated Countries')
st.pyplot(fig2)

# Highest density
highest_density = df.sort_values(by='Density', ascending=False).head(10)
fig3, ax3 = plt.subplots()
sns.barplot(x='Density', y='Country', data=highest_density, palette='magma', ax=ax3)
ax3.set_title('Countries with Highest Population Density')
st.pyplot(fig3)

# Lowest density
lowest_density = df.sort_values(by='Density').head(10)
fig4, ax4 = plt.subplots()
sns.barplot(x='Density', y='Country', data=lowest_density, palette='coolwarm', ax=ax4)
ax4.set_title('Countries with Lowest Population Density')
st.pyplot(fig4)

# Highest growth
highest_growth = df.sort_values(by='Growth Rate %', ascending=False).head(10)
fig5, ax5 = plt.subplots()
sns.barplot(x='Growth Rate %', y='Country', data=highest_growth, palette='crest', ax=ax5)
ax5.set_title('Countries with Highest Growth Rate')
st.pyplot(fig5)

# Lowest growth
lowest_growth = df.sort_values(by='Growth Rate %').head(10)
fig6, ax6 = plt.subplots()
sns.barplot(x='Growth Rate %', y='Country', data=lowest_growth, palette='flare', ax=ax6)
ax6.set_title('Countries with Lowest Growth Rate')
st.pyplot(fig6)

# Distribution of Country Ranks
fig7, ax7 = plt.subplots()
sns.histplot(df['Rank'], bins=50, kde=True, color='blue', ax=ax7)
ax7.set_title('Country Rank Distribution')
ax7.set_xlabel('Rank')
ax7.set_ylabel('Count')
st.pyplot(fig7)

# Correlation Heatmap
corr = df.select_dtypes(include=[np.number]).corr()
fig8, ax8 = plt.subplots(figsize=(10,8))
sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax8)
ax8.set_title('Correlation Map')
st.pyplot(fig8)
