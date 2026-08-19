from pathlib import Path
from fastapi import FastAPI, File, Form, UploadFile, HTTPException, status
import uuid
import os
import shutil
app = FastAPI()
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
ALLOWED_COURSES = [
    "Python Basic",
    "FastAPI",
    "Data Analysis",
]

@app.post("/students/register")
async def register_student(
    full_name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...),
    course: str = Form(...),
    avatar: UploadFile = File(...),
):
    if full_name == "":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Full name is required"
        )

    if len(phone) < 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid phone number"
        )

    if course not in ALLOWED_COURSES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Course is not available"
        )
    
    file_ext = avatar.content_type.startswith("image/")
    file_size = avatar.size
    
    
    if not file_ext:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file"
        )
        
    if file_size > 2_000_000_000:
        raise HTTPException(
            status_code=status.HTTP_413_CONTENT_TOO_LARGE,
            detail="File too large"
        )

    file_name = f"{uuid.uuid4()}_{avatar.filename}"
    file_path = os.path.join(UPLOAD_DIR, file_name)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(avatar.file, buffer)

    return {
        "success": True,
        "message": "Registration successful",
        "data": {
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "course": course,
            "avatar": str(file_path),
        },
    }