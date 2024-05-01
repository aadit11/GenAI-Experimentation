
import os
import time

os.environ["OPENAI_API_KEY"] = ""

from langchain_openai import ChatOpenAI
from langchain.globals import set_llm_cache

llm = ChatOpenAI(model="gpt-3.5-turbo-0125")



from langchain.cache import InMemoryCache

set_llm_cache(InMemoryCache())


start = time.time()

response = llm.invoke("Tell me a joke")
print(response)

end = time.time()  # End time
print("Time taken:", end - start, "seconds")


start = time.time()

response = llm.invoke("Tell me a joke")
print(response)

end = time.time()  # End time
print("Time taken:", end - start, "seconds")