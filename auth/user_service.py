from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database.models import User
from .auth_utils import hash_password, verify_password

class UserService:
    """Service class for user-related operations."""
    
    @staticmethod
    def create_user(
        db: Session,
        email: str,
        username: str,
        password: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None
    ) -> Optional[User]:
        """
        Create a new user in the database.
        
        Args:
            db: Database session
            email: User's email address
            username: User's username
            password: Plain text password
            first_name: Optional first name
            last_name: Optional last name
            
        Returns:
            Created User object or None if creation failed
        """
        try:
            hashed_password = hash_password(password)
            
            user = User(
                email=email,
                username=username,
                password_hash=hashed_password,
                first_name=first_name,
                last_name=last_name
            )
            
            db.add(user)
            db.commit()
            db.refresh(user)
            
            # Set mem0_user_id after commit when ID is available
            user.mem0_user_id = user.get_mem0_user_id()
            db.commit()
            
            return user
        except IntegrityError as e:
            db.rollback()
            print(f"User creation failed - duplicate email or username: {e}")
            return None
        except Exception as e:
            db.rollback()
            print(f"User creation failed: {e}")
            return None
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Get user by email address."""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """Get user by username."""
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: str) -> Optional[User]:
        """Get user by ID."""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def authenticate_user(
        db: Session,
        username_or_email: str,
        password: str
    ) -> Optional[User]:
        """
        Authenticate a user by username/email and password.
        
        Args:
            db: Database session
            username_or_email: Username or email to authenticate with
            password: Plain text password
            
        Returns:
            User object if authentication successful, None otherwise
        """
        user = UserService.get_user_by_email(db, username_or_email)
        if not user:
            user = UserService.get_user_by_username(db, username_or_email)
        
        if not user:
            return None
        
        if not verify_password(password, user.password_hash):
            return None
        
        user.last_login = datetime.utcnow()
        db.commit()
        
        return user
    
    @staticmethod
    def update_user(
        db: Session,
        user: User,
        **kwargs
    ) -> User:
        """
        Update user fields.
        
        Args:
            db: Database session
            user: User object to update
            **kwargs: Fields to update
            
        Returns:
            Updated User object
        """
        for key, value in kwargs.items():
            if hasattr(user, key) and key != 'id':
                setattr(user, key, value)
        
        user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def delete_user(db: Session, user: User) -> bool:
        """
        Delete a user (soft delete by setting is_active to False).
        
        Args:
            db: Database session
            user: User object to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            user.is_active = False
            user.updated_at = datetime.utcnow()
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            print(f"User deletion failed: {e}")
            return False