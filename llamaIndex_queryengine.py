# In[1]:


import os
from llama_index.llms import AzureOpenAI
from datetime import datetime
import pandas as pd
from llama_index.query_engine.pandas_query_engine import PandasQueryEngine
from llama_index.indices.service_context import ServiceContext
import logging
import sys
from IPython.display import Markdown, display
import matplotlib.pyplot as plt

import pandas as pd
from llama_index.query_engine import PandasQueryEngine





# In[2]:


llm = AzureOpenAI(
    engine="",
    model="",
    temperature=0.0,
    azure_endpoint="",
    api_key="",
    api_version="",
)


# In[3]:


os.environ["OPENAI_API_KEY"] = ""
os.environ[
    "AZURE_OPENAI_ENDPOINT"
] = ""
os.environ["OPENAI_API_VERSION"] = ""


# In[4]:


print(datetime.now())
response = llm.complete("how are you?")
print(response)
print(datetime.now())


# In[5]:


os.environ["OPENAI_API_KEY"] = ""
os.environ[
    "AZURE_OPENAI_ENDPOINT"
] = ""
os.environ["OPENAI_API_VERSION"] = ""


# In[6]:


df = pd.read_csv("data\leetcode_questions.csv",encoding="latin1")


# In[7]:


service_context = ServiceContext.from_defaults(llm=llm)


# In[8]:


df.head()


# In[9]:


query_engine = PandasQueryEngine(df=df,service_context=service_context,verbose=True)


# In[10]:


print(datetime.now())
response = query_engine.query(
    "What is the first question",)
print(datetime.now())


# In[ ]:

print(datetime.now())
response = query_engine.query(
    "Tell me the most mentioned",)
print(datetime.now())



# %%
print(datetime.now())
response = query_engine.query(
    "Give me the average value of the uploads coulumn",)
print(datetime.now())
# %%
