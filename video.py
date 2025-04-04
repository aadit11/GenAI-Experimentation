from langchain.document_loaders import AzureAIDocumentIntelligenceLoader
from langchain_community.agent_toolkits import AzureCognitiveServicesToolkit
from langchain.agents import AgentType, initialize_agent
from langchain.llms import AzureOpenAI

toolkit = AzureCognitiveServicesToolkit()

llm = AzureOpenAI(temperature=0)
agent = initialize_agent(
    tools=toolkit.get_tools(),
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

agent.run("What can I make with these ingredients?")