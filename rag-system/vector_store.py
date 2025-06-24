import os
import chromadb
from chromadb.config import Settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.schema import Document
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MedicalKnowledgeVectorStore:
    def __init__(self, persist_directory="./chroma_db"):
        """Initialize the vector store for medical knowledge."""
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            length_function=len,
        )
        self.vectorstore = None
        
    def load_medical_documents(self, docs_directory="./medical_knowledge"):
        """Load and process medical documents."""
        documents = []
        
        # Get all text files from the medical knowledge directory
        for filename in os.listdir(docs_directory):
            if filename.endswith('.txt'):
                file_path = os.path.join(docs_directory, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                        doc = Document(
                            page_content=content,
                            metadata={
                                "source": filename,
                                "type": "medical_knowledge"
                            }
                        )
                        documents.append(doc)
                        logger.info(f"Loaded document: {filename}")
                except Exception as e:
                    logger.error(f"Error loading {filename}: {e}")
        
        return documents
    
    def create_vectorstore(self, documents=None):
        """Create or load the vector store."""
        if documents is None:
            documents = self.load_medical_documents()
        
        # Split documents into chunks
        texts = self.text_splitter.split_documents(documents)
        logger.info(f"Split documents into {len(texts)} chunks")
        
        # Create or load vector store
        if os.path.exists(self.persist_directory):
            logger.info("Loading existing vector store...")
            self.vectorstore = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
        else:
            logger.info("Creating new vector store...")
            self.vectorstore = Chroma.from_documents(
                documents=texts,
                embedding=self.embeddings,
                persist_directory=self.persist_directory
            )
            self.vectorstore.persist()
        
        return self.vectorstore
    
    def search_similar_documents(self, query, k=3):
        """Search for similar documents based on query."""
        if self.vectorstore is None:
            self.create_vectorstore()
        
        results = self.vectorstore.similarity_search(query, k=k)
        return results
    
    def add_documents(self, documents):
        """Add new documents to the vector store."""
        if self.vectorstore is None:
            self.create_vectorstore()
        
        texts = self.text_splitter.split_documents(documents)
        self.vectorstore.add_documents(texts)
        self.vectorstore.persist()
        logger.info(f"Added {len(texts)} new document chunks")

def initialize_vector_store():
    """Initialize and return the vector store."""
    vs = MedicalKnowledgeVectorStore()
    vectorstore = vs.create_vectorstore()
    return vs

if __name__ == "__main__":
    # Test the vector store
    print("Initializing medical knowledge vector store...")
    vs = initialize_vector_store()
    
    # Test search
    test_query = "What are the symptoms of endometriosis?"
    results = vs.search_similar_documents(test_query)
    
    print(f"\nSearch results for: '{test_query}'")
    for i, doc in enumerate(results):
        print(f"\n--- Result {i+1} ---")
        print(f"Source: {doc.metadata.get('source', 'Unknown')}")
        print(f"Content: {doc.page_content[:200]}...")