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


pdf_file_obj = open("data\file.pdf", "rb")
pdf_reader = PyPDF2.PdfReader(pdf_file_obj)
num_pages = len(pdf_reader.pages)
detected_text = ""

for page_num in range(num_pages):
    page_obj = pdf_reader.pages[page_num]
    detected_text += page_obj.extract_text() + "\n\n"

pdf_file_obj.close()

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
Analyze the attached document and provide a JSON structure listing the requirements
Critical:
    a)
    b)
Very Important:
    a) 
    b) 
    c) 
"""    



prompt1 = """
Analyze the attached document and provide a JSON structure listing the requirements
Critical:
    a)
    b)
Very Important:
    a) 
    b) 
    c) 
""" 



prompt2 = """
Give me a detailed explanation of the contents in a file.
"""       

response = qa_interface(
    prompt
)

response1 = qa_interface(
    prompt1
)

response2 = qa_interface(
    prompt2
)

print(response["result"])
print(response1["result"])
print(response2["result"])


