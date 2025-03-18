import os
import pandas as pd
from generate_occupation_data import OccupationDataGenerator

def test_single_occupation():
    """
    Test the OccupationDataGenerator with a single occupation.
    This is a simple example of how to use the generator programmatically.
    """
    # Get API key from environment variable
    api_key = os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set.")
        print("Please set your OpenAI API key as an environment variable:")
        print("  set OPENAI_API_KEY=your_api_key_here  # Windows")
        print("  export OPENAI_API_KEY=your_api_key_here  # macOS/Linux")
        return
    
    # Initialize the generator
    generator = OccupationDataGenerator(
        api_key=api_key,
        model='gpt-4',  # You can change this to 'gpt-3.5-turbo' for faster, cheaper results
        sample_file='VSL Data for ChatGPT v2.xlsx'
    )
    
    # Define a test occupation
    anzsic_code = '8401'
    description = 'Hospitals'
    
    print(f"Testing with occupation: {description} (ANZSIC: {anzsic_code})")
    print("This will make multiple API calls to OpenAI. Please wait...")
    
    # Generate data for the occupation
    result = generator.generate_all_data(anzsic_code, description)
    
    # Print the results
    print("\n=== RESULTS ===\n")
    
    print("DRIVERS:")
    print(result['Drivers'])
    
    print("\nSIGNIFICANT LOSSES INTERNATIONAL:")
    print(result['Significant Losses International'])
    
    print("\nSIGNIFICANT LOSSES AUSTRALIAN:")
    print(result['Significant Losses Australian'])
    
    # Print class action description if available
    if 'Class Action Description' in result:
        print("\nCLASS ACTION DESCRIPTION:")
        if result['Class Action Description']:
            print(result['Class Action Description'])
        else:
            print("No class action information found for this occupation.")
    
    # Save to Excel (optional)
    df = pd.DataFrame([result])
    output_file = 'test_result.xlsx'
    df.to_excel(output_file, index=False)
    print(f"\nResults also saved to {output_file}")

if __name__ == "__main__":
    test_single_occupation() 