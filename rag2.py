import time
from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI
from langchain.embeddings import AzureOpenAIEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda, RunnablePassthrough
from langchain.vectorstores import FAISS
from langchain.callbacks import get_openai_callback
import os 
import PyPDF2
import re
import time

load_dotenv()

os.environ["OPENAI_API_TYPE"] = os.getenv("")
os.environ["OPENAI_API_BASE"] = ""
os.environ["OPENAI_API_KEY"] = os.getenv("Embeddings_GPT_4_API_KEY")
os.environ["OPENAI_API_VERSION"] = os.getenv("Embeddings_GPT_4_API_VERSION")

embeddings = AzureOpenAIEmbeddings(
    deployment=os.getenv(""),
    model="",
    openai_api_base= "",
    openai_api_key= os.getenv("Embeddings_GPT_4_API_KEY"),
    openai_api_version = os.getenv("Embeddings_GPT_4_API_VERSION"),
    openai_api_type=os.getenv("")
)

model = AzureChatOpenAI(
        openai_api_base=os.getenv("GPT_4_API_BASE"),
        openai_api_version=os.getenv("GPT_4_API_VERSION"),
        deployment_name=os.getenv("GPT_4_ID"),
        openai_api_key=os.getenv("GPT_4_API_KEY"),
        openai_api_type=os.getenv("ORGANIZATION"),
    )

def extractTextFromPdf():
    file = 'file.pdf'
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

# print(extractTextFromPdf())
# vectorstore = FAISS.from_texts([extractTextFromPdf()], embedding=embeddings)
# retriever = vectorstore.as_retriever()
# print("Embeddings")


def generateSQLQuery(question):
    startTime = time.time()
    template = f""" 

    insert your template here
    You are a SQL query generator.

    question: {question}
"""
    cleaned_text = re.sub(r'\s{2,}', '  ', template)
    prompt = ChatPromptTemplate.from_template(template)

    
    chain = (
          {"question": RunnablePassthrough()}
        | prompt
        | model
        | StrOutputParser()
    )
    with get_openai_callback() as cb:
      past = time.time()
      SqlQuery = chain.invoke(question)
      print("[INFO] LLM Resposne Time: ",time.time()-past,"\n")
      input_token_cost = (cb.prompt_tokens/1000)*0.01
      output_token_cost = (cb.completion_tokens/1000)*0.03
      print(f"[INFO] Cost for GPT4 turbo:\ninput_token_cost:{input_token_cost}$\
            \noutput_token_cost:{output_token_cost}$\n\
            total_cost:{input_token_cost+output_token_cost}$")
      print("\n")
      print("Token Counter: ",cb)
    endTime = time.time()
    return SqlQuery

question = "Name of the all clients"
print(generateSQLQuery(question))