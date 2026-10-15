from typing import List

from pydantic import BaseModel,Field
from dotenv import load_dotenv


load_dotenv()

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

# from tavily import TavilyClient

# tavily = TavilyClient()


# @tool
# def search(query: str):
#     """
#         Tool that searches over internet
#         Args:
#             query: The query to search for
#         Returns:
#             The search results
#     """
#     print(f"Searching for: {query}")
#     return tavily.search(query = query)

class Source(BaseModel):
    """Schema for a source used by the agent"""
    url:str = Field(description="The URL of the source")

class AgentResponse(BaseModel):
    """Schema for the response from the agent"""
    answer:str = Field(description="The answer from the agent")
    sources:List[Source] = Field(default_factory=list, description="The sources used by the agent to answer the question")




llm = ChatOpenAI()
tools = [TavilySearch()]
agent = create_agent(model=llm, tools=tools, response_format=AgentResponse)


def main():
    print("Hello from langchain-course!")
    result = agent.invoke({"messages": [HumanMessage(content="Search top 3 jobs for AI Engineer using LangChain in the California on linkedin which accepts H1B applications.")]})
    print(f"Result: {result}")

if __name__ == "__main__":
    main()