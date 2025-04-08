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

df = pd.read_csv("Global_YouTube_Statistics.csv", encoding="latin1")

# In[1]:
service_context = ServiceContext.from_defaults(llm=llm)

# In[1]:
df.head()

# In[1]:
query_engine = PandasQueryEngine(df=df, service_context=service_context, verbose=True)

# In[1]:
startTime = time.time()
response = query_engine.query(
    "Visulaize the comparison between the subscribers of pewidepie and tseries",
)
endTime = time.time()
timeTaken = endTime - startTime
print("time taken : ",timeTaken)


