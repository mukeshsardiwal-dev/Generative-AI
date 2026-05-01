# from langchain_openai import OpenAIEmbeddings
# from dotenv import load_dotenv

# load_dotenv()
# embeddings = OpenAIEmbeddings(model="text-embedding-3-small", dimensions=64)

# # vector = embeddings.embed_query("You are going to learn Gen AI")
text = ["Hello, I am Mukesh Sardiwal","I am a Backend Engineer"]
# vector = embeddings.embed_documents(text)
# print(vector)

from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
)

vector = embeddings.embed_documents(text)
print(vector)