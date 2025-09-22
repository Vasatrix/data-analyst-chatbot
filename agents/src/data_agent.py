# agents/data_agent.py

import os
import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI
# Corrected import statement
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from dotenv import load_dotenv

# The rest of your code remains the same
# ...

# Load environment variables
load_dotenv()

def create_data_agent(df: pd.DataFrame):
    """
    Creates a LangChain agent for data analysis using a Pandas DataFrame.
    """
    # Initialize the Gemini model
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.1
    )

    # Create the Pandas DataFrame agent
    agent = create_pandas_dataframe_agent(
        llm,
        df,
        verbose=True, # Set to True to see the thought process of the agent
        agent_type="tool-calling", # This is a good choice for Gemini models
        allow_dangerous_code=True # IMPORTANT: Allows the agent to run Python code. Use with caution.
    )

    return agent
