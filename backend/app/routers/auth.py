from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.database import get_db
from app import models, schemas, auth
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
router = APIRouter()
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        # Check if email already exists
        db_user = auth.get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Check if username already exists
        db_user = auth.get_user_by_username(db, username=user.username)
        if db_user:
            raise HTTPException(status_code=400, detail="Username already taken")
        
        # Create new user
        hashed_password = auth.get_password_hash(user.password)
        db_user = models.User(
            email=user.email,
            username=user.username,
            hashed_password=hashed_password,
            full_name=user.full_name
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        logger.info(f"User registered successfully: {user.username} ({user.email})")
        return db_user
    
    except HTTPException:
        # Re-raise HTTP exceptions (like email/username already taken)
        db.rollback()
        raise
    
    except IntegrityError as e:
        # Handle database constraint violations
        db.rollback()
        logger.error(f"Database integrity error during registration: {str(e)}")
        error_msg = str(e.orig) if hasattr(e, 'orig') else str(e)
        if "email" in error_msg.lower() or "unique constraint" in error_msg.lower():
            raise HTTPException(
                status_code=400,
                detail="Email or username already registered"
            )
        raise HTTPException(
            status_code=400,
            detail="Registration failed due to database constraint violation"
        )
    
    except SQLAlchemyError as e:
        # Handle other database errors
        db.rollback()
        logger.error(f"Database error during registration: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Database error occurred. Please try again later."
        )
    
    except Exception as e:
        # Handle any other unexpected errors
        db.rollback()
        logger.error(f"Unexpected error during registration: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred. Please try again later."
        )

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        user = auth.authenticate_user(db, form_data.username, form_data.password)
        if not user:
            logger.warning(f"Failed login attempt for username: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        logger.info(f"User logged in successfully: {user.username}")
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        # Re-raise HTTP exceptions (like authentication failures)
        raise
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during login. Please try again later."
        )

@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

