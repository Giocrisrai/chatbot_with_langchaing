import logging
from langchain.vectorstores import Chroma
import os


def get_chroma_db(embeddings, documents, path, recreate_chroma_db=False):
    """
    Create or load a Chroma vector store from documents and embeddings.

    Parameters:
    - embeddings: The embeddings to use for creating the Chroma vector store.
    - documents: The documents to include in the Chroma vector store.
    - path: The path where the Chroma vector store will be saved or loaded from.
    - recreate_chroma_db (bool): If True, recreate the Chroma vector store; if False, load an existing one.

    Returns:
    - Chroma: The Chroma vector store.
    """
    try:
        if recreate_chroma_db:
            logging.info("RECREATING CHROMA DB")
            return Chroma.from_documents(
                documents=documents, embedding=embeddings, persist_directory=path
            )
        else:
            logging.info("LOADING EXISTING CHROMA")
            return Chroma(persist_directory=path, embedding_function=embeddings)
    except Exception as e:
        logging.error(f"Error in get_chroma_db: {e}")
        raise e
