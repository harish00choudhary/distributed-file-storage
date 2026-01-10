from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.database import Base

class FileMetadata(Base):
    __tablename__ = "file_metadata"

    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("files.id"))
    filename = Column(String(255))
    chunk_name = Column(String(255))
    storage_node = Column(String(255))
    total_chunks = Column(Integer)
