from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
messages = [

]

model = ChatOpenAI(model="gpt-4o-mini",temperature=0.9)
print("------------You are taking to AI Agent Created By Mukesh Sardiwal Type 0 to exit------------")
while(True):

    prompt = input("You: ")
    messages.append(prompt)
    if prompt == "0":
        break
    response = model.invoke(messages)
    messages.append(response.content)
    print("Agentic Bot:",response.conten)

print(messages)