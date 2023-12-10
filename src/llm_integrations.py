import requests
import json
import time
import pandas as pd
from CSVCleaner import CSVCleaner
import time
import re


class LLM_integrations:
    def __init__(self, file_path):
        # API URL and headers for the language model
        self.url = "http://localhost:11434/api/generate"
        self.headers = {'Content-Type': 'application/json'}

        # Conversation history for the language model
        self.conversation_history = []

    @staticmethod
    def find_column_headings(prompt,dataframe):
        # Use regular expression to find all occurrences of text within double curly brackets
        columns = re.findall(r"\{\{(.+?)\}\}", prompt)
        
        # Check for missing columns
        missing_columns = [column for column in columns if column not in dataframe.columns]
        
        if missing_columns:
            print("Error: The following columns do not exist in the dataframe: " + ", ".join(missing_columns))
            return
        
        ## Return columns that are column headings
        return [column for column in columns if column in dataframe.columns]
    
    @staticmethod
    def replace_with_df_columns(s, columns, df, row_number):
        for column in columns:
            # Ensure row_number is an integer or a list of integers
            s = s.replace(f"{{{{{column}}}}}", str(df[column].iloc[row_number]))
        return s


    def process_selection(selection, csv_data):
        # Filter the DataFrame based on the selected columns
        if selection:  # Check if any selection is made
            return csv_data[selection]
        else:
            return csv_data  # Return the full DataFrame if no selection

    @staticmethod
    def add_column(new_column_name, prompt, df,num_rows=None):
        """
        Adds a new column to a DataFrame with responses generated from an API call.
        The API call uses a prompt concatenated with contents from a specified column of the DataFrame.

        Parameters:
        input_column (str): The name of the column in the DataFrame to use for generating prompts.
        new_column_name (str): The name of the new column to be added to the DataFrame.
        prompt (str): The prompt to be concatenated with the input column's contents for the API call.
        df (DataFrame): The DataFrame to which the new column will be added.

        Returns:
        DataFrame: The original DataFrame with the new column added.
        """
        
        print(f"Running prompt: {prompt}")
        
        if new_column_name==[]:
            print("No name for the new column.")
            return df
        elif  prompt == []:
            print("provide a prompt!")
            return df
        
        column_headings = LLM_integrations.find_column_headings(prompt,df)
        
        
        
        responses = []
        
        # If num_rows is None or greater than the length of df, use the length of df
        num_rows_to_process = len(df) if num_rows is None else min(num_rows, len(df))

        df_subset = df.iloc[0:num_rows_to_process].copy()
        
        for i in range(num_rows_to_process):

            url = "http://localhost:11434/api/generate"
            headers = {'Content-Type': 'application/json'}
            
            data = {
                "model": "mistral",
                "stream": False,
                "prompt": LLM_integrations.replace_with_df_columns(prompt, column_headings,df,i),
            }
            

            try:
                response = requests.post(url, headers=headers, data=json.dumps(data), timeout=10)
                if response.status_code == 200:
                    responses.append(json.loads(response.text)["response"])
                else:
                    responses.append(f"Error: Received status code {response.status_code}")
            except requests.exceptions.RequestException as e:
                responses.append(f"Request failed: {e}")
            
            time.sleep(2)
        
        
        df_subset[new_column_name] = responses
        

        return df_subset
    
    # Combined function for API call and slow echo
    def llm_chat(message, history):
        # Add the user prompt to the conversation history
        self.conversation_history.append(message)
        full_prompt = "\n".join(self.conversation_history)

        # Prepare the data for the API request
        data = {
            "model": "mistral",
            "stream": False,
            "prompt": full_prompt,
        }

        # Make the API call
        response = requests.post(self.url, headers= self.headers, data=json.dumps(data))

        # Process the response
        if response.status_code == 200:
            response_text = response.text
            data = json.loads(response_text)
            actual_response = data["response"]
            self.conversation_history.append(actual_response)

            # Echo back the conversation with delay
            combined_text = "\n".join(self.conversation_history)
            for i in range(len(combined_text)):
                time.sleep(0.05)
                yield "My guy: " + actual_response[: i+1]
        else:
            print("Error:", response.status_code, response.text)
            yield "Error in response from language model."



