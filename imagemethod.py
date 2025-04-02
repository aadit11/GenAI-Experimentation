from pdf2image import convert_from_path
import pytesseract
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage
from datetime import datetime
from PIL import Image, ImageEnhance
import os
from dotenv import load_dotenv
import pytesseract


pytesseract.pytesseract.tesseract_cmd = "C:\pytesseract-0.3.10"


openai_api_key = ""

llm = AzureChatOpenAI(
    deployment_name="",
    openai_api_version="",
    openai_api_key=openai_api_key,
    openai_api_base="",
)


print(datetime.now())

pdf_path = "data/file.pdf"


def pdf_to_images(pdf_path):
    images = convert_from_path(pdf_path,poppler_path=r'C:\poppler-23.01.0\Library\bin')
    return images

def extract_text_from_image(image):
    # Pre-processing
    image = image.convert("L")  # Convert to grayscale
    image = ImageEnhance.Contrast(image).enhance(2.0)  # Increase contrast
    image = ImageEnhance.Sharpness(image).enhance(2.0)  # Increase sharpness
    image = image.point(lambda x: 0 if x < 128 else 255)  # Binarization

    
    text = pytesseract.image_to_string(image)
    return text

def pdf_to_text(pdf_path):
    all_text = ''
    images = pdf_to_images(pdf_path)
    for i, image in enumerate(images):
        text = extract_text_from_image(image)
        all_text += f'Page {i + 1}:\n{text}\n'
    return all_text

def handle_input_from_terminal_and_pdf(pdf_path, previous_context=None):
    pdf_text = pdf_to_text(pdf_path)
    
    user_query = input("Enter your query (or press Enter to skip):\n")
    
    general_info = "This is a document about XYZ. It contains information about ABC."
    user_message = HumanMessage(content=f"{pdf_text}\n{general_info}", context=previous_context)
    
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
