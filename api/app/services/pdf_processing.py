import logging
from langchain.document_loaders import PyPDFLoader
from langchain.schema.document import Document
from typing import Tuple, List
import PyPDF2

# Set up logging
logging.basicConfig(level=logging.INFO)


def process_pdf(file_path: str) -> Tuple[List[Document], str]:
    """
    Procesa un archivo PDF desde una ruta de archivo local para extraer texto y devuelve los datos extraídos.

    Parameters:
    - file_path (str): La ruta del archivo PDF a procesar.

    Returns:
    - Tuple[List[Document], str]: Una tupla que contiene los datos de texto extraídos y la ruta del archivo PDF.
    """
    try:
        logging.info(f"Processing PDF: {file_path}")

        # Obtiene el número de páginas
        with open(file_path, 'rb') as f:
            pdf = PyPDF2.PdfReader(f)
            numero_paginas = len(pdf.pages)
        logging.info(f"Number of pages: {numero_paginas}")

        # Procesa el PDF
        loader = PyPDFLoader(file_path)
        data = loader.load()

        logging.info(f"PDF processed successfully: {file_path}")

        return data, file_path

    except Exception as e:
        logging.error(f"Error processing the PDF: {e}")
        raise Exception(f"Error processing the PDF: {e}")
