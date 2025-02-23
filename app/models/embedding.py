from langchain_google_genai import GoogleGenerativeAIEmbeddings

def get_google_embedding():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    return embeddings