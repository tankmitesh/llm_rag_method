# Third party package
import streamlit as st

# Custom packages
from rag_search_method import data_to_embeddding, rag_query
from vector_search_method import vector_query

#############################################################################

def get_webpage() :

    # title 
    st.title("VectorVerse: Mapping Similarity with Gemini AI")

    # side panel
    page = st.sidebar.selectbox("Select Method : ", ['VectorSearch', "RAG"])

    if page == "VectorSearch" :
        vector_page()

    elif page == "RAG" :
        rag_page()


##############################################################################
        
def vector_page() :

    # input text query
    text_data = st.text_input("Write your movie context")

    button_data = st.button("Search")

    if button_data : 
        
        # convert into vector and apply similarity search
        movie_data = vector_query(text_data)

        for xdata in movie_data :
            st.write(f"""Movie Name : {xdata[0]}\n
                     Movie Plot : {xdata[1]}""")

##############################################################################

def rag_page() :

    folder_path = st.text_input("Paste dir path : ")

    submit_button = st.button("Submit")

    if folder_path and submit_button :

        # generate embedding data and store in database
        retriever = data_to_embeddding(folder_path)
        st.success("Data is processed")
        
        question = st.text_input("Ask me question :")

        button_data = st.button("Search")

        if button_data :  
                  
            # search context based on database and llm
            answer = rag_query(retriever, question)

            st.write(f"**Answer:** {answer}")

##############################################################################

if __name__ == "__main__":
    get_webpage()



   