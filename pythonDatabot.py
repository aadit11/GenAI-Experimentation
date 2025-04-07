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
# import time



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
    ""
] = ""
os.environ["OPENAI_API_VERSION"] = ""



# In[1]:


def generate_natural_language_explanation(query):
    response = llm.complete(f"Explain the following query: {query}")
    return response

# In[1]:

df = pd.read_csv("Global_YouTube_Statistics.csv", encoding="latin1")

# In[1]:
service_context = ServiceContext.from_defaults(llm=llm)

# In[1]:
df.head()

# In[1]:
query_engine = PandasQueryEngine(df=df, service_context=service_context, verbose=True)

# In[1]:
print(datetime.now())
response = query_engine.query(
    "give me the  top ten youtube channels based on subscribers and add the title.",
)
natural_language_explanation = generate_natural_language_explanation(
    query="give me the  top ten youtube channels based on subscribers and add the title."
)
print(f"Natural language explanation: {natural_language_explanation}")
print(datetime.now())


# In[1]:
print(datetime.now())
response = query_engine.query(
    "Tell me the country which has the most youtubers",
)
natural_language_explanation = generate_natural_language_explanation(
    query="Tell me the country which has the most youtubers"
)
print(f"Natural language explanation: {natural_language_explanation}")
print(datetime.now())


# %%
# starttime = time.time()
print(datetime.now())
response = query_engine.query(
    "Give me the average value of the uploads column for all youtubers",
)
print('After response')
print(response)
natural_language_explanation = generate_natural_language_explanation(
    query="Give me the average value of the uploads column for all youtubers"
)
# endtime = time.time()
print(f"Natural language explanation: {natural_language_explanation}")
print(datetime.now())
# print("time taken : ", endtime - starttime)

# %% natural_language_explanation = generate_natural_language_explanation(
# starttime = time.time()
natural_language_explanation = generate_natural_language_explanation(
    query="Give me the average value of the uploads column for all youtubers"
)
# endtime = time.time()
print(natural_language_explanation)
# print(endtime - starttime)

# %%
print(datetime.now())
response = query_engine.query(
    "Give me the most common category",
)
natural_language_explanation = generate_natural_language_explanation(
    query="Give me the most common category"
)
print(f"Natural language explanation: {natural_language_explanation}")
print(datetime.now())

# %%
print(datetime.now())
response = query_engine.query(
    "When did WWE create its channel",
)
natural_language_explanation = generate_natural_language_explanation(
    query="When did WWE create its channel"
)
print(f"Natural language explanation: {natural_language_explanation}")
print(datetime.now())


# %%
print(datetime.now())
response = query_engine.query(
    "Which youtuber is ranked 23rd in video views",
)
natural_language_explanation = generate_natural_language_explanation(
    query="Which youtuber is ranked 23rd in video views"
)
print(f"Natural language explanation: {natural_language_explanation}")
print(datetime.now())

















