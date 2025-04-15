import pandas as pd
from openai import AzureOpenAI
import threading
import time
import os

csv_data = pd.read_csv("data\Global_YouTube_Statistics.csv")

os.environ["AZURE_OPENAI_API_KEY"] = ''

client = AzureOpenAI(
    api_version="",
    azure_endpoint=""
)

def process_query(query):
    prompt = query + "\n\n" + csv_data.to_string(index=False)

    function_descriptions = [
        {
            "name": "get_csv_summary",
            "description": "Generate a summary of the CSV data in 10 lines",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "Prompt to generate CSV summary in 10 lines"
                    }
                }
            }
        }
    ]
            
    response = client.chat.completions.create(
        model="gpt4turboindia",
        messages=[{"role": "user", "content": prompt}],
        functions=function_descriptions
    )

    if response.choices[0].message.function_call:
        function_call = response.choices[0].message.function_call
        function_name = function_call.name  

        if function_name == 'get_csv_summary':
            return function_call.text.strip()

    return "Could not process the query."

def send_request():
    query = "Generate a summary of the CSV data in 10 lines."

    output = process_query(query)

    print("Generated Output:", output)

if __name__ == '__main__':
    thread = threading.Thread(target=send_request)
    thread.start()

    thread.join()
