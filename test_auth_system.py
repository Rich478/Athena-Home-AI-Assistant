#!/usr/bin/env python
"""
Quick test script for the authentication system.
Run this to verify Phase 1 implementation is working.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from database.connection import get_db, init_db
from auth.user_service import UserService
from auth.auth_utils import create_access_token, verify_token

def test_auth_system():
    """Test the authentication system with a simple flow."""
    print("\n" + "="*60)
    print("TESTING AUTHENTICATION SYSTEM")
    print("="*60 + "\n")
    
    # Initialize database
    print("1. Initializing database...")
    init_db()
    
    # Get database session
    db = next(get_db())
    
    # Test user creation
    print("2. Creating test user...")
    test_user = UserService.create_user(
        db=db,
        email="test@family.com",
        username="testfamily",
        password="SecurePassword123",
        first_name="Test",
        last_name="Family"
    )
    
    if test_user:
        print(f"   [SUCCESS] User created: {test_user.username}")
        print(f"   - ID: {test_user.id}")
        print(f"   - Mem0 ID: {test_user.mem0_user_id}")
    else:
        print("   [FAILED] User creation failed")
        return False
    
    # Test authentication
    print("\n3. Testing authentication...")
    authenticated = UserService.authenticate_user(
        db=db,
        username_or_email="testfamily",
        password="SecurePassword123"
    )
    
    if authenticated:
        print(f"   [SUCCESS] Authentication successful for: {authenticated.username}")
    else:
        print("   [FAILED] Authentication failed")
        return False
    
    # Test JWT token
    print("\n4. Testing JWT token generation...")
    token = create_access_token({
        "user_id": authenticated.id,
        "username": authenticated.username
    })
    print(f"   [SUCCESS] Token generated (length: {len(token)})")
    
    # Verify token
    print("\n5. Verifying JWT token...")
    decoded = verify_token(token)
    if decoded and decoded.get("user_id") == authenticated.id:
        print(f"   [SUCCESS] Token verified for user: {decoded.get('username')}")
    else:
        print("   [FAILED] Token verification failed")
        return False
    
    # Test duplicate prevention
    print("\n6. Testing duplicate prevention...")
    duplicate_user = UserService.create_user(
        db=db,
        email="test@family.com",
        username="differentname",
        password="AnotherPassword"
    )
    
    if duplicate_user is None:
        print("   [SUCCESS] Duplicate email prevented")
    else:
        print("   [FAILED] Duplicate was not prevented")
        return False
    
    # Clean up
    print("\n7. Cleaning up test data...")
    UserService.delete_user(db, test_user)
    print("   [SUCCESS] Test user marked as inactive")
    
    db.close()
    
    print("\n" + "="*60)
    print("[SUCCESS] ALL AUTHENTICATION TESTS PASSED!")
    print("="*60 + "\n")
    
    return True

if __name__ == "__main__":
    success = test_auth_system()
    sys.exit(0 if success else 1)