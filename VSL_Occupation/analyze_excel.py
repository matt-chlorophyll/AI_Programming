import pandas as pd
import re

# Read the Excel file
file_path = "VSL Data for ChatGPT v2.xlsx"
df = pd.read_excel(file_path)

# Display basic information about the dataframe
print("DataFrame shape:", df.shape)
print("\nColumns:", df.columns.tolist())

# Check for any missing values
print("\nMissing values per column:")
print(df.isnull().sum())

# Print a sample row with all columns
print("\nSample row (first row):")
sample_row = df.iloc[0]
for col, value in sample_row.items():
    print(f"\n{col}:")
    if isinstance(value, str):
        # Print first 300 characters
        print(value[:300] + "..." if len(value) > 300 else value)
    else:
        print(value)

# Check if the text in these columns follows a bullet point format
def check_bullet_format(text):
    if isinstance(text, str):
        # Check if text starts with bullet points (*, -, •, etc.)
        lines = text.split('\n')
        for line in lines:
            if line.strip() and not re.match(r'^\s*[\*\-•]\s', line):
                return False
        return True
    return False

print("\nChecking bullet point format:")
for col in ['Drivers', 'Significant Losses International', 'Significant Losses Australian']:
    if col in df.columns:
        has_bullets = df[col].dropna().apply(check_bullet_format).mean() * 100
        print(f"{col}: {has_bullets:.1f}% of entries use bullet points") 