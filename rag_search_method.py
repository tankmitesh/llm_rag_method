# Inbuild packages
import os 
from dotenv import load_dotenv
load_dotenv()

# Third party packages
from langchain_google_genai import GoogleGenerativeAIEmbeddings, GoogleGenerativeAI
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import Chroma

################################################################################################## 

def data_to_embeddding(dir_path) :

    # load all files and into one document
    loader = DirectoryLoader(dir_path, glob = "**/*.txt")
    docs = loader.load()

    # splitting document into text 
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 100, chunk_overlap = 50)
    texts = text_splitter.split_documents(docs)

    persist_directory = "db"
    embedding_model = GoogleGenerativeAIEmbeddings(model = "models/embedding-001", 
                                                   google_api_key = os.getenv("GENAI_KEY"))

    vector_db = Chroma.from_documents(documents = texts, 
                                     embedding = embedding_model,
                                     persist_directory = persist_directory)
    
    # persiste the db to disk
    vector_db.persist()
    vector_db = None

    # Now we can load the persisted database from disk, and use it as normal. 
    vector_db = Chroma(persist_directory = persist_directory, 
                       embedding_function = embedding_model)
    
    retriever = vector_db.as_retriever(search_kwargs={"k": 2})
    
    return retriever

################################################################################################## 

def rag_query(retriever, query) :

    # create the chain to answer questions 
    qa_chain = RetrievalQA.from_chain_type(llm = GoogleGenerativeAI(model = "gemini-pro", 
                                                                    google_api_key = os.getenv("GENAI_KEY")), 
                                                                    chain_type = "stuff", 
                                                                    retriever = retriever, 
                                                                    return_source_documents = True)
    llm_response = qa_chain(query)
    
    return llm_response['result']