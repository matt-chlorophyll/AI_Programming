import pandas as pd

# Sample ANZSIC codes and descriptions
sample_data = [
    {'ANSZIC Code': '0501', 'Description': 'Fishing'},
    {'ANSZIC Code': '0701', 'Description': 'Oil and Gas Extraction'},
    {'ANSZIC Code': '1001', 'Description': 'Meat Processing'},
    {'ANSZIC Code': '2001', 'Description': 'Pharmaceutical Manufacturing'},
    {'ANSZIC Code': '3001', 'Description': 'Residential Building Construction'}
]

# Create DataFrame
df = pd.DataFrame(sample_data)

# Save to Excel
df.to_excel('sample_input.xlsx', index=False)

print("Sample input file created: sample_input.xlsx")
print("This file contains 5 sample ANZSIC codes and descriptions for testing.") 