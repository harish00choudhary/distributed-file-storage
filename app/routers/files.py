from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import os
import uuid

router = APIRouter(prefix="/files", tags=["Files"])

BASE_STORAGE = "storage"

os.makedirs(BASE_STORAGE, exist_ok=True)


@router.post("/upload")
async def upload_chunk(
    file: UploadFile = File(...),
    file_id: str = Form(...),
    chunk_index: int = Form(...),
):
    file_dir = os.path.join(BASE_STORAGE, file_id)
    os.makedirs(file_dir, exist_ok=True)

    chunk_path = os.path.join(file_dir, f"chunk_{chunk_index}")

    with open(chunk_path, "wb") as f:
        content = await file.read()
        f.write(content)

    return {
        "message": "Chunk uploaded",
        "file_id": file_id,
        "chunk_index": chunk_index
    }
from fastapi.responses import FileResponse

@router.get("/download/{file_id}")
def download_file(file_id: str):
    file_dir = os.path.join(BASE_STORAGE, file_id)

    if not os.path.exists(file_dir):
        raise HTTPException(status_code=404, detail="File not found")

    output_file = os.path.join(BASE_STORAGE, f"{file_id}_final")

    with open(output_file, "wb") as outfile:
        for chunk_name in sorted(os.listdir(file_dir)):
            chunk_path = os.path.join(file_dir, chunk_name)
            with open(chunk_path, "rb") as infile:
                outfile.write(infile.read())

    return FileResponse(
        output_file,
        filename=f"{file_id}.bin",
        media_type="application/octet-stream"
    )
