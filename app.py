import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Optional: make the plots look nicer
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (10,6)


# Use the python engine and skip bad lines
df = pd.read_csv('World_population_messy.csv', engine='python', on_bad_lines='skip')

# 3. Quick look at the data
print("Initial Data:")
print(df.head())
print("\nSummary:\n", df.info())

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
print("\nAfter Cleaning:")
print(df.head())
print("\nNull values:\n", df.isnull().sum())
print("\nSummary:\n", df.info())


# 10. Save the clean dataset
df.to_csv('world_population_cleaned.csv', index=False)
print("\n✅ Cleaned data saved as 'world_population_cleaned.csv'!")


top_10 = df.sort_values(by='Population', ascending=False).head(10)

sns.barplot(x='Population', y='Country', data=top_10, palette='viridis')
plt.title('Top 10 Most Populated Countries')
plt.xlabel('Population')
plt.ylabel('Country')
plt.show()

least_10 = df.sort_values(by='Population', ascending=True).head(10)

sns.barplot(x='Population', y='Country', data=least_10, palette='rocket')
plt.title('Top 10 Least Populated Countries')
plt.xlabel('Population')
plt.ylabel('Country')
plt.show()

# Highest density
highest_density = df.sort_values(by='Density', ascending=False).head(10)
sns.barplot(x='Density', y='Country', data=highest_density, palette='magma')
plt.title('Countries with Highest Population Density')
plt.show()

# Lowest density
lowest_density = df.sort_values(by='Density').head(10)
sns.barplot(x='Density', y='Country', data=lowest_density, palette='coolwarm')
plt.title('Countries with Lowest Population Density')
plt.show()

# Highest growth
highest_growth = df.sort_values(by='Growth Rate %', ascending=False).head(10)
sns.barplot(x='Growth Rate %', y='Country', data=highest_growth, palette='crest')
plt.title('Countries with Highest Growth Rate')
plt.show()

# Lowest growth
lowest_growth = df.sort_values(by='Growth Rate %').head(10)
sns.barplot(x='Growth Rate %', y='Country', data=lowest_growth, palette='flare')
plt.title('Countries with Lowest Growth Rate')
plt.show()

sns.histplot(df['Rank'], bins=50, kde=True, color='blue')
plt.title('Country Rank Distribution')
plt.xlabel('Rank')
plt.ylabel('Count')
plt.show()

# Only take numeric columns
corr = df.select_dtypes(include=[np.number]).corr()

# Heatmap
plt.figure(figsize=(10,8))
sns.heatmap(corr, annot=True, cmap='coolwarm')
plt.title('Correlation Map')
plt.show()