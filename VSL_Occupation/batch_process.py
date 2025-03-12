import os
import argparse
import pandas as pd
import glob
from datetime import datetime
from generate_occupation_data import OccupationDataGenerator

def batch_process(input_dir, output_dir, api_key, model='gpt-4', sample_file='VSL Data for ChatGPT v2.xlsx'):
    """
    Process all Excel files in the input directory and save results to the output directory.
    
    Args:
        input_dir: Directory containing input Excel files
        output_dir: Directory to save output Excel files
        api_key: OpenAI API key
        model: OpenAI model to use
        sample_file: Path to sample data file for reference
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize generator
    generator = OccupationDataGenerator(
        api_key=api_key,
        model=model,
        sample_file=sample_file
    )
    
    # Get all Excel files in the input directory
    input_files = glob.glob(os.path.join(input_dir, '*.xlsx'))
    
    if not input_files:
        print(f"No Excel files found in {input_dir}")
        return
    
    print(f"Found {len(input_files)} Excel files to process")
    
    # Process each file
    for input_file in input_files:
        file_name = os.path.basename(input_file)
        print(f"\nProcessing {file_name}...")
        
        try:
            # Read input data
            input_data = pd.read_excel(input_file)
            
            # Check if input data has required columns
            required_columns = ['ANSZIC Code', 'Description']
            missing_columns = [col for col in required_columns if col not in input_data.columns]
            if missing_columns:
                print(f"Skipping {file_name}: Missing required columns: {', '.join(missing_columns)}")
                continue
            
            # Process input data
            result_df = generator.process_input_data(input_data)
            
            # Generate output file name
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = os.path.join(output_dir, f"processed_{os.path.splitext(file_name)[0]}_{timestamp}.xlsx")
            
            # Save results to Excel
            result_df.to_excel(output_file, index=False)
            print(f"Results saved to {output_file}")
            
        except Exception as e:
            print(f"Error processing {file_name}: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Batch process multiple input files using OpenAI API')
    parser.add_argument('--input_dir', type=str, help='Directory containing input Excel files', default='input')
    parser.add_argument('--output_dir', type=str, help='Directory to save output Excel files', default='output')
    parser.add_argument('--api_key', type=str, help='OpenAI API key', default=None)
    parser.add_argument('--model', type=str, help='OpenAI model to use', default='gpt-4')
    parser.add_argument('--sample', type=str, help='Path to sample data file for reference', default='VSL Data for ChatGPT v2.xlsx')
    
    args = parser.parse_args()
    
    # Get API key from arguments or environment variable
    api_key = args.api_key or os.environ.get('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OpenAI API key must be provided via --api_key argument or OPENAI_API_KEY environment variable")
    
    # Process files
    batch_process(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        api_key=api_key,
        model=args.model,
        sample_file=args.sample
    )

if __name__ == "__main__":
    main() 