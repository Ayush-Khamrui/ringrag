from app.config import Config
from app.models.embedding import get_google_embedding
from app.models.generation import get_llm
import weaviate
from langchain_weaviate.vectorstores import WeaviateVectorStore
import weaviate
from weaviate.classes.init import Auth

def connect_to_vectordb():
    # Best practice: store your credentials in environment variables
    weaviate_url = "https://xszeyzqto6blwazoincfg.c0.asia-southeast1.gcp.weaviate.cloud"
    weaviate_api_key = "TpxLQjiwzoqAYWtyrk5MgWI6EUTU9BcgvEmR"

    # Connect to Weaviate Cloud
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=weaviate_url,
        auth_credentials=Auth.api_key(weaviate_api_key),
    )

    return client

def get_vector_db(docs):
    embeddings = get_google_embedding()
    client = connect_to_vectordb()
    vectordb = WeaviateVectorStore.from_documents(documents=docs, embedding=embeddings, client=client, persist_directory=Config.DB_DIR,index_name="MyVectorStore")
    return vectordb

def existing_vector_db():
    client = connect_to_vectordb()
    embeddings = get_google_embedding()
    vector_store = WeaviateVectorStore(
        embedding=embeddings,
        client=client,
        index_name="MyVectorStore",
        text_key="text"
    )
    return vector_store

def get_retriever(vectordb):
    llm = get_llm()
    return vectordb.as_retriever(search_type="mmr", search_kwargs={"k": 1, "fetch_k": 5},llm=llm)
