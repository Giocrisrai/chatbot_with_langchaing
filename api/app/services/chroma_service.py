from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
import os


def initialize_chroma(persist_directory: str):
    """
    Inicializa la base de datos Chroma con OpenAI Embeddings.

    Args:
    - persist_directory (str): Directorio para almacenar la base de datos de Chroma.

    Returns:
    - Chroma: Instancia de la base de datos Chroma.
    """
    os.environ['OPENAI_API_KEY'] = os.getenv(
        'OPENAI_API_KEY', 'default_api_key')
    embeddings = OpenAIEmbeddings()
    return Chroma(persist_directory=persist_directory, embedding_function=embeddings)


def store_document_in_chroma(chroma_db, document_content, unique_filename):
    """
    Convierte el contenido del documento en embedding y lo almacena en Chroma.

    Args:
    - chroma_db: Instancia de la base de datos Chroma.
    - document_content (str): Contenido del documento.
    - unique_filename (str): Nombre único del archivo/documento.

    Returns:
    - str: Mensaje de confirmación.
    """
    embedding = chroma_db.embedding_function.embed_text(document_content)
    chroma_db.add_documents([(unique_filename, embedding)])
    return "Documento almacenado en Chroma."


def search_similar_documents(chroma_db, query):
    """
    Realiza una búsqueda de similitud en la base de datos Chroma.

    Args:
    - chroma_db: Instancia de la base de datos Chroma.
    - query (str): Consulta para la búsqueda de similitud.

    Returns:
    - List[Document]: Lista de documentos similares encontrados.
    """
    return chroma_db.similarity_search(query)
