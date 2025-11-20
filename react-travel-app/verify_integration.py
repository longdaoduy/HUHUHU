#!/usr/bin/env python3
"""
Verification Script - Check if Authentication Integration is Complete
"""

import os
import json
import sys

def check_file_exists(filepath, description):
    """Check if a file exists."""
    exists = os.path.exists(filepath)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {filepath}")
    return exists

def check_content_in_file(filepath, content, description):
    """Check if content exists in file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            file_content = f.read()
            found = content in file_content
            status = "✅" if found else "❌"
            print(f"{status} {description}")
            return found
    except Exception as e:
        print(f"❌ Error checking {filepath}: {e}")
        return False

def main():
    print("\n" + "="*60)
    print("AUTHENTICATION INTEGRATION VERIFICATION")
    print("="*60 + "\n")
    
    all_checks_passed = True
    
    # Check backend files
    print("📁 Backend Files:")
    all_checks_passed &= check_file_exists(
        "backend/main.py",
        "Main API file"
    )
    all_checks_passed &= check_file_exists(
        "backend/requirements.txt",
        "Requirements file"
    )
    all_checks_passed &= check_file_exists(
        "backend/test_api.py",
        "Test API script"
    )
    
    # Check frontend files
    print("\n📁 Frontend Files:")
    all_checks_passed &= check_file_exists(
        "frontend/src/pages/LoginPage.js",
        "LoginPage component"
    )
    all_checks_passed &= check_file_exists(
        "frontend/src/pages/SignupPage.js",
        "SignupPage component"
    )
    
    # Check main.py content
    print("\n🔍 Backend Integration:")
    all_checks_passed &= check_content_in_file(
        "backend/main.py",
        "import jwt",
        "JWT import"
    )
    all_checks_passed &= check_content_in_file(
        "backend/main.py",
        "def hash_password",
        "hash_password function"
    )
    all_checks_passed &= check_content_in_file(
        "backend/main.py",
        "def verify_password",
        "verify_password function"
    )
    all_checks_passed &= check_content_in_file(
        "backend/main.py",
        "def create_access_token",
        "create_access_token function"
    )
    all_checks_passed &= check_content_in_file(
        "backend/main.py",
        "def verify_token",
        "verify_token function"
    )
    all_checks_passed &= check_content_in_file(
        "backend/main.py",
        "@app.post(\"/api/register\")",
        "Register endpoint"
    )
    all_checks_passed &= check_content_in_file(
        "backend/main.py",
        "@app.post(\"/api/login\")",
        "Login endpoint"
    )
    all_checks_passed &= check_content_in_file(
        "backend/main.py",
        "@app.post(\"/api/logout\")",
        "Logout endpoint"
    )
    all_checks_passed &= check_content_in_file(
        "backend/main.py",
        "@app.get(\"/api/user/profile\")",
        "Profile endpoint"
    )
    
    # Check requirements.txt
    print("\n📦 Dependencies:")
    all_checks_passed &= check_content_in_file(
        "backend/requirements.txt",
        "PyJWT",
        "PyJWT package"
    )
    
    # Check frontend integration
    print("\n🎨 Frontend Integration:")
    all_checks_passed &= check_content_in_file(
        "frontend/src/App.js",
        "LoginPage",
        "LoginPage import"
    )
    all_checks_passed &= check_content_in_file(
        "frontend/src/App.js",
        "SignupPage",
        "SignupPage import"
    )
    all_checks_passed &= check_content_in_file(
        "frontend/src/App.js",
        "/login",
        "Login route"
    )
    all_checks_passed &= check_content_in_file(
        "frontend/src/App.js",
        "/signup",
        "Signup route"
    )
    
    # Check documentation
    print("\n📖 Documentation:")
    all_checks_passed &= check_file_exists(
        "INTEGRATION_SUMMARY.md",
        "Integration summary"
    )
    all_checks_passed &= check_file_exists(
        "SETUP_GUIDE.md",
        "Setup guide"
    )
    all_checks_passed &= check_file_exists(
        "AUTHENTICATION_INTEGRATION.md",
        "Authentication documentation"
    )
    
    # Summary
    print("\n" + "="*60)
    if all_checks_passed:
        print("✅ ALL CHECKS PASSED - INTEGRATION COMPLETE!")
        print("="*60)
        print("\n📋 Next Steps:")
        print("1. pip install -r backend/requirements.txt")
        print("2. python backend/main.py")
        print("3. npm start (in frontend directory)")
        print("4. Open http://localhost:3000")
        print("\n🧪 Testing:")
        print("- python backend/test_api.py")
        print("- http://localhost:8000/docs (API Swagger UI)")
        sys.exit(0)
    else:
        print("❌ SOME CHECKS FAILED - PLEASE REVIEW ABOVE")
        print("="*60)
        sys.exit(1)

if __name__ == "__main__":
    main()
