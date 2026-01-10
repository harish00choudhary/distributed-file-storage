import os

CHUNK_SIZE = 1024 * 1024  # 1MB

def split_file(file_bytes: bytes):
    chunks = []
    for i in range(0, len(file_bytes), CHUNK_SIZE):
        chunks.append(file_bytes[i:i + CHUNK_SIZE])
    return chunks
