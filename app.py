import os
from dotenv import load_dotenv

# loading environment variable from the .env hidden file
load_dotenv()


# Load the Document
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_documents():
    loader = DirectoryLoader(
        "./docs/",
        glob="**/*.txt",
        loader_cls=TextLoader,
        loader_kwargs={"encoding": "utf-8"}
    )
    documents = loader.load()
    print(f"Loaded {len(documents)} documents")
    return documents


def split_documents(documents):
    """Split documents into manageable chunks for retrieval."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,          # Characters per chunk
        chunk_overlap=50,        # Overlap to preserve context across boundaries
        separators=["\n\n", "\n", "。", "！", "？", "，", " ", ""],
        length_function=len
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split into {len(chunks)} chunks")
    return chunks


# 2. Embeddings and Vector Store
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

def create_vector_store(chunks):
    """Create and persist a FAISS vector store."""
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"  # Efficient embedding model
    )
    
    # Check if vector store already exists
    if os.path.exists("./db/faiss_index"):
        vectorstore = FAISS.load_local(
            "./db/faiss_index", 
            embeddings,
            allow_dangerous_deserialization=True
        )
        print("Loaded existing vector store")
        return vectorstore
    
    # Create new vector store
    vectorstore = FAISS.from_documents(chunks, embeddings)
    vectorstore.save_local("./db/faiss_index")
    print("Created and saved new vector store")
    return vectorstore

# 3. RAG Chain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def create_rag_chain(vectorstore):
    """Build the complete RAG pipeline."""
    
    # Create retriever with MMR for diverse results
    retriever = vectorstore.as_retriever(
        search_type="mmr",  # Maximal Marginal Relevance
        search_kwargs={
            "k": 5,          # Return top 5 chunks
            "fetch_k": 20,   # Fetch 20 for MMR diversity
            "lambda_mult": 0.5
        }
    )
    
    # System prompt template
    template = """You are an expert assistant for question-answering tasks.
    Use the following pieces of retrieved context to answer the question.
    If you don't know the answer, just say "I don't have enough information to answer that."
    Keep your answer concise and cite the source when possible.
    
    Question: {question}
    
    Context: {context}
    
    Answer:"""
    
    prompt = ChatPromptTemplate.from_template(template)
    
    # Initialize LLM
    llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature=0.3,  # Lower temperature for factual answers
        max_tokens=500
    )
    
    # Format documents for the prompt
    def format_docs(docs):
        return "\n\n".join([
            f"Source: {doc.metadata.get('source', 'Unknown')}\n{doc.page_content}"
            for doc in docs
        ])
    
    # Build the RAG chain using LCEL
    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain

# 4. Main Application
def main():
    """Run the Q&A system."""
    print("\n=== RAG Q&A System ===\n")
    print("Loading and processing documents...")
    
    # Load and process documents
    documents = load_documents()
    chunks = split_documents(documents)
    
    # Create vector store
    vectorstore = create_vector_store(chunks)
    
    # Create RAG chain
    rag_chain = create_rag_chain(vectorstore)
    
    print("\nSystem ready! Ask questions about your documents.\n")
    print("Type 'exit' to quit.\n")
    
    # Interactive Q&A loop
    while True:
        question = input("\nYour question: ")
        if question.lower() in ["exit", "quit", "q"]:
            print("Goodbye!")
            break
        
        if not question.strip():
            continue
        
        print("\nThinking...")
        try:
            answer = rag_chain.invoke(question)
            print(f"\nAnswer:\n{answer}\n")
            print("-" * 50)
        except Exception as e:
            print(f"\nError: {e}\n")

if __name__ == "__main__":
    main()