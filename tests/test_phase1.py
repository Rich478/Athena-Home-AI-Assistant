"""
Comprehensive tests for Phase 1: Database & User Model
Tests database setup, user creation, authentication, and password hashing.
"""

import unittest
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.connection import Base, get_db, init_db
from database.models import User
from auth.auth_utils import hash_password, verify_password, create_access_token, verify_token
from auth.user_service import UserService

class TestPhase1(unittest.TestCase):
    """Test suite for Phase 1 implementation."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test database for all tests."""
        cls.test_db_path = "test_athena_users.db"
        cls.engine = create_engine(
            f"sqlite:///./{cls.test_db_path}",
            connect_args={"check_same_thread": False}
        )
        cls.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=cls.engine)
        Base.metadata.create_all(bind=cls.engine)
        
    @classmethod
    def tearDownClass(cls):
        """Clean up test database after all tests."""
        cls.engine.dispose()  # Close all connections
        if os.path.exists(cls.test_db_path):
            try:
                os.remove(cls.test_db_path)
            except PermissionError:
                pass  # Windows sometimes holds the file briefly
    
    def setUp(self):
        """Set up each test with a fresh session."""
        self.db = self.SessionLocal()
        
    def tearDown(self):
        """Clean up after each test."""
        self.db.query(User).delete()
        self.db.commit()
        self.db.close()
    
    def test_database_connection(self):
        """Test 1: Database connection and table creation."""
        tables = Base.metadata.tables
        self.assertIn('users', tables)
        print("[PASS] Test 1: Database connection and users table created")
    
    def test_user_model_creation(self):
        """Test 2: User model creation with all fields."""
        user = User(
            email="test@example.com",
            username="testuser",
            password_hash="hashed_password",
            first_name="John",
            last_name="Doe"
        )
        
        self.db.add(user)
        self.db.commit()
        
        retrieved_user = self.db.query(User).filter_by(email="test@example.com").first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.username, "testuser")
        self.assertEqual(retrieved_user.first_name, "John")
        self.assertEqual(retrieved_user.last_name, "Doe")
        self.assertTrue(retrieved_user.is_active)
        self.assertFalse(retrieved_user.is_verified)
        print("[PASS] Test 2: User model created with all fields")
    
    def test_password_hashing(self):
        """Test 3: Password hashing and verification."""
        password = "SecurePassword123!"
        hashed = hash_password(password)
        
        self.assertNotEqual(password, hashed)
        self.assertTrue(verify_password(password, hashed))
        self.assertFalse(verify_password("WrongPassword", hashed))
        print("[PASS] Test 3: Password hashing and verification working")
    
    def test_jwt_token_creation_and_verification(self):
        """Test 4: JWT token creation and verification."""
        user_data = {"user_id": "test-user-123", "username": "testuser"}
        token = create_access_token(user_data)
        
        self.assertIsNotNone(token)
        self.assertIsInstance(token, str)
        
        decoded = verify_token(token)
        self.assertIsNotNone(decoded)
        self.assertEqual(decoded["user_id"], "test-user-123")
        self.assertEqual(decoded["username"], "testuser")
        
        invalid_token = "invalid.token.here"
        self.assertIsNone(verify_token(invalid_token))
        print("[PASS] Test 4: JWT token creation and verification working")
    
    def test_user_service_create_user(self):
        """Test 5: UserService create_user functionality."""
        user = UserService.create_user(
            db=self.db,
            email="service@example.com",
            username="serviceuser",
            password="TestPassword123",
            first_name="Jane",
            last_name="Smith"
        )
        
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "service@example.com")
        self.assertEqual(user.username, "serviceuser")
        self.assertIsNotNone(user.password_hash)
        self.assertNotEqual(user.password_hash, "TestPassword123")
        self.assertIsNotNone(user.mem0_user_id)
        self.assertTrue(user.mem0_user_id.startswith("user_"))
        print("[PASS] Test 5: UserService create_user working")
    
    def test_user_service_duplicate_prevention(self):
        """Test 6: Duplicate email/username prevention."""
        user1 = UserService.create_user(
            db=self.db,
            email="duplicate@example.com",
            username="uniqueuser1",
            password="Password123"
        )
        self.assertIsNotNone(user1)
        
        user2 = UserService.create_user(
            db=self.db,
            email="duplicate@example.com",  # Duplicate email
            username="uniqueuser2",
            password="Password123"
        )
        self.assertIsNone(user2)
        
        user3 = UserService.create_user(
            db=self.db,
            email="unique@example.com",
            username="uniqueuser1",  # Duplicate username
            password="Password123"
        )
        self.assertIsNone(user3)
        print("[PASS] Test 6: Duplicate email/username prevention working")
    
    def test_user_service_authentication(self):
        """Test 7: User authentication with email and username."""
        UserService.create_user(
            db=self.db,
            email="auth@example.com",
            username="authuser",
            password="CorrectPassword"
        )
        
        user_by_email = UserService.authenticate_user(
            db=self.db,
            username_or_email="auth@example.com",
            password="CorrectPassword"
        )
        self.assertIsNotNone(user_by_email)
        self.assertEqual(user_by_email.username, "authuser")
        
        user_by_username = UserService.authenticate_user(
            db=self.db,
            username_or_email="authuser",
            password="CorrectPassword"
        )
        self.assertIsNotNone(user_by_username)
        self.assertEqual(user_by_username.email, "auth@example.com")
        
        wrong_password = UserService.authenticate_user(
            db=self.db,
            username_or_email="authuser",
            password="WrongPassword"
        )
        self.assertIsNone(wrong_password)
        
        nonexistent = UserService.authenticate_user(
            db=self.db,
            username_or_email="nonexistent",
            password="AnyPassword"
        )
        self.assertIsNone(nonexistent)
        print("[PASS] Test 7: User authentication working")
    
    def test_user_service_get_methods(self):
        """Test 8: UserService get_user methods."""
        created_user = UserService.create_user(
            db=self.db,
            email="getter@example.com",
            username="getteruser",
            password="Password123"
        )
        
        by_id = UserService.get_user_by_id(self.db, created_user.id)
        self.assertIsNotNone(by_id)
        self.assertEqual(by_id.email, "getter@example.com")
        
        by_email = UserService.get_user_by_email(self.db, "getter@example.com")
        self.assertIsNotNone(by_email)
        self.assertEqual(by_email.username, "getteruser")
        
        by_username = UserService.get_user_by_username(self.db, "getteruser")
        self.assertIsNotNone(by_username)
        self.assertEqual(by_username.email, "getter@example.com")
        print("[PASS] Test 8: UserService get methods working")
    
    def test_user_service_update_user(self):
        """Test 9: UserService update_user functionality."""
        user = UserService.create_user(
            db=self.db,
            email="update@example.com",
            username="updateuser",
            password="Password123"
        )
        
        updated_user = UserService.update_user(
            db=self.db,
            user=user,
            first_name="Updated",
            last_name="Name",
            is_verified=True
        )
        
        self.assertEqual(updated_user.first_name, "Updated")
        self.assertEqual(updated_user.last_name, "Name")
        self.assertTrue(updated_user.is_verified)
        print("[PASS] Test 9: UserService update_user working")
    
    def test_user_service_delete_user(self):
        """Test 10: UserService soft delete functionality."""
        user = UserService.create_user(
            db=self.db,
            email="delete@example.com",
            username="deleteuser",
            password="Password123"
        )
        
        self.assertTrue(user.is_active)
        
        result = UserService.delete_user(self.db, user)
        self.assertTrue(result)
        
        deleted_user = UserService.get_user_by_id(self.db, user.id)
        self.assertIsNotNone(deleted_user)
        self.assertFalse(deleted_user.is_active)
        print("[PASS] Test 10: UserService soft delete working")
    
    def test_mem0_user_id_generation(self):
        """Test 11: Mem0 user ID generation."""
        user = UserService.create_user(
            db=self.db,
            email="mem0@example.com",
            username="mem0user",
            password="Password123"
        )
        
        mem0_id = user.get_mem0_user_id()
        self.assertIsNotNone(mem0_id)
        self.assertEqual(mem0_id, f"user_{user.id}")
        self.assertEqual(mem0_id, user.mem0_user_id)
        print("[PASS] Test 11: Mem0 user ID generation working")
    
    def test_user_to_dict_serialization(self):
        """Test 12: User to_dict serialization."""
        user = UserService.create_user(
            db=self.db,
            email="serial@example.com",
            username="serialuser",
            password="Password123",
            first_name="Serial",
            last_name="User"
        )
        
        user_dict = user.to_dict()
        
        self.assertIsInstance(user_dict, dict)
        self.assertEqual(user_dict["email"], "serial@example.com")
        self.assertEqual(user_dict["username"], "serialuser")
        self.assertEqual(user_dict["first_name"], "Serial")
        self.assertEqual(user_dict["last_name"], "User")
        self.assertIn("id", user_dict)
        self.assertIn("created_at", user_dict)
        self.assertNotIn("password_hash", user_dict)
        print("[PASS] Test 12: User serialization working")

def run_tests():
    """Run all Phase 1 tests."""
    print("\n" + "="*60)
    print("RUNNING PHASE 1 TESTS: Database & User Model")
    print("="*60 + "\n")
    
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestPhase1)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    print("\n" + "="*60)
    if result.wasSuccessful():
        print("[SUCCESS] ALL PHASE 1 TESTS PASSED!")
    else:
        print(f"[FAILED] TESTS FAILED: {len(result.failures)} failures, {len(result.errors)} errors")
    print("="*60 + "\n")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)