import pandas as pd

def remove_rows_with_keywords(csv_file, keywords, output_file):
    """
    Reads a CSV file, removes rows containing any of the specified keywords in any column, 
    and saves the cleaned data to a new CSV file.
    
    :param csv_file: Path to the input CSV file.
    :param keywords: List of keywords to search for.
    :param output_file: Path to save the cleaned CSV file.
    """
    # Load the CSV file
    df = pd.read_csv(csv_file, dtype=str)  # Read as string to avoid conversion issues

    # Create a mask to filter out rows containing any of the keywords
    mask = df.apply(lambda row: row.astype(str).str.contains('|'.join(keywords), case=False, na=False), axis=1)

    # Remove rows where any column contains a keyword
    df_cleaned = df[~mask.any(axis=1)]

    # Save the cleaned CSV
    df_cleaned.to_csv(output_file, index=False)

    print(f"Rows containing {keywords} have been removed. Cleaned file saved as: {output_file}")

# Example usage
csv_file_path = "/Users/anthonythambiah/Downloads/cleaned_output.csv"  # Replace with your CSV file path
output_csv_path = "/Users/anthonythambiah/Downloads/cleaned_output_new.csv"  # Output file path
keywords_to_remove = ["montreal","Montréal","LaSalle","Saint-Léonard","Westmount","Mont-Royal","Outremont","Saint-Laurent","Anjou","Dollard-des-Ormeaux,","Pointe-aux-Trembles","Montréal-Nord","Brossard","Verdun","L'Île-Perrot","Pointe-Claire","Roxboro","Pierrefonds","Longueuil"]  # Keywords to remove

remove_rows_with_keywords(csv_file_path, keywords_to_remove, output_csv_path)