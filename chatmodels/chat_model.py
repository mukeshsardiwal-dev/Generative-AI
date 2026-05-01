from dotenv import load_dotenv
load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

# openai_model = ChatOpenAI(model="gpt-4o")
google_model = ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0.5,max_tokens=10)

# print(openai_model.invoke("Hello from OpenAI"))
response = google_model.invoke("Hello, I am Mukesh Sardiwal?")
print(response.content)