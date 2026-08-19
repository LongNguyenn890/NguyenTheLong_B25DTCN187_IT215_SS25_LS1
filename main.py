import os
from fastapi import FastAPI, File, Form, UploadFile, HTTPException, status
from fastapi.staticfiles import StaticFiles
import uuid
import shutil
from pathlib import Path
app = FastAPI()
UPLOAD_FOLDER = Path("storage/documents")
UPLOAD_FOLDER.mkdir(parents = True, exist_ok=True)

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".doc",
    ".docx",
    ".ppt",
    ".pptx",
}

ALLOWED_DOCUMENT_TYPES = {
    "lecture",
    "assignment",
    "reference",
    "exam",
}

@app.post("/documents")
async def upload_document(
    title: str = Form(...),
    course_code: str = Form(...),
    document_type: str = Form(...),
    description: str = Form(""),
    document: UploadFile = File(...),
):
    if not document.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File name is required"
        )

    original_filename = document.filename
    extension = Path(original_filename).suffix.lower()
    
    if not extension:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must have an extension"
        )
    
    if extension not in ALLOWED_EXTENSIONS:
        return {
            "success": False,
            "message": "File type is not allowed",
        }
        
        
    if document.size == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is not empty"
        )
        
    
        
    file_name = f"{uuid.uuid4()}_{document.filename}"
    file_path = os.path.join(
        UPLOAD_FOLDER,
        file_name,
    )


    with open(file_path, "wb") as output_file:
        shutil.copyfileobj(document.file, output_file)

    return {
        "success": True,
        "data": {
            "title": title,
            "course_code": course_code.upper(),
            "document_type": document_type,
            "description": description,
            "file_path": file_path,
        },
    }