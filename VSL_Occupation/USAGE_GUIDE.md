# Occupation Risk Assessment Generator - Usage Guide

This guide provides step-by-step instructions on how to use the Occupation Risk Assessment Generator to generate risk assessment information for different occupations.

## Prerequisites

Before using the scripts, make sure you have:

1. Python 3.6 or higher installed
2. Required packages installed:
   ```bash
   pip install pandas openpyxl openai
   ```
3. An OpenAI API key (you can get one from [OpenAI's website](https://platform.openai.com/))

## Setting Up Your API Key

You can set up your OpenAI API key in one of two ways:

1. **Environment Variable (Recommended)**:
   ```bash
   # For Windows
   set OPENAI_API_KEY=your_api_key_here
   
   # For macOS/Linux
   export OPENAI_API_KEY=your_api_key_here
   ```

2. **Command Line Argument**:
   Pass your API key directly to the script using the `--api_key` argument (see examples below).

## Usage Scenarios

### Scenario 1: Generate Data for a Single Occupation (Manual Input)

If you want to generate data for a single occupation by manually entering the ANZSIC code and description:

```bash
python generate_occupation_data.py --output my_result.xlsx
```

The script will prompt you to enter:
- ANZSIC code (e.g., "0501")
- Description (e.g., "Fishing")

### Scenario 2: Generate Data for a Single Occupation (Using a Test Script)

You can use the provided test script to generate data for a predefined occupation (Hospitals):

```bash
python test_single_occupation.py
```

This will generate data for the "Hospitals" occupation and save it to `test_result.xlsx`.

### Scenario 3: Generate Data for Multiple Occupations (Using an Input File)

If you have an Excel file with multiple occupations:

```bash
python generate_occupation_data.py --input sample_input.xlsx --output generated_results.xlsx
```

The input file should have at least two columns:
- `ANSZIC Code`: The ANZSIC code for the occupation
- `Description`: The description of the occupation

You can create a sample input file using:

```bash
python sample_input.py
```

### Scenario 4: Batch Processing Multiple Input Files

If you have multiple input files, you can use the batch processing script:

1. Place all your input Excel files in the `input` directory
2. Run the batch processing script:
   ```bash
   python batch_process.py
   ```
3. The results will be saved in the `output` directory

You can customize the input and output directories:

```bash
python batch_process.py --input_dir my_inputs --output_dir my_results
```

## Advanced Options

### Changing the OpenAI Model

By default, the scripts use the `gpt-4` model. You can change this to `gpt-3.5-turbo` for faster, cheaper results:

```bash
python generate_occupation_data.py --model gpt-3.5-turbo
```

### Using a Different Sample File

If you have a different sample file with the desired format:

```bash
python generate_occupation_data.py --sample my_sample_file.xlsx
```

## Troubleshooting

### API Key Issues

If you get an error about the API key:
- Make sure your API key is correct
- Check that you've set the environment variable correctly or passed it as an argument

### Rate Limiting

If you encounter rate limiting issues:
- The scripts include delays between API calls to avoid rate limiting
- If you still encounter issues, you can modify the `time.sleep()` values in the code to increase the delays

### Missing Columns in Input File

If your input file is missing required columns:
- Make sure your input file has columns named exactly `ANSZIC Code` and `Description`
- If your columns have different names, you can modify the code to match your column names

## File Structure

- `generate_occupation_data.py`: Main script for generating occupation data
- `test_single_occupation.py`: Script for testing with a single occupation
- `sample_input.py`: Script for generating a sample input file
- `batch_process.py`: Script for batch processing multiple input files
- `analyze_format.py`: Script for analyzing the format of existing data
- `README.md`: Project overview and documentation
- `USAGE_GUIDE.md`: This usage guide

## Example Workflow

1. Create a sample input file:
   ```bash
   python sample_input.py
   ```

2. Generate data for the occupations in the sample file:
   ```bash
   python generate_occupation_data.py --input sample_input.xlsx --output results.xlsx
   ```

3. Review the results in `results.xlsx` 