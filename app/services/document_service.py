from langchain_community.document_loaders import S3DirectoryLoader
from app.models.splitter import text_splitter
from app.models.retrieval import get_vector_db
import os

os.environ["AWS_ACCESS_KEY_ID"] = os.getenv("AWS_ACCESS_KEY_ID")
os.environ["AWS_SECRET_ACCESS_KEY"] = os.getenv("AWS_SECRET_ACCESS_KEY")

def load_documents_aws():
    # Initialize the loader
    loader = S3DirectoryLoader('ringrag')

    # Load all documents
    all_documents = loader.load()

    # Filter documents by file extension
    desired_extensions = ('.pdf', '.docx', '.json', '.txt')
    filtered_documents = [
        doc for doc in all_documents
        if doc.metadata['source'].lower().endswith(desired_extensions)
]
    splitter = text_splitter(filtered_documents)
    get_vector_db(splitter)

    return filtered_documents
