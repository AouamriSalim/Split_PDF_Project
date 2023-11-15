import pandas as pd
import openpyxl
# Read the Excel file into a DataFrame
df = pd.read_excel('listemail.xlsx')

# Concatenate two rows into one row
df['Document Name'] = df['Nom'] + ' ' + df['Prenom']

# Drop the original rows
df = df.drop(['Nom', 'Prenom'], axis=1)

# Save the DataFrame to a new Excel file
df.to_excel('listemail2.xlsx', index=False)