# Chat with Gemini

## Introduction

This project aims to create a generative AI-based application utilizing the Gemini AI API. It facilitates summarization of context, question answering, and code analysis.

## Getting Started

### Prerequisites

- Python 3.9
- [Create an account on Gemini AI](https://aistudio.google.com/app/apikey) to obtain your API token.

### Installation

To install the required packages, run the following command:

```bash
pip install -r requirements.txt
```

### API Token

Before running the project, make sure to generate your API token from the Gemini AI website: [Gemini API Token](https://aistudio.google.com/app/apikey). Once obtained, create a file named `.env` in the root directory and add your token like this:

```env
GOOGLE_API_KEY = your_api_token_here
```

### Running the Application

Execute the following command to run the main file:

```bash
streamlit run run.py
```

This will start the generative AI application using the Gemini AI API.

## Project Structure

- `rag_search_method.py`: Utilizes the Retrieve and Generate (RAG) method to provide answers to queries with the assistance of Google Gemini AI model and ChromaDB database.
- `vector_search_method.py`: Implements text-to-vector conversion and searches the vector space for the given query.
- `webpage.py`: Provides the Streamlit frontend for the webpage.
- `requirements.txt`: Contains all relevant packages.

## Related Topics to Know Before Use

- Language Models (LLMs): A Language Model (LLM) is an AI model trained to understand and generate human-like text based on vast amounts of natural language data.
- Embedding: Knowledge of embedding techniques for converting text into numerical vectors.
- MongoDB: Understanding of MongoDB database for storage and retrieval of data.
- ChromaDB: ChromaDB is database specially for the vector storing, retrieval and search in vector space.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- [Gemini AI](https://gemini.google.com/app) for providing the powerful generative AI API.

---
