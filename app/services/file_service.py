import os
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.file_metadata import FileMetadata

STORAGE_NODES = [
    "app/storage/node1",
    "app/storage/node2",
    "app/storage/node3"
]

def merge_chunks(file_id: int, db: Session):
    file_meta = db.query(FileMetadata).filter(FileMetadata.id == file_id).first()

    if not file_meta:
        raise HTTPException(status_code=404, detail="File not found")

    output_path = f"app/storage/merged_{file_meta.filename}"

    with open(output_path, "wb") as output_file:
        for i in range(file_meta.total_chunks):
            chunk_found = False
            chunk_name = f"{file_meta.filename}.part{i}"

            for node in STORAGE_NODES:
                chunk_path = os.path.join(node, chunk_name)
                if os.path.exists(chunk_path):
                    with open(chunk_path, "rb") as chunk:
                        output_file.write(chunk.read())
                    chunk_found = True
                    break

            if not chunk_found:
                raise HTTPException(
                    status_code=500,
                    detail=f"Chunk {i} missing. File corrupted."
                )

    return output_path
