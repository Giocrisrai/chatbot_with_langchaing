from fastapi import APIRouter, UploadFile, File
from typing import List, Dict, Union
import logging
import os
from app.services.pdf_processing import process_pdf
from app.services.docx_processing import process_docx
from app.services.pptx_processing import process_pptx
from app.services.xlsx_processing import process_xlsx
from app.services.csv_processing import process_csv
from app.services.file_postprocessing import split_data, create_embeddings_open_source
from app.services.chroma_service import get_chroma_db

router = APIRouter()


@router.post("/multipleupload/")
async def multiple_upload_route(files: List[UploadFile] = File(...)) -> Dict[str, List[Dict[str, Union[str, bool]]]]:
    results = []

    if not files:
        return {"results": results}

    temp_dir = "data/raw"  # Directorio temporal para guardar los archivos
    os.makedirs(temp_dir, exist_ok=True)  # Crear el directorio si no existe

    for file in files:
        unique_filename = file.filename
        file_extension = unique_filename.split(".")[-1].lower()
        file_path = os.path.join(temp_dir, unique_filename)

        supported_extensions = ["pdf", "docx", "pptx", "xlsx", "csv"]
        if file_extension not in supported_extensions:
            error_message = f"Unsupported file extension: {file_extension}"
            logging.error(error_message)
            results.append({"filename": unique_filename,
                            "status": False, "message": error_message})
            continue

        try:
            with open(file_path, "wb") as out_file:
                out_file.write(await file.read())

            if file_extension == "pdf":
                data = process_pdf(file_path)
            elif file_extension == "docx":
                data = process_docx(file_path)
            elif file_extension == "pptx":
                data = process_pptx(file_path)
            elif file_extension == "xlsx":
                data = process_xlsx(file_path)
            elif file_extension == "csv":
                data = process_csv(file_path)

            documents = split_data(data)
            model_name = "all-MiniLM-L6-v2"
            embeddings = create_embeddings_open_source(model_name=model_name)
            get_chroma_db(embeddings, documents, "chroma_docs",
                          recreate_chroma_db=False)

            results.append({"filename": unique_filename, "status": True,
                            "message": "File processed and stored successfully"})
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            logging.exception(error_message)
            results.append({"filename": unique_filename,
                            "status": False, "message": error_message})
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

    return {"results": results}
