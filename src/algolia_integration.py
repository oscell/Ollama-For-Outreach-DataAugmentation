from os import getenv
import pandas as pd

# Install the API client: https://www.algolia.com/doc/api-client/getting-started/install/python/?client=python
from algoliasearch.search_client import SearchClient
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Get your Algolia Application ID and (admin) API key from the dashboard: https://www.algolia.com/account/api-keys
# and choose a name for your index. Add these environment variables to a `.env` file:
ALGOLIA_APP_ID = getenv('ALGOLIA_APP_ID')
ALGOLIA_API_KEY = getenv('ALGOLIA_API_KEY')
ALGOLIA_INDEX_NAME = getenv('ALGOLIA_INDEX_NAME')

# Start the API client
# https://www.algolia.com/doc/api-client/getting-started/instantiate-client-index/
client = SearchClient.create(ALGOLIA_APP_ID, ALGOLIA_API_KEY)

# Create an index (or connect to it, if an index with the name `ALGOLIA_INDEX_NAME` already exists)
# https://www.algolia.com/doc/api-client/getting-started/instantiate-client-index/#initialize-an-index
index = client.init_index(ALGOLIA_INDEX_NAME)

# Add new objects to the index
# https://www.algolia.com/doc/api-reference/api-methods/add-objects/



class algolia_integration:
    def __init__(self, df):
        self.df = df
        self.index = index


    def create_index(self):
        df = self.df.fillna("")
        # Initialize an empty list to store JSON objects
        json_objects = []

        # Iterate over each row in the DataFrame
        for i, row in df.iterrows():
            # Construct the JSON object for each row
            json_object = {
                'objectID': i,
                df.columns.to_list()[0]: row[df.columns.to_list()[0]],
                df.columns.to_list()[1]: row[df.columns.to_list()[1]],
                df.columns.to_list()[2]: row[df.columns.to_list()[2]],
                df.columns.to_list()[3]: row[df.columns.to_list()[3]],
                df.columns.to_list()[4]: row[df.columns.to_list()[4]],
                df.columns.to_list()[5]: row[df.columns.to_list()[5]],
                df.columns.to_list()[6]: row[df.columns.to_list()[6]],
                df.columns.to_list()[7]: row[df.columns.to_list()[7]],
                df.columns.to_list()[8]: row[df.columns.to_list()[8]],
                df.columns.to_list()[9]: row[df.columns.to_list()[9]],
                df.columns.to_list()[10]: row[df.columns.to_list()[10]],
                df.columns.to_list()[11]: row[df.columns.to_list()[11]],
                df.columns.to_list()[12]: row[df.columns.to_list()[12]],
            }
            # Add the JSON object to the list
            
            json_objects.append(json_object)


        res = index.save_objects(json_objects)

        # Wait for the indexing task to complete
        # https://www.algolia.com/doc/api-reference/api-methods/wait-task/
        res.wait()
        return index

    # # Search the index for "Fo"
    # # https://www.algolia.com/doc/api-reference/api-methods/search/
    