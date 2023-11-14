from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List, Dict, Union
import logging
from app.services.pdf_processing import process_pdf
from app.services.chroma_service import store_in_chroma

router = APIRouter()


@router.post("/multipleupload/")
async def multiple_upload_route(files: List[UploadFile] = File(...)) -> Dict[str, Union[str, bool]]:
    """
    Procesa y almacena múltiples archivos subidos, almacenando sus representaciones vectoriales en Chroma.

    Args:
    - files (List[UploadFile]): Lista de archivos a ser subidos.

    Returns:
    - Dict[str, Union[str, bool]]: Un diccionario con los resultados del procesamiento y almacenamiento de cada archivo.
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
            # Procesamiento de archivos según su tipo
            if file_extension == "pdf":
                data = process_pdf(file_content, unique_filename)
            elif file_extension == "docx":
                data = process_docx(file_content, unique_filename)
            # Agregar condiciones para otros tipos de archivo...

            # Almacenamiento en Chroma
            store_result = await store_in_chroma(data, unique_filename)
            results.append({"filename": unique_filename, "status": "Success",
                           "message": "File processed and stored in Chroma"})
        except Exception as e:
            logging.exception(f"An error occurred: {str(e)}")
            results.append({"filename": unique_filename, "status": "Failed",
                           "message": "An internal server error occurred"})

    return {"results": results}
