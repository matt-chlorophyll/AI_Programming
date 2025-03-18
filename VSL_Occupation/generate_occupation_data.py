import pandas as pd
import openai
import time
import os
import argparse
from typing import List, Dict, Any, Tuple

# Set up argument parser
parser = argparse.ArgumentParser(description='Generate occupation data using OpenAI API')
parser.add_argument('--input', type=str, help='Path to input Excel file with ANZSIC codes and descriptions', default=None)
parser.add_argument('--output', type=str, help='Path to output Excel file', default='generated_occupation_data.xlsx')
parser.add_argument('--api_key', type=str, help='OpenAI API key', default=None)
parser.add_argument('--model', type=str, help='OpenAI model to use', default='gpt-4o')
parser.add_argument('--sample', type=str, help='Path to sample data file for reference', default='VSL Data for ChatGPT v2.xlsx')

class OccupationDataGenerator:
    def __init__(self, api_key: str, model: str = 'gpt-4', sample_file: str = 'VSL Data for ChatGPT v2.xlsx'):
        """
        Initialize the OccupationDataGenerator.
        
        Args:
            api_key: OpenAI API key
            model: OpenAI model to use
            sample_file: Path to sample data file for reference
        """
        self.api_key = api_key
        self.model = model
        self.client = openai.OpenAI(api_key=api_key)
        
        # Load sample data for reference
        self.sample_data = pd.read_excel(sample_file)
        
        # Extract sample entries for prompting
        self.sample_drivers = self.sample_data['Drivers'].iloc[0]
        self.sample_intl_losses = self.sample_data['Significant Losses International'].iloc[0]
        self.sample_aus_losses = self.sample_data['Significant Losses Australian'].iloc[0]
        
        # Check if Class Action Description column exists and extract sample if available
        self.has_class_action_column = 'Class Action Description' in self.sample_data.columns
        self.sample_class_action = None
        
        if self.has_class_action_column:
            # Find a non-null example for Class Action Description
            non_null_examples = self.sample_data[self.sample_data['Class Action Description'].notnull()]
            if not non_null_examples.empty:
                self.sample_class_action = non_null_examples['Class Action Description'].iloc[0]
        
        # Format analysis results (based on analyze_format.py)
        self.format_info = {
            'Drivers': {
                'bullet_type': '*',
                'avg_num_points': 6.6,
                'range_points': (5, 10),
                'avg_words_per_point': 21.8
            },
            'Significant Losses International': {
                'bullet_type': '*',
                'avg_num_points': 3.0,
                'range_points': (1, 5),
                'avg_words_per_point': 30.8
            },
            'Significant Losses Australian': {
                'bullet_type': '*',
                'avg_num_points': 2.4,
                'range_points': (2, 5),
                'avg_words_per_point': 31.5
            }
        }
    
    def generate_drivers(self, anzsic_code: str, description: str) -> str:
        """
        Generate drivers of claims for a given occupation.
        
        Args:
            anzsic_code: ANZSIC code
            description: Occupation description
            
        Returns:
            Generated drivers text
        """
        format_info = self.format_info['Drivers']
        
        prompt = f"""
        You are an expert in corporate liability insurance risk assessment. I need you to generate a list of drivers of claims for the following occupation:
        
        ANZSIC Code: {anzsic_code}
        Description: {description}
        
        Please provide a comprehensive list of potential drivers of claims for this occupation. Format your response as a bulleted list with each point starting with an asterisk (*).
        Limit the response to 5 bullet points.
        
        Here's an example of the format I'm looking for:
        
        {self.sample_drivers}
        
        Format requirements:
        - Each bullet point should start with an asterisk (*)
        - Include between {format_info['range_points'][0]} and {format_info['range_points'][1]} bullet points (aim for about {format_info['avg_num_points']:.1f})
        - Each bullet point should be detailed and specific, with around {format_info['avg_words_per_point']:.1f} words per point
        - Focus on the specific risks and liability exposures associated with this occupation
        - Each point should be a complete thought, often with a cause-and-effect relationship
        - Use a colon after the main risk category, followed by an explanation
        
        Focus on the specific risks and liability exposures associated with this occupation. Be detailed and specific.
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": "You are an expert in corporate liability insurance risk assessment."},
                      {"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content.strip()
    
    def generate_international_losses(self, anzsic_code: str, description: str) -> str:
        """
        Generate significant international losses for a given occupation.
        
        Args:
            anzsic_code: ANZSIC code
            description: Occupation description
            
        Returns:
            Generated international losses text
        """
        format_info = self.format_info['Significant Losses International']
        
        prompt = f"""
        You are an expert in corporate liability insurance risk assessment. I need you to generate a list of significant international losses for the following occupation:
        
        ANZSIC Code: {anzsic_code}
        Description: {description}
        
        Please provide examples of significant international losses related to this occupation. Format your response as a bulleted list with each point starting with an asterisk (*).
        
        Here's an example of the format I'm looking for:
        
        {self.sample_intl_losses}
        
        Format requirements:
        - Each bullet point should start with an asterisk (*)
        - Include between {format_info['range_points'][0]} and {format_info['range_points'][1]} bullet points (aim for about {format_info['avg_num_points']:.1f})
        - Each bullet point should be detailed with around {format_info['avg_words_per_point']:.1f} words per point
        - Each example should start with the location and year in parentheses, e.g., "(USA 2010)"
        - After the location and year, include a brief title of the incident, followed by a colon
        - Then provide details about the incident and its liability implications
        
        Each example should include:
        - Location and year in parentheses at the start of each point
        - Brief description of the incident
        - Information about liability implications and costs if available
        
        Focus on real, notable cases from around the world (excluding Australia).
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": "You are an expert in corporate liability insurance risk assessment."},
                      {"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content.strip()
    
    def generate_australian_losses(self, anzsic_code: str, description: str) -> str:
        """
        Generate significant Australian losses for a given occupation.
        
        Args:
            anzsic_code: ANZSIC code
            description: Occupation description
            
        Returns:
            Generated Australian losses text
        """
        format_info = self.format_info['Significant Losses Australian']
        
        prompt = f"""
        You are an expert in corporate liability insurance risk assessment. I need you to generate a list of significant Australian losses for the following occupation:
        
        ANZSIC Code: {anzsic_code}
        Description: {description}
        
        Please provide examples of significant Australian losses related to this occupation. Format your response as a bulleted list with each point starting with an asterisk (*).
        
        Here's an example of the format I'm looking for:
        
        {self.sample_aus_losses}
        
        Format requirements:
        - Each bullet point should start with an asterisk (*)
        - Include between {format_info['range_points'][0]} and {format_info['range_points'][1]} bullet points (aim for about {format_info['avg_num_points']:.1f})
        - Each bullet point should be detailed with around {format_info['avg_words_per_point']:.1f} words per point
        - Each example should start with the location in Australia and year in parentheses, e.g., "(Victoria 2010)"
        - After the location and year, include a brief title of the incident, followed by a colon
        - Then provide details about the incident and its liability implications
        
        Each example should include:
        - Location in Australia and year in parentheses at the start of each point
        - Brief description of the incident
        - Information about liability implications and costs if available
        
        Focus on real, notable cases from Australia only.
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": "You are an expert in corporate liability insurance risk assessment."},
                      {"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content.strip()
    
    def generate_class_action_description(self, anzsic_code: str, description: str) -> str:
        """
        Generate class action description for a given occupation in Australia.
        If no relevant class action information is found, return an empty string.
        
        Args:
            anzsic_code: ANZSIC code
            description: Occupation description
            
        Returns:
            Generated class action description or empty string if none found
        """
        # If sample class action is not available, use a generic example
        sample_text = self.sample_class_action if self.sample_class_action else "* [Law Firm] has filed a class action lawsuit against [Company]. The class action is on behalf of [affected group]. The class action alleges that [allegations]. The case seeks [damages/compensation] for [specific harms]."
        print(sample_text)
        
        prompt = f"""
        You are an expert in corporate liability insurance risk assessment, specifically focused on class actions in Australia. 
        I need you to provide information about class actions in Australia related to the following occupation:
        
        ANZSIC Code: {anzsic_code}
        Description: {description}
        
        Provide details of any known class actions in Australia related to this occupation. Format your response as a bulleted list with each point starting with an asterisk (*).
        
        Here's an example of the format I'm looking for:
        
        {sample_text}
        
        Format requirements:
        - Each class action should be its own bullet point starting with an asterisk (*)
        - Include information about the law firm filing the action, the company/entity being sued, the affected group, allegations, and sought damages
        - Focus on Australian class actions only
        - Be specific and detailed about the class action, including names of firms, companies, and allegations when possible
        
        IMPORTANT: If you cannot find any relevant class action information for this occupation in Australia, return ONLY the text "NO_CLASS_ACTION_FOUND" with no other text or explanation. Do not make up or fabricate class actions if none exist.
        """
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": "You are an expert in corporate liability insurance risk assessment, specifically focused on class actions in Australia."},
                      {"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000
        )
        
        result = response.choices[0].message.content.strip()
        
        # Check if the model couldn't find any class action information
        if "NO_CLASS_ACTION_FOUND" in result:
            return ""
        
        return result
    
    def generate_all_data(self, anzsic_code: str, description: str) -> Dict[str, str]:
        """
        Generate all data for a given occupation.
        
        Args:
            anzsic_code: ANZSIC code
            description: Occupation description
            
        Returns:
            Dictionary with generated data
        """
        print(f"Generating data for {description} (ANZSIC: {anzsic_code})...")
        
        drivers = self.generate_drivers(anzsic_code, description)
        print("  ✓ Drivers generated")
        
        # Add a small delay to avoid rate limiting
        time.sleep(1)
        
        intl_losses = self.generate_international_losses(anzsic_code, description)
        print("  ✓ International losses generated")
        
        # Add a small delay to avoid rate limiting
        time.sleep(1)
        
        aus_losses = self.generate_australian_losses(anzsic_code, description)
        print("  ✓ Australian losses generated")
        
        result = {
            'ANSZIC Code': anzsic_code,
            'Description': description,
            'Drivers': drivers,
            'Significant Losses International': intl_losses,
            'Significant Losses Australian': aus_losses
        }
        
        # Generate class action description if the sample file has that column
        if self.has_class_action_column:
            # Add a small delay to avoid rate limiting
            time.sleep(1)
            
            class_action = self.generate_class_action_description(anzsic_code, description)
            print("  ✓ Class action description generated")
            result['Class Action Description'] = class_action
        
        return result
    
    def process_input_data(self, input_data: pd.DataFrame) -> pd.DataFrame:
        """
        Process input data and generate all required information.
        
        Args:
            input_data: DataFrame with ANZSIC codes and descriptions
            
        Returns:
            DataFrame with generated data
        """
        results = []
        
        for _, row in input_data.iterrows():
            anzsic_code = str(row['ANSZIC Code'])
            description = row['Description']
            
            try:
                result = self.generate_all_data(anzsic_code, description)
                results.append(result)
                print(f"Completed {description}\n")
                
                # Add a delay between processing different occupations
                time.sleep(2)
                
            except Exception as e:
                print(f"Error processing {description}: {str(e)}")
                # Add partial result if available
                partial_result = {
                    'ANSZIC Code': anzsic_code,
                    'Description': description,
                    'Drivers': "Error: " + str(e),
                    'Significant Losses International': "",
                    'Significant Losses Australian': ""
                }
                if self.has_class_action_column:
                    partial_result['Class Action Description'] = ""
                results.append(partial_result)
        
        return pd.DataFrame(results)

def main():
    args = parser.parse_args()
    
    # Get API key from arguments or environment variable
    api_key = args.api_key or os.environ.get('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OpenAI API key must be provided via --api_key argument or OPENAI_API_KEY environment variable")
    
    # Initialize generator
    generator = OccupationDataGenerator(
        api_key=api_key,
        model=args.model,
        sample_file=args.sample
    )
    
    # Process input data
    if args.input:
        # Read input data from file
        input_data = pd.read_excel(args.input)
        
        # Check if input data has required columns
        required_columns = ['ANSZIC Code', 'Description']
        missing_columns = [col for col in required_columns if col not in input_data.columns]
        if missing_columns:
            raise ValueError(f"Input file is missing required columns: {', '.join(missing_columns)}")
        
        # Process input data
        result_df = generator.process_input_data(input_data)
        
    else:
        # If no input file is provided, ask for manual input
        print("No input file provided. Please enter ANZSIC code and description manually.")
        anzsic_code = input("ANZSIC code: ")
        description = input("Description: ")
        
        # Generate data for the single entry
        result = generator.generate_all_data(anzsic_code, description)
        result_df = pd.DataFrame([result])
    
    # Save results to Excel
    result_df.to_excel(args.output, index=False)
    print(f"Results saved to {args.output}")

if __name__ == "__main__":
    main() 