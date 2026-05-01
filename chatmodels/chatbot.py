from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import GoogleGenerativeAI

model = GoogleGenerativeAI(model="gemini-2.5-flash",temperature=0.9)
print("------------You are taking to AI Agent Created By Mukesh Sardiwal Type 0 to exit------------")
while(True):

    prompt = input("You: ")
    if prompt == "0":
        break
    response = model.invoke(prompt)
    print("Agentic Bot:",response)
