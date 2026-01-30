# 📦 Distributed File Storage System

A backend system built using **FastAPI** that supports **chunk-based file upload and download**, user authentication, and metadata management using **MySQL**.
The project demonstrates core concepts of **distributed systems**, **large file handling**, and **backend system design**.

---

## 🚀 Features

 🔐 Authentication

* User registration
* Secure password hashing (SHA-256)
* User data stored in MySQL

 📂 File Management

* Chunk-based file upload (supports very large files)
* Distributed storage simulation using multiple storage nodes
* File metadata tracking in MySQL
* File reconstruction and download using stored chunks

 🗄️ Database

* MySQL used for persistent storage
* Separate tables for users, files, and file metadata
* SQLAlchemy ORM integration

---

## 🧠 System Design Overview

### File Upload Flow

1. User uploads a file in chunks
2. Each chunk is saved in a storage node directory
3. Metadata (chunk name, node, file id) is stored in `file_metadata`
4. File-level information is stored in `files`

### File Download Flow

1. File ID is provided
2. Metadata is fetched from database
3. Chunks are merged in order
4. Final file is returned to the user

---

## 🏗️ Project Structure

```text
file_storage_system/
│
├── app/
│   ├── api/
│   │   └── auth.py
│   ├── routers/
│   │   └── files.py
│   ├── services/
│   │   ├── file_service.py
│   │   └── chunk_service.py
│   ├── models/
│   │   ├── user.py
│   │   └── file_metadata.py
│   ├── db/
│   │   └── database.py
│   └── main.py
│
├── storage/
│   ├── node1/
│   └── node2/
│
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

* **Backend:** FastAPI
* **Database:** MySQL
* **ORM:** SQLAlchemy
* **Server:** Uvicorn
* **Language:** Python
* **API Docs:** Swagger (OpenAPI)

---

## 📑 Database Tables

### `users`

| Column   | Description     |
| -------- | --------------- |
| id       | User ID         |
| username | Username        |
| email    | Email           |
| password | Hashed password |

### `files`

| Column     | Description       |
| ---------- | ----------------- |
| id         | File ID           |
| filename   | Original filename |
| owner_id   | User ID           |
| created_at | Upload time       |

### `file_metadata`

| Column       | Description                |
| ------------ | -------------------------- |
| id           | Metadata ID                |
| file_id      | File ID                    |
| chunk_name   | Chunk filename             |
| storage_node | Node where chunk is stored |
| total_chunks | Total chunks of file       |

---

 ▶️ How to Run
    1. 'pip install -r requirements.txt'
    2. 'uvicorn app.main:app --reload'
   
   ### Open API Docs
   -> 'http://127.0.0.1:8000/docs'

---

## 📌 API Endpoints

### Authentication

* `POST /auth/register` → Register new user

### Files

* `POST /files/upload` → Upload file chunks
* `GET /files/download/{file_id}` → Download reconstructed file

---

## ⚠️ Known Limitations

* File downloads currently reconstruct the entire file **in memory**
* Very large files (e.g. >1GB) may cause high memory usage
* Planned improvement: **streaming-based downloads**


---

## 🎯 Learning Outcomes

* Understanding of distributed file systems
* Handling large files using chunking
* Backend API design
* Database schema design
* FastAPI & SQLAlchemy integration
* System scalability considerations

---

## 👨‍💻 Author

**Harish Choudhary**
BTech CSE (AI)

---

⭐ If you like this project, give it a star!
