import fitz
from langchain.chat_models import AzureChatOpenAI

openai_api_key = ""

llm = AzureChatOpenAI(
    deployment_name="",
    openai_api_version="",
    openai_api_key=openai_api_key,
    openai_api_base="",
)


def split_pdf_by_prompt(pdf_path, prompt):
    doc = fitz.open(pdf_path)
    relevant_chunks = []

    for page_num in range(doc.page_count):
        page = doc[page_num]
        text = page.get_text()

        if prompt in text:
            relevant_chunks.append((page_num + 1, text)) 

    return relevant_chunks


def generate_prompt():
    user_prompt = input("Give me the user requirements: ")
    return user_prompt


def stream_responses(prompt, messages):
    for i, message in enumerate(messages):
        response = llm.stream(prompt + message)
        print(f"Response {i + 1}:\n{response['choices'][0]['message']['content']}\n")


pdf_path = "data\file.pdf"
user_prompt = generate_prompt()
chunks = split_pdf_by_prompt(pdf_path, user_prompt)

for i, (page_num, chunk) in enumerate(chunks):
    print(f"Chunk {i + 1} (Page {page_num}):\n{chunk}\n")
    messages = chunk.split('\n')  
    stream_responses(user_prompt, messages)
