import os
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.file_metadata import FileMetadata

def merge_chunks(file_id: int, db: Session) -> str:
    chunks = (
        db.query(FileMetadata)
        .filter(FileMetadata.file_id == file_id)
        .order_by(FileMetadata.chunk_name)
        .all()
    )

    if not chunks:
        raise HTTPException(status_code=404, detail="No chunks found")

    total_chunks = chunks[0].total_chunks

    # ---- BASE PATH (PROJECT ROOT) ----
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    STORAGE_ROOT = os.path.join(BASE_DIR, "storage")

    output_filename = f"merged_{chunks[0].filename}"
    output_path = os.path.join(STORAGE_ROOT, output_filename)

    with open(output_path, "wb") as output_file:
        for i in range(total_chunks):
            chunk = next(
                (c for c in chunks if c.chunk_name.endswith(f".part{i}")),
                None
            )

            if not chunk:
                raise HTTPException(
                    status_code=500,
                    detail=f"Chunk {i} missing. File corrupted."
                )

            chunk_path = os.path.join(chunk.storage_node, chunk.chunk_name)

            if not os.path.exists(chunk_path):
                raise HTTPException(
                    status_code=500,
                    detail=f"Chunk file missing: {chunk_path}"
                )

            with open(chunk_path, "rb") as f:
                output_file.write(f.read())

    return output_path
