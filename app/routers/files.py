from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.file_metadata import FileMetadata
from app.models.file import File as FileModel
from app.services.file_service import merge_chunks
import os
import random

router = APIRouter(prefix="/files", tags=["Files"])

# -------------------- ABSOLUTE STORAGE PATH --------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
STORAGE_ROOT = os.path.join(BASE_DIR, "storage")

STORAGE_NODES = [
    os.path.join(STORAGE_ROOT, "node1"),
    os.path.join(STORAGE_ROOT, "node2"),
    os.path.join(STORAGE_ROOT, "node3"),
]

# Create folders if missing
for node in STORAGE_NODES:
    os.makedirs(node, exist_ok=True)

# -------------------- START UPLOAD --------------------
@router.post("/start-upload")
def start_upload(
    filename: str = Form(...),
    user_id: int = Form(...),  # later replace with JWT
    db: Session = Depends(get_db)
):
    new_file = FileModel(
        filename=filename,
        owner_id=user_id
    )

    db.add(new_file)
    db.commit()
    db.refresh(new_file)

    return {
        "message": "File upload initialized",
        "file_id": new_file.id
    }

# -------------------- UPLOAD CHUNK --------------------
@router.post("/upload")
async def upload_chunk(
    file: UploadFile = File(...),
    file_id: int = Form(...),
    chunk_index: int = Form(...),
    total_chunks: int = Form(...),
    db: Session = Depends(get_db)
):
    node = random.choice(STORAGE_NODES)
    chunk_name = f"{file.filename}.part{chunk_index}"
    chunk_path = os.path.join(node, chunk_name)

    # Save chunk
    with open(chunk_path, "wb") as f:
        f.write(await file.read())

    metadata = FileMetadata(
        file_id=file_id,
        filename=file.filename,
        chunk_name=chunk_name,
        storage_node=node,
        total_chunks=total_chunks
    )

    db.add(metadata)
    db.commit()

    return {
        "message": "Chunk stored successfully",
        "node": os.path.basename(node),
        "chunk_index": chunk_index
    }

# -------------------- DOWNLOAD --------------------
@router.get("/download/{file_id}")
def download_file(file_id: int, db: Session = Depends(get_db)):
    try:
        output_path = merge_chunks(file_id, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return FileResponse(
        path=output_path,
        media_type="application/octet-stream",
        filename=os.path.basename(output_path)
    )
