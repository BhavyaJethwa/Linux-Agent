import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini")

try:
    
    # Create a simple message to send to the LLM
    messages = [
        HumanMessage(content="Hello, how are you?")
    ]
    
    # Invoke the model to get a response
    response = llm.invoke(messages)
    
    print("✅ Success! Your OpenAI API key is working with LangChain.")
    print("\nModel's Response:")
    print(response.content)

except Exception as e:
    print("❌ An error occurred while testing the API key.")
    # Check for a specific authentication error
    if "AuthenticationError" in str(e):
        print("This likely means your API key is invalid or has insufficient credits.")
    print(f"Error details: {e}")