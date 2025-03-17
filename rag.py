import time
from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI
from langchain.embeddings import AzureOpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from langchain.vectorstores import FAISS
import os 
import PyPDF2
from prompts_module import *

load_dotenv()

# # # Set the environment variables for Azure OpenAI
os.environ["OPENAI_API_TYPE"] = ""
os.environ["OPENAI_API_BASE"] = ""
os.environ["OPENAI_API_KEY"] = ""
os.environ["OPENAI_API_VERSION"] = "" 

# Create an instance of AzureOpenAIEmbeddings
embeddings = AzureOpenAIEmbeddings(
    deployment="",
    model="",
    openai_api_base= "",
    openai_api_key= "",
    openai_api_version = "",
    openai_api_type=""
)

model = AzureChatOpenAI(
        openai_api_base=os.getenv("GPT_4_API_BASE"),
        openai_api_version=os.getenv("GPT_4_API_VERSION"),
        deployment_name=os.getenv("GPT_4_ID"),
        openai_api_key=os.getenv("GPT_4_API_KEY"),
        openai_api_type=os.getenv("ORGANIZATION"),
    )

def extractTextFromPdf():
    file = 'data\path to file'
    try:
        if file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ''
            for page in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page].extract_text()
                # text.append(pdf_reader.pages[page].extract_text())
            if text and not text == '':
                return text
            else:
                return None
        else:
            return None

    except Exception as e:
        print(f"An error occurred: {e}")

    return None


vectorstore = FAISS.from_texts([extractTextFromPdf()], embedding=embeddings)
retriever = vectorstore.as_retriever()



def ChatWithPdf(template):
    prompt = ChatPromptTemplate.from_template(template)
    
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )

    res = chain.invoke(template)
    print(res)
    return res

question =f"""
insert prompt here

"""
ChatWithPdf(question)