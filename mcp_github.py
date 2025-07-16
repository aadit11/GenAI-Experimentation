from langgraph.graph import StateGraph
from langchain_community.chat_models import ChatOllama
from langchain.agents import Tool, AgentExecutor, create_openai_functions_agent
from github import Github
import os

GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
REPO_NAME = "aadit11/Medi-Match-Copilot"

github = Github(GITHUB_TOKEN)
repo = github.get_repo(REPO_NAME)


llm = ChatOllama(model="llama3.1")


def review_code(file_path: str):
    content_file = repo.get_contents(file_path)
    code = content_file.decoded_content.decode("utf-8")
    prompt = f"You are a senior software engineer. Review the following code and provide feedback:\n\n{code}"
    response = llm.invoke(prompt)
    return response.content if hasattr(response, 'content') else str(response)

code_tools = [
    Tool(
        name="review_code",
        func=lambda input: review_code(**input),
        description="Review a file from the GitHub repo. Input must be a dict with 'file_path'."
    )
]


llm_agent = create_openai_functions_agent(llm, code_tools)
executor = AgentExecutor(agent=llm_agent, tools=code_tools, verbose=True)


def llm_node(state):
    print("\n[LLM Node] Processing user input...")
    result = executor.invoke({"input": state["user_input"]})
    return {"result": result}

workflow = StateGraph()
workflow.add_node("llm", llm_node)
workflow.set_entry_point("llm")
workflow.set_finish_point("llm")
app = workflow.compile()


example_input = {
    "user_input": "Review the file 'app/main.py' for improvements."
}

if __name__ == "__main__":
    print("\n--- Running LangGraph Code Review with LLaMA 3.1 ---")
    result = app.invoke(example_input)
    print("\n[Final Output]:", result["result"])
