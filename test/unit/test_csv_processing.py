import pytest
import os
from unittest.mock import Mock, patch
from langchain.schema.document import Document
from api.app.services.csv_processing import process_csv
import tempfile
from typing import List


@patch('api.app.services.csv_processing.UnstructuredCSVLoader')
def test_process_csv_success(mock_loader: Mock) -> None:
    """
    Test to ensure that the process_csv function correctly processes a simulated CSV.

    This test simulates the behavior of UnstructuredCSVLoader returning mock documents,
    and then checks whether the process_csv function processes these documents as expected.

    Args:
        mock_loader (Mock): A mock object of UnstructuredCSVLoader.
    """
    # Set up simulated behavior
    mock_docs: List[Document] = [
        Document(page_content="Test CSV Content", metadata={
                 "source": "example_data/test.csv"})
    ]
    mock_loader.return_value.load.return_value = mock_docs

    # Create a temporary fake CSV file
    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temp_file:
        temp_path = temp_file.name

    try:
        # Execute the function with the temporary file path
        documents = process_csv(temp_path)

        # Perform assertions
        assert len(documents) == 1
        assert documents[0].page_content == "Test CSV Content"
        assert documents[0].metadata['source'] == 'example_data/test.csv'
    finally:
        # Clean up by removing the temporary file
        os.remove(temp_path)
