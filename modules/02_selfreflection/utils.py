from dotenv import load_dotenv
from tavily import TavilyClient
from langfuse.openai import openai


load_dotenv()

openai_client = openai
tavily_client = TavilyClient()