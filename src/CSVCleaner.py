import pandas as pd
import re
import json

class CSVCleaner:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = None
        self.dict = None
        self.filter = None

    def read_csv(self, encoding='utf-8'):
        """Read the CSV file."""
        self.df = pd.read_csv(self.file_path, encoding=encoding)

    def write(self, file_path):
        """Write the CSV file."""
        self.df.to_csv(file_path, index=False)
        
    def read_dict(self,file_name):
        """Return the dictionary."""
        with open(file_name, 'r', encoding='utf-8') as file:
            french_english_dict = json.load(file)
            self.dict = french_english_dict
            
    def read_filter(self, file_name):
        """Gets the filter of all the cities and regions in Belgium, Switzerland, Luxembourg and Canada that do and don't speak French"""
        with open(file_name, 'r', encoding='utf-8') as file:
            french_filter = json.load(file)
            self.filter = french_filter
        
    def normalize_column_headings(self):
        """Removes spaces and converts to lowercase the column headings."""
        self.df.columns = self.df.columns.str.lower().str.replace(' ', '_')


    def translate_column(self, column_name):
        """Translate the contents of a column using the stored dictionary."""
        if self.dict is not None and column_name in self.df.columns:
            self.df[column_name] = self.df[column_name].map(self.dict).fillna(self.df[column_name])
        else:
            if self.dict is None:
                print(f"Dictionary not loaded.")
            
            else: 
                print(f"Column '{column_name}' not found in DataFrame. Here are the columns: {self.df.columns}")
                
    def write_column_to_txt(self, column_name, output_file_path):
        """Write the unique contents of a specified column in alphabetical order to a text file."""
        if self.df is not None and column_name in self.df.columns:
            # Convert all items to strings and store unique items in a set
            unique_items = set(self.df[column_name].astype(str))

            # Sort the unique items alphabetically
            sorted_items = sorted(unique_items)

            with open(output_file_path, 'w', encoding='utf-8') as file:
                for item in sorted_items:
                    file.write(item + '\n')
        else:
            print(f"DataFrame is not loaded or column '{column_name}' not found.")


    def remove_non_french_speaking_regions(self, column_name):
        """Remove rows where the column content is in the 'no-french-regions' list."""
        if self.filter is not None and self.df is not None and column_name in self.df.columns:
            # Get the list of non-French speaking regions from the filter
            regions_to_remove = []
            for country in self.filter['countries']:
                regions_to_remove.extend(self.filter['countries'][country]['no-french-regions'])

            # Remove rows where the column content is in the regions_to_remove list
            self.df = self.df[~self.df[column_name].isin(regions_to_remove)]
        else:
            if self.filter is None:
                print("Filter not loaded.")
            elif self.df is None:
                print("DataFrame not loaded.")
            else:
                print(f"Column '{column_name}' not found in DataFrame.")
    
    def get_dataframe(self):
        """Return the dataframe."""
        return self.df
    






