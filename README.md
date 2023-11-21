# Chatbot with Langchain

This project is an API created with FastAPI that uses Langchain Chroma as a vector database. Its main goal is to process various types of files and allow interaction and conversation with these files through a chatbot.

## Project Structure

The project structure is as follows:

```
chatbot_with_langchain/
├── api/
│ ├── app/
│ │ ├── routers/
│ │ │ ├── check_documents_router.py
│ │ │ ├── file_upload_router.py
│ │ │ └── multiple_upload.py
│ │ └── services/
│ │ ├── chroma_service.py
│ │ ├── csv_processing.py
│ │ ├── docx_processing.py
│ │ ├── file_postprocessing.py
│ │ ├── pdf_processing.py
│ │ ├── pptx_processing.py
│ │ └── xlsx_processing.py
│ └── main.py
├── chroma_docs/
│ ├── cf26b08d-1fbb-4f19-995f-76f991710310/
│ │ ├── data_level0.bin
│ │ ├── header.bin
│ │ ├── length.bin
│ │ └── link_lists.bin
│ └── chroma.sqlite3
├── data/
│ └── raw/
├── LICENSE
├── README.md
├── requirements.txt

```

## Key Features

- **File Processing:** The API can process various types of files, such as PDF, DOCX, PPTX, XLSX, and CSV, extracting information and storing it for later use.

- **Vector Database:** Langchain Chroma is used as a vector database to store vectorized information from processed documents.

- **Interaction with Documents:** The API allows interaction and chat with processed documents, making it easier to search for information and answer questions related to the files.

## Usage

To run the API, follow these steps:

1. Make sure you have the necessary libraries and dependencies installed. You can check them in `requirements.txt`.

2. Run the `main.py` file located in the `api` folder:

cd api
uvicorn main:app --reload

3. The API will be available at `http://localhost:8000`. You can use tools like Postman or cURL to interact with it.

## Contributions

Contributions are welcome. If you want to contribute to this project, follow these steps:

1. Fork the repository.

2. Create a branch for your changes: `git checkout -b feature/new-feature`.

3. Make your changes and commit: `git commit -m "Add new feature"`.

4. Push to your branch: `git push origin feature/new-feature`.

5. Create a pull request on GitHub.

## License

This project is under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contact

If you have any questions or comments, feel free to contact me at 

contact@giocrisrai.com.

https://www.linkedin.com/in/giocrisrai/
