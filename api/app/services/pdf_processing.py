import logging
from langchain.document_loaders import PyMuPDFLoader
from langchain.schema.document import Document
from typing import List

# Set up logging
logging.basicConfig(level=logging.INFO)


def process_pdf(file_path: str) -> List[Document]:
    """
    Processes a PDF file, extracting text and metadata from each page.

    This function uses PyMuPDFLoader to load the PDF file and extract the content of each page,
    along with detailed metadata such as page number, title, author, etc.
    The progress of the processing and any errors encountered are logged.

    Parameters:
    - file_path (str): The path to the PDF file to be processed.

    Returns:
    - List[Document]: A list of Document objects,
      where each object represents a page of the PDF with its content and metadata.

    Raises:
    - Exception: Propagates any exceptions that occur during the processing of the PDF.
    """

    try:
        logging.info(f"Starting PDF processing: {file_path}")

        # Load and process the PDF
        loader = PyMuPDFLoader(file_path)
        documents = loader.load()

        # Log the number of processed pages
        number_of_pages = len(documents)
        logging.info(f"Number of pages processed: {number_of_pages}")

        logging.info(f"PDF processing completed successfully: {file_path}")
        return documents

    except Exception as e:
        logging.error(f"Error processing the PDF: {e}")
        raise Exception(f"Error processing the PDF: {e}")
