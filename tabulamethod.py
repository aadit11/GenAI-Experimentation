import fitz  # PyMuPDF
import tabula
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage
from datetime import datetime

openai_api_key = ""

llm = AzureChatOpenAI(
    deployment_name="",
    openai_api_version="",
    openai_api_key=openai_api_key,
    openai_api_base="",
)

print(datetime.now())

pdf_path = "data\file.pdf"

def extract_plain_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page_num in range(doc.page_count):
        page = doc[page_num]
        text += page.get_text()
    return text

def extract_tables_from_pdf(pdf_path):
   
    tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
    return tables

def process_and_query_pdf(plain_text, extracted_tables, user_query):
    output = []

    if "summary" in user_query.lower():
        summary = plain_text[:500]
        output.append(f"Summary: {summary}")

    if "table" in user_query.lower():
        for i, table in enumerate(extracted_tables, start=1):
            if not table.iloc[1:].empty:
                first_row_values = table.iloc[0].tolist()
                output.append(f"Values from the first row of Table {i}: {first_row_values}")

    return output


def handle_input_from_terminal_and_pdf(pdf_path, previous_context=None):
    plain_text = extract_plain_text_from_pdf(pdf_path)

    extracted_tables = extract_tables_from_pdf(pdf_path)

    user_query = input("Enter your query (or press Enter to skip):\n")

    query_output = process_and_query_pdf(plain_text, extracted_tables, user_query)

    user_message = HumanMessage(content=f"{query_output}", context=previous_context)

    if user_query:
        user_message.content += f"\nUser Query: {user_query}"

    response_generator = llm.stream([user_message])

    for chunk in response_generator:
        print(chunk.content, end='', flush=True)

    return user_message.context

previous_context = None

while True:
    previous_context = handle_input_from_terminal_and_pdf(pdf_path, previous_context)
    print(datetime.now())
