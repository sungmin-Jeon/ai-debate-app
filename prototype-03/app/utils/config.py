import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langfuse import Langfuse

load_dotenv()

def get_llm():
    return ChatOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.7,
    )

def get_langfuse():
    return Langfuse(
        secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
        public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
        host=os.getenv("LANGFUSE_BASE_URL"),
    )

langfuse = get_langfuse()