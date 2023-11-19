import pytest
import os
from unittest.mock import Mock, patch
from langchain.schema.document import Document
from api.app.services.pptx_processing import process_pptx
import tempfile


@patch('api.app.services.pptx_processing.UnstructuredPowerPointLoader')
def test_process_pptx_success(mock_loader: Mock) -> None:
    """
    Test to ensure that the process_pptx function correctly processes a simulated PowerPoint file.

    This test simulates the behavior of UnstructuredPowerPointLoader returning mock documents,
    and then checks whether the process_pptx function processes these documents as expected.

    Args:
        mock_loader (Mock): A mock object of UnstructuredPowerPointLoader.
    """
    # Set up simulated behavior
    mock_docs: List[Document] = [
        Document(page_content="Test Content 1", metadata={"slide": 1}),
        Document(page_content="Test Content 2", metadata={"slide": 2})
    ]
    mock_loader.return_value.load.return_value = mock_docs

    # Create a temporary fake .pptx file
    with tempfile.NamedTemporaryFile(suffix=".pptx", delete=False) as temp_file:
        temp_path = temp_file.name

    try:
        # Execute the function with the temporary file path
        slides = process_pptx(temp_path)

        # Perform assertions
        assert len(slides) == 2
        assert slides[0].page_content == "Test Content 1"
        assert slides[1].page_content == "Test Content 2"
        assert slides[0].metadata["slide"] == 1
        assert slides[1].metadata["slide"] == 2
    finally:
        # Clean up by removing the temporary file
        os.remove(temp_path)


@patch('api.app.services.pptx_processing.UnstructuredPowerPointLoader')
def test_process_pptx_error(mock_loader: Mock) -> None:
    """
    Test the error handling in the process_pptx function.

    This test simulates a situation where UnstructuredPowerPointLoader throws an exception,
    and then checks whether the process_pptx function correctly propagates this exception.

    Args:
        mock_loader (Mock): A mock object of UnstructuredPowerPointLoader.
    """
    # Set up the mock to throw an exception
    mock_loader.return_value.load.side_effect = Exception("Error de carga")

    # Create a temporary fake .pptx file
    with tempfile.NamedTemporaryFile(suffix=".pptx", delete=False) as temp_file:
        temp_path = temp_file.name

    try:
        # Verify that an exception is thrown as expected
        with pytest.raises(Exception) as exc_info:
            process_pptx(temp_path)
        assert "Error de carga" in str(exc_info.value)
    finally:
        # Clean up by removing the temporary file
        os.remove(temp_path)
