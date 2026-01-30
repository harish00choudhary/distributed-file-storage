from fastapi import APIRouter, Depends, HTTPException, Form, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import hashlib

from app.db.database import get_db
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# -------------------- SECURITY UTILS --------------------

def _pre_hash(password: str) -> str:
    """SHA256 pre-hash to avoid bcrypt 72-byte limit"""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def hash_password(password: str) -> str:
    return pwd_context.hash(_pre_hash(password))


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(_pre_hash(plain_password), hashed_password)


# -------------------- REGISTER --------------------

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    user = User(
        username=username,
        email=email,
        hashed_password=hash_password(password)
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "User registered successfully",
        "user_id": user.id,
        "email": user.email
    }


# -------------------- LOGIN --------------------

@router.post("/login")
def login(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    return {
        "message": "Login successful",
        "user_id": user.id,
        "email": user.email
    }
