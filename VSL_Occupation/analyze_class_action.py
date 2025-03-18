import pandas as pd

# Read the Excel file
file_path = "VSL Data for ChatGPT v2.xlsx"
df = pd.read_excel(file_path)

# Check if the Class Action Description column exists
if 'Class Action Description' in df.columns:
    # Get information about the column
    print("Class Action Description column exists in the file.")
    print(f"Number of non-null values: {df['Class Action Description'].count()}")
    print(f"Number of null values: {df['Class Action Description'].isnull().sum()}")
    
    # Show some examples
    non_null_examples = df[df['Class Action Description'].notnull()]
    if not non_null_examples.empty:
        print("\nExamples of non-null values:")
        for idx, row in non_null_examples.head(3).iterrows():
            print(f"\nANZSIC Code: {row['ANSZIC Code']}")
            print(f"Description: {row['Description']}")
            print(f"Class Action Description: {row['Class Action Description'][:300]}..." if len(str(row['Class Action Description'])) > 300 else f"Class Action Description: {row['Class Action Description']}")
    else:
        print("\nNo non-null examples found.")
else:
    print("Class Action Description column does not exist in the file.") 