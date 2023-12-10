from CSVCleaner import CSVCleaner
from llm_integrations import LLM_integrations as llm
import gradio as gr
from algolia_integration import algolia_integration as algolia
import pandas as pd

cleaner = CSVCleaner(r'/mnt/c/Users/OEM/Desktop/Ollama-For-Outreach/data/raw/12k_VERIFIED_RAW.csv')


cleaner.clean()


cleaner.write('data/clean/12k_VERIFIED_CLEAN.csv')

csv_data = cleaner.df

algolia = algolia(csv_data) 


# Global list to store data history
data_history = [csv_data]

def update_data_history(new_column_name, prompt, data):
    # Store current state of data in history
    data_history.append(data.copy())

    # Perform the add_column operation
    return llm.add_column(new_column_name, prompt, data)

def algolia_search(search_term):
    # Perform the search
    results = algolia.index.search(search_term)
    # Convert results to a DataFrame
    return pd.DataFrame(results['hits'])

def update_dataframe(search_term):
    # Get search results
    search_results = algolia_search(search_term)
    # Return the results to update the DataFrame
    return search_results

def preview_run(new_column_name, prompt, data):

    # Perform the add_column operation
    return llm.add_column(new_column_name, prompt, data,num_rows=5)

def undo_last_change():
    if data_history:
        # Revert to the last state in the history
        return data_history.pop()
    else:
        # No history to revert to
        return gr.Dataframe() 

def save():
    csv_data.to_csv('data/clean/12k_VERIFIED_AUGM.csv', index=False)

# Initialize an empty DataFrame component
# dataframe_component_serach_results = gr.Dataframe()

# Using gr.Blocks to create a custom layout
with gr.Blocks() as demo:
    
    gr.Markdown("# Data Augmentation using LLMs")
    
    with gr.Row():
        # Create a textbox for search
        search_box = gr.Textbox(label="What are you looking for?", placeholder="Enter search term...")
        # Link the textbox to update the DataFrame
        

    with gr.Row():
        # Place the DataFrame component below the search box
        dataframe_component_serach_results = gr.Dataframe()
        
        search_box.change(fn=update_dataframe, inputs=search_box, outputs=dataframe_component_serach_results)

    
    gr.Markdown("## Data Augmentation")
    gr.Markdown('This prompt will add a new column to the data frame. given the inputs of other columns.\n **e.g. "Write a short fgreeting for {{first_name}} {{last_name}}."** will make a new column that wil greet the person using their fist and last name.')
    
    with gr.Row():
        prompt = gr.Textbox(label="What prompt do you want to use?")
     
    with gr.Row():
        new_column_name = gr.Textbox(label="Title of the new comlumn")

    
    with gr.Row():
        save_button = gr.Button("Save")
        undo_button = gr.Button("Undo")    

    
    with gr.Row():
        run_button = gr.Button("Run")
        

        preview_run_button = gr.Button("Preview Run")
          
    
    
    gr.Markdown("### Preview")  
    with gr.Row():
        # Initialize an empty DataFrame component
        preview_data = gr.Dataframe()
        
 
        
    

    gr.Markdown("### Further inspection")
    gr.Markdown("You can use this to inspect the data, only selecting certain rows.")
    with gr.Row():
        dropdown = gr.Dropdown(
            label="Select Columns", 
            choices=csv_data.columns.to_list(), 
            multiselect=True, 
            type="value",
        )

    with gr.Row():
        # Initialize an empty DataFrame component
        dataframe_component = gr.Dataframe()

        # Link the dropdown to update the DataFrame
        dropdown.change(
            fn=lambda selection: llm.process_selection(selection, csv_data),
            inputs=dropdown,
            outputs=dataframe_component
        )
        
    gr.Markdown("## Full Raw data")
    with gr.Accordion("We full raw data"):
        data = gr.Dataframe(csv_data)
        
        save_button.click(save)
        undo_button.click(undo_last_change, inputs=[], outputs=[data])
        run_button.click(update_data_history, inputs=[new_column_name, prompt, data], outputs=[data])
        preview_run_button.click(preview_run, inputs=[new_column_name, prompt, data], outputs=[preview_data]) 
        
        


    



if __name__ == "__main__":
    demo.launch()