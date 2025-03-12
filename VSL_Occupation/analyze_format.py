import pandas as pd
import re
import statistics

def analyze_text_format(text):
    """
    Analyze the format of text to extract patterns.
    
    Args:
        text: Text to analyze
        
    Returns:
        Dictionary with analysis results
    """
    if not isinstance(text, str):
        return {
            'is_bulleted': False,
            'bullet_type': None,
            'avg_points': 0,
            'avg_words_per_point': 0,
            'sample': str(text)[:100]
        }
    
    # Check if text is bulleted
    lines = text.split('\n')
    bullet_pattern = re.compile(r'^\s*([\*\-•])\s')
    
    bullet_lines = [line for line in lines if bullet_pattern.match(line)]
    is_bulleted = len(bullet_lines) > 0
    
    if is_bulleted:
        # Determine bullet type
        bullet_types = [bullet_pattern.match(line).group(1) for line in bullet_lines]
        bullet_type = max(set(bullet_types), key=bullet_types.count)
        
        # Count number of bullet points
        num_points = len(bullet_lines)
        
        # Calculate average words per point
        words_per_point = [len(line.split()) for line in bullet_lines]
        avg_words = statistics.mean(words_per_point) if words_per_point else 0
        
        return {
            'is_bulleted': True,
            'bullet_type': bullet_type,
            'num_points': num_points,
            'avg_words_per_point': avg_words,
            'sample': bullet_lines[0] if bullet_lines else ""
        }
    else:
        return {
            'is_bulleted': False,
            'bullet_type': None,
            'num_points': 0,
            'avg_words_per_point': 0,
            'sample': text[:100] + "..." if len(text) > 100 else text
        }

def analyze_column_format(df, column_name):
    """
    Analyze the format of a column in the dataframe.
    
    Args:
        df: DataFrame to analyze
        column_name: Name of the column to analyze
        
    Returns:
        Dictionary with analysis results
    """
    if column_name not in df.columns:
        return {
            'column': column_name,
            'exists': False
        }
    
    # Get non-null values
    values = df[column_name].dropna().tolist()
    
    if not values:
        return {
            'column': column_name,
            'exists': True,
            'non_null_count': 0
        }
    
    # Analyze format of each value
    format_analyses = [analyze_text_format(value) for value in values]
    
    # Calculate statistics
    is_bulleted_count = sum(1 for analysis in format_analyses if analysis['is_bulleted'])
    bullet_types = [analysis['bullet_type'] for analysis in format_analyses if analysis['is_bulleted']]
    most_common_bullet = max(set(bullet_types), key=bullet_types.count) if bullet_types else None
    
    num_points = [analysis['num_points'] for analysis in format_analyses if analysis['is_bulleted']]
    avg_num_points = statistics.mean(num_points) if num_points else 0
    min_num_points = min(num_points) if num_points else 0
    max_num_points = max(num_points) if num_points else 0
    
    avg_words = [analysis['avg_words_per_point'] for analysis in format_analyses if analysis['is_bulleted']]
    avg_words_per_point = statistics.mean(avg_words) if avg_words else 0
    
    return {
        'column': column_name,
        'exists': True,
        'non_null_count': len(values),
        'bulleted_percentage': (is_bulleted_count / len(values)) * 100 if values else 0,
        'most_common_bullet': most_common_bullet,
        'avg_num_points': avg_num_points,
        'min_num_points': min_num_points,
        'max_num_points': max_num_points,
        'avg_words_per_point': avg_words_per_point,
        'sample': format_analyses[0]['sample'] if format_analyses else ""
    }

def main():
    # Read the Excel file
    file_path = "VSL Data for ChatGPT v2.xlsx"
    df = pd.read_excel(file_path)
    
    # Columns to analyze
    columns = ['Drivers', 'Significant Losses International', 'Significant Losses Australian']
    
    # Analyze each column
    for column in columns:
        analysis = analyze_column_format(df, column)
        
        print(f"\n=== ANALYSIS OF '{column}' ===")
        if not analysis['exists']:
            print(f"Column '{column}' does not exist in the dataframe.")
            continue
        
        print(f"Non-null values: {analysis['non_null_count']}")
        print(f"Percentage of bulleted entries: {analysis['bulleted_percentage']:.1f}%")
        
        if analysis['bulleted_percentage'] > 0:
            print(f"Most common bullet type: '{analysis['most_common_bullet']}'")
            print(f"Average number of bullet points: {analysis['avg_num_points']:.1f}")
            print(f"Range of bullet points: {analysis['min_num_points']} to {analysis['max_num_points']}")
            print(f"Average words per bullet point: {analysis['avg_words_per_point']:.1f}")
            print(f"Sample: {analysis['sample']}")

if __name__ == "__main__":
    main() 