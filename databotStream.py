# In[1]:
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import os
from datetime import datetime
import time

# In[1]:
openai_api_key = os.environ['OPENAI_API_KEY'] 

llm = AzureChatOpenAI(deployment_name="", openai_api_version="", openai_api_key=openai_api_key, openai_api_base="")


# In[1]:
print(datetime.now())
msg = HumanMessage(content="Write a song about water in 250 words")
response = llm(messages=[msg])
print(datetime.now())

# In[1]:
content = response.content
words = content.split()
words_per_line = 15

# In[1]:
word_count = 0
print(datetime.now())
for word in words:
    print(word, end=' ', flush=True)
    time.sleep(0.1)

    word_count = word_count + 1
    if word_count % words_per_line == 0:
        print('\n', end='', flush=True)

print(datetime.now())  


# %%
