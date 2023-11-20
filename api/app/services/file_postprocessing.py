import os
from typing import List

from langchain.schema.document import Document
from langchain.embeddings import OpenAIEmbeddings, SentenceTransformerEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()


def split_data(data: List[Document]) -> List[Document]:
    """
    Split the data into smaller chunks using RecursiveCharacterTextSplitter.

    Parameters:
    data (List[Document]): A list of Document objects containing the text data and metadata.

    Returns:
    List[Document]: A list of Document objects containing the text data split into smaller chunks.
    """
    # Configure chunk size and overlap
    chunk_size = 1000
    chunk_overlap = 200

    # Create a TextSplitter object
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )

    # Split documents into smaller chunks
    return text_splitter.split_documents(data)


def create_embeddings_openai(data: List[Document]) -> List[Document]:
    """
    Create embeddings for the data using OpenAIEmbeddings.

    Parameters:
    data (List[Document]): A list of Document objects containing the text data and metadata.

    Returns:
    List[Document]: A list of Document objects containing the text data, metadata, and embeddings.
    """
    # Set up the OpenAI API key from environment variables
    openai_api_key = os.getenv('OPENAI_API_KEY', 'default_api_key')
    os.environ['OPENAI_API_KEY'] = openai_api_key

    # Create an OpenAIEmbeddings object
    embeddings = OpenAIEmbeddings()

    # Generate text embeddings for the documents
    return embeddings.embed_documents(data)


def create_embeddings_open_source(model_name: str) -> List[Document]:
    """
    Create embeddings for the data using SentenceTransformerEmbeddings.

    Parameters:
    model_name (str): The name of the model to use for generating embeddings.

    Returns:
    List[Document]: A list of Document objects containing the text data, metadata, and embeddings.
    """
    # Create a SentenceTransformerEmbeddings object
    embeddings = SentenceTransformerEmbeddings(model_name=model_name)

    # Generate text embeddings for the documents
    return embeddings.embed_documents(data)
