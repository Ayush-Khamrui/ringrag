from app.models.retrieval import get_retriever,existing_vector_db
from app.models.generation import get_llm
from weaviate.classes.query import Filter
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from app.models.generation import get_llm

system_prompt = ChatPromptTemplate.from_messages([
    ("system", "Use only the context to craft the answer . Do not fabricate information.If you don't know simply tell I don't know.But be careful do not give any false and fabricated information.\n\n{context}"),
    ("human", "{input}")
])

def get_qa_service(question, title=None):
    # Initialize the vector database and retriever
    vectordb = existing_vector_db()
    retriever = get_retriever(vectordb)
    llm = get_llm()

    # Create the combine_docs_chain with the custom prompt
    combine_docs_chain = create_stuff_documents_chain(llm, system_prompt)

    # Create the retrieval chain
    rag_chain = create_retrieval_chain(retriever, combine_docs_chain)

    if title:
        search_filter = Filter.by_property("source").equal("s3://ringrag/"+title)
        # Search for the document with the specified title
        documents = vectordb.similarity_search(query=question,filters=search_filter)
        if documents:
            context = documents[0].page_content
            result = llm.invoke(question+" Answer the above question based on the below context, Do not fabricate any answer. if the answer to the question is not in the context simply state `I don't know`: "+context)
            return result.content
        else:
            # If the document isn't found, proceed with the usual retrieval
            result = rag_chain.invoke({"input": question})
    else:
        # If no title is provided, proceed with the usual retrieval
        result = rag_chain.invoke({"input": question})

    return result["answer"]