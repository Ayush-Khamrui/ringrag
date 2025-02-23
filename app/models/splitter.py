import os
from langchain_text_splitters import RecursiveCharacterTextSplitter

def text_splitter(docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = []
    
    for doc in docs:
        # Extract the source path from metadata
        source_path = doc.metadata.get('source', '')
        
        # Extract the filename without extension
        title = os.path.splitext(os.path.basename(source_path))[0]
        
        # Update the document's metadata with the title
        doc.metadata['title'] = title
        
        # Split the document into chunks
        chunks = text_splitter.split_documents([doc])
        
        # Add the chunks to the list
        split_docs.extend(chunks)
    
    return split_docs


