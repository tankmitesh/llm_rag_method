# Inbuild packages
import os
from typing import List
from dotenv import load_dotenv
load_dotenv()

# Third party packages
import google.generativeai as genai
from tqdm import tqdm
import pymongo

###########################################################################################

def database_connector() :

    """Connect database and get movie data collection."""

    # get password
    PASSWORD = os.getenv("PASSWORD")

    if PASSWORD == None :
        return "Password is invalid!" 

    # link with server
    client = pymongo.MongoClient(f"mongodb+srv://generativeai:{PASSWORD}@cluster0.a8ppcpx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

    # connect with database
    db = client.sample_mflix

    # get collection
    collection = db.movies 

    return collection

###########################################################################################

def vector_query(text: str) -> List[str] :

    """input text query and find similar data based on vector search.

    Args:
        text : input text for similar data search.

    Retunrs:
        movie_data : similar movie data 

    """

    # get data
    collection = database_connector()

    # text to vector convert
    text_vector = text_to_embedding(text)

    results = collection.aggregate([{"$vectorSearch" : {"queryVector" : text_vector,
                                                        "path" : "plot_embedding_hf",
                                                        "limit" : 4,
                                                        "index" : "default",
                                                        "numCandidates" : 100,
                                                        }}
                                                ])
    
    movie_data = [ ]
    for xdocument in results :
        movie_data.append([xdocument['title'], xdocument['plot']])


    return movie_data

###########################################################################################

def text_to_embedding(text: str) -> List[float] :


    """convert input text data into vector (embedding vector).

    Args :
        text : text which convert into vector.

    Returns :
        embedding_vector : vector form of given text input. 
    """

    # get gemini api key
    genai.configure(api_key = os.getenv("GENAI_KEY"))

    embedding_model = genai.embed_content(model= "models/embedding-001",
                                          content = text)
    
    embedding_vector = embedding_model['embedding']
    
    return embedding_vector

###########################################################################################

def embedding_generation(num_of_doc: int) -> None :


    """generate embedding vector from movie data information.

    Args :
        num_of_doc : number of documents convert into vector.

    Retunrs :
        None
    """

    # get data
    collection = database_connector()

    # apply find query with num of doc limit
    collection_files = collection.find({"plot" :  {"$exists" : True}}).limit(num_of_doc)

    # text template 
    embedding_template = """
                        Movie Title : {title} \n
                        Plot : {plot}
                        """ 

    for xdoc in tqdm(collection_files) :

        # data extraction
        title, plot = xdoc['title'], xdoc['plot']

        # fillup information
        text_data = embedding_template.format(title = title, plot = plot)
        
        # convert text into vector and store
        xdoc['plot_embedding_hf'] = text_to_embedding(text_data)

        # replace new id with old id
        collection.replace_one({"_id" : xdoc['_id']}, xdoc)


