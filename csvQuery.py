from openai import AzureOpenAI
from langchain.vectorstores import FAISS
#from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.embeddings import AzureOpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA  # Update as needed
import PyPDF2
import os
import openai
from langchain.chat_models import ChatOpenAI
from langchain.chat_models import AzureChatOpenAI
import psycopg2
from psycopg2 import sql
import csv
import os

GPT_4_API_KEY = ""
GPT_4_ENDPOINT = ""



GPT_4_ID = ''
ORGANIZATION = ""
GPT_4_API_BASE = ""
GPT_4_API_VERSION = ""


EmbeddingModelDeploymentName = ""
EmbeddingModelName = ""

os.environ["AZURE_OPENAI_API_KEY"] = GPT_4_API_KEY



client = AzureOpenAI(
    api_version=GPT_4_API_VERSION,
    azure_endpoint=GPT_4_API_BASE,
    
)

def ask_model(prompt):
    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt},
        ],
        model=GPT_4_ID  
    )
    return response


csv_file_path = "data\leetcode_questions.csv"
with open(csv_file_path, "r", newline="", encoding="utf-8") as csv_file:
    csv_reader = csv.reader(csv_file)
    data = list(csv_reader)


detected_text = ""
for row in data:
    detected_text += ",".join(row) + "\n"

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
texts = text_splitter.create_documents([detected_text])

directory = "index_store"
vector_index = FAISS.from_documents(texts, AzureOpenAIEmbeddings(
    azure_endpoint = GPT_4_API_BASE,
    deployment=EmbeddingModelDeploymentName,
    ))  
vector_index.save_local(directory)

vector_index = FAISS.load_local("index_store", AzureOpenAIEmbeddings(
    azure_endpoint = GPT_4_API_BASE,
    deployment=EmbeddingModelDeploymentName))  


retriever = vector_index.as_retriever(search_type="similarity", search_kwargs={"k": 6})



qa_interface = RetrievalQA.from_chain_type(
    llm=AzureChatOpenAI(openai_api_key=GPT_4_API_KEY,api_version=GPT_4_API_VERSION,base_url=GPT_4_API_BASE,azure_deployment=GPT_4_ID),
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

prompt = """

"""    





prompt1 = """
What is the highest amount of likes a question has??
""" 



# prompt2 = """
# I want you to consider the table which lists the details of all the corporate users.
# "Important for output" : I require the ouput as the json version of the table inside the <json></json> tags.
# Critical: The standard format of json I require
#           {
#                 "sectionname_tablename(please dont include any special characters except '_')":
#                 [{
#                 "column_name" : ["column_value"],
#                  all the rest of the values of that row
#                 },
#                 {
#                 Same process to be repeated for every row in that table
#                 }],         
#           }
# Very Important: 
#     a) Only display the output if there are values present in the table of the repective fields.
#     b) The table has 5 columns. Make sure to include all of them with the respective fields. Do not merge any of them.
# """       

# response = qa_interface(
#     prompt
# )

response1 = qa_interface(
    prompt1
)

# response2 = qa_interface(
#     prompt2
# )

# print(response["result"])
print(response1["result"])
# print(response2["result"])

