from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List, Dict, Union
import logging
from app.services.pdf_processing import process_pdf
from app.services.docx_processing import process_docx
from app.services.pptx_processing import process_pptx
from app.services.xlsx_processing import process_xlsx
from app.services.csv_processing import process_csv
from app.services.file_postprocessing import split_data, create_embeddings_openai, create_embeddings_open_source
from app.services.chroma_service import get_chroma_db

router = APIRouter()


@router.post("/multipleupload/")
async def multiple_upload_route(files: List[UploadFile] = File(...)) -> Dict[str, Union[str, bool]]:
    """
    Process and store multiple uploaded files, storing their vector representations in Chroma.

    Args:
    - files (List[UploadFile]): List of files to be uploaded.

    Returns:
    - Dict[str, Union[str, bool]]: A dictionary with the results of processing and storing each file.
    """
    results = []
    for file in files:
        unique_filename = file.filename
        file_content = await file.read()
        file_extension = unique_filename.split(".")[-1].lower()

        if file_extension not in ["pdf", "docx", "pptx", "mp3", "m4a", "csv"]:
            logging.error(f"Unsupported file extension: {file_extension}")
            results.append({"filename": unique_filename, "status": "Failed",
                           "message": "Unsupported file extension"})
            continue

        try:
            # Process files based on their type
            if file_extension == "pdf":
                data = process_pdf(file_content, unique_filename)
            elif file_extension == "docx":
                data = process_docx(file_content, unique_filename)
            elif file_extension == "pptx":
                data = process_pptx(file_content, unique_filename)
            elif file_extension == "xlsx":
                data = process_xlsx(file_content, unique_filename)
            elif file_extension == "csv":
                data = process_csv(file_content, unique_filename)

            # Split the data into smaller chunks
            documents = split_data(data)

            # Create embeddings
            model_name = "all-MiniLM-L6-v2"
            embeddings = create_embeddings_open_source(model_name=model_name)

            # Store in Chroma
            vectorstore_chroma = get_chroma_db(
                embeddings, documents, "chroma_docs", recreate_chroma_db=False)

            results.append({"filename": unique_filename, "status": "Success",
                           "message": "File processed and stored in Chroma"})
        except Exception as e:
            logging.exception(f"An error occurred: {str(e)}")
            results.append({"filename": unique_filename, "status": "Failed",
                           "message": "An internal server error occurred"})

    return {"results": results}
