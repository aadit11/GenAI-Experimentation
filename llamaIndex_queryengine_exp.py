# In[1]:

import os
from llama_index.llms import AzureOpenAI
from datetime import datetime
import pandas as pd
from llama_index.query_engine.pandas_query_engine import PandasQueryEngine
from llama_index.indices.service_context import ServiceContext
import matplotlib.pyplot as plt

import pandas as pd
from llama_index.query_engine import PandasQueryEngine
import time



# In[1]:


llm = AzureOpenAI(
    engine="",
    model="",
    temperature=0.0,
    azure_endpoint="",
    api_key="",
    api_version="",
)


# In[1]:

os.environ["OPENAI_API_KEY"] = ""
os.environ[
    "AZURE_OPENAI_ENDPOINT"
] = ""
os.environ["OPENAI_API_VERSION"] = ""



# In[1]:


def generate_natural_language_explanation(query):
    response = llm.complete(f"Explain the following query: {query}")
    return response

# In[1]:


df = pd.read_csv("data\leetcode_questions.csv", encoding="latin1")

# In[1]:
service_context = ServiceContext.from_defaults(llm=llm)

# In[1]:
df.head()

# In[1]:
query_engine = PandasQueryEngine(df=df, service_context=service_context, verbose=True)

# In[1]:
print(datetime.now())
response = query_engine.query(
    "Plot a graph comparing the difficulties of the various questions present in the dataset",
)
natural_language_explanation = generate_natural_language_explanation(
    query="Plot a graph comparing the difficulties of the various questions present in the dataset"
)
print(f"Natural language explanation: {natural_language_explanation}")
print(datetime.now())







# %%
