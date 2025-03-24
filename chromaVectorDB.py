import PyPDF2
from langchain.vectorstores import Chroma
from langchain.embeddings import AzureOpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.chat_models import AzureChatOpenAI
import os

# Set up Azure OpenAI credentials
GPT_4_API_KEY = ""
GPT_4_ENDPOINT = ""

GPT_4_ID = ''
ORGANIZATION = ""
GPT_4_API_BASE = ""
GPT_4_API_VERSION = ""

EmbeddingModelDeploymentName = ""

os.environ["AZURE_OPENAI_API_KEY"] = GPT_4_API_KEY

# Initialize Azure OpenAI client
client = AzureChatOpenAI(
    openai_api_key=GPT_4_API_KEY,
    api_version=GPT_4_API_VERSION,
    base_url=GPT_4_API_BASE,
    azure_deployment=GPT_4_ID
)

def ask_model(prompt):
    response = client.chat.completions.create(
        messages=[
            {"role": "user", "content": prompt},
        ],
        model=GPT_4_ID
    )
    return response

# Your existing code for processing the PDF file
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

# Replace the ChromaVectorDatabase with Chroma
vector_index = Chroma.from_documents(texts, AzureOpenAIEmbeddings(
    azure_endpoint=GPT_4_API_BASE,
    deployment=EmbeddingModelDeploymentName,
))


# Create the retriever
retriever = vector_index.as_retriever(search_type="similarity", search_kwargs={"k": 6})

# Update the qa_interface
qa_interface = RetrievalQA.from_chain_type(
    llm=AzureChatOpenAI(openai_api_key=GPT_4_API_KEY, api_version=GPT_4_API_VERSION, base_url=GPT_4_API_BASE,
                        azure_deployment=GPT_4_ID),
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

prompt = """

"""

prompt1 = """

"""

response = qa_interface(
    prompt1
)

print(response["result"])


