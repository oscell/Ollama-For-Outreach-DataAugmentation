import requests
import json
import gradio as gr
import time
import pandas as pd
from CSVCleaner import CSVCleaner

# API URL and headers for the language model
url = "http://localhost:11434/api/generate"
headers = {'Content-Type': 'application/json'}

# Conversation history for the language model
conversation_history = []



csv_data = pd.read_csv("/mnt/c/Users/OEM/Desktop/Ollama-For-Outreach/data/clean/12k_VERIFIED_CLEAN.csv")

def select_column(records, gender):
    return records[records["gender"] == gender]

# Combined function for API call and slow echo
def combined_function(message, history):
    # Add the user prompt to the conversation history
    conversation_history.append(message)
    full_prompt = "\n".join(conversation_history)

    # Prepare the data for the API request
    data = {
        "model": "mistral",
        "stream": False,
        "prompt": full_prompt,
    }

    # Make the API call
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Process the response
    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        actual_response = data["response"]
        conversation_history.append(actual_response)

        # Echo back the conversation with delay
        combined_text = "\n".join(conversation_history)
        for i in range(len(combined_text)):
            time.sleep(0.05)
            yield "My guy: " + actual_response[: i+1]
    else:
        print("Error:", response.status_code, response.text)
        yield "Error in response from language model."



# Using gr.Blocks to create a custom layout
with gr.Blocks() as demo:
    with gr.Row():
        chat_box = gr.ChatInterface(combined_function).queue()
        
    with gr.Row():
            select_column,
    [
        gr.Dropdown(csv_data.columns.to_list(),label="Select the heading you want to edit"),
        gr.Dataframe(csv_data,column_widths="100px"),
        
    ],
        
    



if __name__ == "__main__":
    demo.launch()