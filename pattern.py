# In[1]:
import os
from llama_index.llms.azure_openai import AzureOpenAI
from datetime import datetime
import pandas as pd
from llama_index.core.query_engine import PandasQueryEngine
from llama_index.core import ServiceContext
import logging
import sys
import matplotlib.pyplot as plt
import pandas as pd



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


df = pd.read_csv("data\merged_file.csv",encoding="latin1")


# In[7]:


service_context = ServiceContext.from_defaults(llm=llm)


# In[8]:


df.head()


# In[9]:


query_engine = PandasQueryEngine(df=df,service_context=service_context,verbose=True)


# In[10]:


print(datetime.now())
response = query_engine.query(
    "How many such transactions are there where beneficiary is sending money back to the same remmiter.",)
print(datetime.now())


# In[ ]:

print(datetime.now())
response = query_engine.query(
    "Plot a graph comparing the number of debit and credit amounts",)
print(datetime.now())



# %%
print(datetime.now())
response = query_engine.query(
    "Tell me the exact number of a pair of transactions where the remmiter is sending some amount to beneficiary and the beneficiary then sends some maount back to the same remmiter",)
print(datetime.now())


# %%
print(datetime.now())
response = query_engine.query(
    "Tell me the exact number of a pair of transactions where the remmiter is sending some amount to beneficiary and the beneficiary then sends some maount back to the same remmiter. Also then give me all the pairs of remmiter and beneficiary which satisfy these conditions.",)
print(datetime.now())

# %%
