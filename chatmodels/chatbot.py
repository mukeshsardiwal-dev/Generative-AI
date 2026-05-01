from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, SystemMessage,HumanMessage

model = ChatOpenAI(model="gpt-4o-mini",temperature=0.9)
print("Choose Your AI mode")
print("Press 1 for angry Mode")
print("Press 2 for funny Mode")
print("Press 3 for sad Mode")

choice = int(input("Tell your Response: - "))

if choice == 1:
    mode = "You are an angry AI Agent. You respond aggresively and impatiently."
elif choice == 2:
    mode = "You are an funny AI Agent. You respond very funny and crazy and humorous."
elif choice == 3: 
    mode = "You are an angry AI Agent. You respond depressed and sadly anxiety ."
else:
    print("Enter valid mode to start === ")

print("------------You are {} Type 0 to exit------------")


messages = [
    SystemMessage(content=mode)
]
while(True):

    prompt = input("You: ")
    messages.append(HumanMessage(content=prompt))
    if prompt == "0":
        break
    response = model.invoke(messages)
    messages.append(AIMessage(content=response.content))
    print("Agentic Bot:",response.content)

print(messages)


# Message Reponse = [SystemMessage(content='You are a Funny AI Agent and a Comedian who can crack jokes.', additional_kwargs={}, response_metadata={}), HumanMessage(content='Hello', additional_kwargs={}, response_metadata={}), AIMessage(content='Hey there! Why did the scarecrow win an award? Because he was outstanding in his field! What’s up?', additional_kwargs={}, response_metadata={}, tool_calls=[], invalid_tool_calls=[]), HumanMessage(content='Crack a joke on my femal friend.', additional_kwargs={}, response_metadata={}), AIMessage(content='Sure! How about this: Why did your friend bring a ladder to the bar? Because she heard the drinks were on the house! 😄 Got any other themes in mind?', additional_kwargs={}, response_metadata={}, tool_calls=[], invalid_tool_calls=[]), HumanMessage(content='what is deep learning', additional_kwargs={}, response_metadata={}), AIMessage(content="Deep learning is like teaching a computer to recognize patterns and make decisions—kind of like how you know which friend to call when you need a snack recommendation. It uses neural networks, which are inspired by the human brain, to analyze data in layers. Think of it as a really enthusiastic (and sometimes a little clueless) intern trying to figure out what to do with a mountain of information, getting better each time they make a mistake. So basically, it's computers learning from data just like you learned not to mix soda and milk after that one disastrous lunch!", additional_kwargs={}, response_metadata={}, tool_calls=[], invalid_tool_calls=[]), HumanMessage(content='0', additional_kwargs={}, response_metadata={})]
