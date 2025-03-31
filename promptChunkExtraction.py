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

        # Use language model to determine if the page content matches the prompt
        if prompt in text:
            relevant_chunks.append((page_num + 1, text))  # Adding page number along with chunk

    return relevant_chunks


def generate_prompt():
    # You can modify this function to take user input for the prompt
    user_prompt = input("Give me the user requirements: ")
    return user_prompt


def stream_responses(prompt, messages):
    # Send each message to the model and stream responses
    for i, message in enumerate(messages):
        response = llm.stream(prompt + message)
        print(f"Response {i + 1}:\n{response['choices'][0]['message']['content']}\n")


pdf_path = "data\file.pdf"
user_prompt = generate_prompt()
chunks = split_pdf_by_prompt(pdf_path, user_prompt)

# Extract text from each chunk and stream responses
for i, (page_num, chunk) in enumerate(chunks):
    print(f"Chunk {i + 1} (Page {page_num}):\n{chunk}\n")
    messages = chunk.split('\n')  # You can adjust this based on how you want to split the text
    stream_responses(user_prompt, messages)
