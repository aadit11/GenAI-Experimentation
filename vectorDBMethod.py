#from azure.ai.textanalytics import TextAnalyticsClient, AzureKeyCredential
#from azure.core.credentials import AzureKeyCredential
#from azure.ai.openai import OpenAIClient  
from openai import AzureOpenAI
from langchain.vectorstores import FAISS
#from langchain.embeddings.openai import OpenAIEmbeddings  
from langchain.embeddings import AzureOpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA  
import PyPDF2
import os
import openai
from langchain.chat_models import ChatOpenAI
from langchain.chat_models import AzureChatOpenAI


import os





# Set up Azure OpenAI credentials
GPT_4_API_KEY = ""
GPT_4_ENDPOINT = ""

# Set up Azure OpenAI credentials
# Embeddings_GPT_4_API_BASE = ""
# Embeddings_GPT_4_API_VERSION = ""
# Embeddings_GPT_4_API_KEY = ""
# Embeddings_GPT_4_ENDPOINT = ""


GPT_4_ID = ''
ORGANIZATION = ""
GPT_4_API_BASE = ""
GPT_4_API_VERSION = ""
# GPT_4_API_KEY = ""
# TEXT_EMBEDDING_002_DEPLOYMENT_NAME = ""
# GPT_4_ENDPOINT = ""


EmbeddingModelDeploymentName = ""
EmbeddingModelName = ""

os.environ["AZURE_OPENAI_API_KEY"] = GPT_4_API_KEY
# os.environ["AZURE_OPENAI_ENDPOINT"] = GPT_4_API_BASE


# openai.api_key = GPT_4_API_KEY


# Initialize Azure OpenAI client
#client = TextAnalyticsClient(endpoint=GPT_4_ENDPOINT, credential=AzureKeyCredential(GPT_4_API_KEY))
# client = OpenAIClient(endpoint=GPT_4_ENDPOINT, credential=AzureKeyCredential(GPT_4_API_KEY))
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
directory = "index_store"
vector_index.save_local(directory)

vector_index = FAISS.load_local(directory, AzureOpenAIEmbeddings(
    azure_endpoint=GPT_4_API_BASE,
    deployment=EmbeddingModelDeploymentName
))

retriever = vector_index.as_retriever(search_type="similarity", search_kwargs={"k": 6})
original_embeddings = text_splitter.create_documents([detected_text])

qa_interface = RetrievalQA.from_chain_type(
    llm=AzureChatOpenAI(openai_api_key=GPT_4_API_KEY,api_version=GPT_4_API_VERSION,base_url=GPT_4_API_BASE,azure_deployment=GPT_4_ID),
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

prompt = """
How many pages are there in the document
"""




response = qa_interface(
    prompt
)

print(response["result"])

total_vectors = len(original_embeddings)

print("Total number of vectors:", total_vectors)


index_to_retrieve = 10
if 0 <= index_to_retrieve < len(original_embeddings):
    specific_vector = original_embeddings[index_to_retrieve]
    print("Vector at Index", index_to_retrieve, ":", specific_vector)
else:
    print("Index", index_to_retrieve, "is out of bounds.")



