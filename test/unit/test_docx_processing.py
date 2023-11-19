import pytest
import os
from unittest.mock import Mock, patch
from langchain.schema.document import Document
from api.app.services.docx_processing import process_docx
import tempfile


@patch('api.app.services.docx_processing.UnstructuredWordDocumentLoader')
def test_process_docx_success(mock_loader: Mock) -> None:
    """
    Test to ensure that the process_docx function correctly processes a simulated DOCX.

    This test simulates the behavior of UnstructuredWordDocumentLoader returning mock documents,
    and then checks whether the process_docx function processes these documents as expected.

    Args:
        mock_loader (Mock): A mock object of UnstructuredWordDocumentLoader.
    """
    # Set up simulated behavior
    mock_docs: List[Document] = [
        Document(page_content="Test Content 1", metadata={"page": 1}),
        Document(page_content="Test Content 2", metadata={"page": 2})
    ]
    mock_loader.return_value.load.return_value = mock_docs

    # Create a temporary fake DOCX file
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as temp_file:
        temp_path = temp_file.name

    try:
        # Execute the function with the temporary file path
        documents = process_docx(temp_path)

        # Perform assertions
        assert len(documents) == 2
        assert documents[0].page_content == "Test Content 1"
        assert documents[1].page_content == "Test Content 2"
        assert documents[0].metadata["page"] == 1
        assert documents[1].metadata["page"] == 2
    finally:
        # Clean up by removing the temporary file
        os.remove(temp_path)


@patch('api.app.services.docx_processing.UnstructuredWordDocumentLoader')
def test_process_docx_error(mock_loader: Mock) -> None:
    """
    Test the error handling in the process_docx function.

    This test simulates a situation where UnstructuredWordDocumentLoader throws an exception,
    and then checks whether the process_docx function correctly propagates this exception.

    Args:
        mock_loader (Mock): A mock object of UnstructuredWordDocumentLoader.
    """
    # Set up the mock to throw an exception
    mock_loader.return_value.load.side_effect = Exception("Error de carga")

    # Create a temporary fake DOCX file
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as temp_file:
        temp_path = temp_file.name

    try:
        # Verify that an exception is thrown as expected
        with pytest.raises(Exception) as exc_info:
            process_docx(temp_path)
        assert "Error de carga" in str(exc_info.value)
    finally:
        # Clean up by removing the temporary file
        os.remove(temp_path)
