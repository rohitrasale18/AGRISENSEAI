#!/usr/bin/env python3
"""
Test script for AgriSense AI Authentication System
Tests all authentication features including signup, login, admin panel, and data storage
"""

import requests
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000"
session = requests.Session()

def print_test(test_name, status):
    """Print test result"""
    symbol = "✅" if status else "❌"
    print(f"{symbol} {test_name}")

def test_homepage():
    """Test if homepage loads"""
    try:
        response = session.get(f"{BASE_URL}/")
        success = response.status_code == 200 and "AgriSense AI" in response.text
        print_test("Homepage loads successfully", success)
        return success
    except Exception as e:
        print_test(f"Homepage loads successfully - Error: {e}", False)
        return False

def test_login_page():
    """Test if login page loads"""
    try:
        response = session.get(f"{BASE_URL}/login")
        success = response.status_code == 200 and "Login to AgriSense AI" in response.text
        print_test("Login page loads", success)
        return success
    except Exception as e:
        print_test(f"Login page loads - Error: {e}", False)
        return False

def test_signup_page():
    """Test if signup page loads"""
    try:
        response = session.get(f"{BASE_URL}/signup")
        success = response.status_code == 200 and "Sign Up for AgriSense AI" in response.text
        print_test("Signup page loads", success)
        return success
    except Exception as e:
        print_test(f"Signup page loads - Error: {e}", False)
        return False

def test_signup():
    """Test user signup"""
    try:
        test_email = f"testuser{datetime.now().timestamp()}@test.com"
        data = {
            'name': 'Test User',
            'email': test_email,
            'password': 'testpass123'
        }
        response = session.post(f"{BASE_URL}/signup", data=data, allow_redirects=True)
        success = response.status_code == 200 and ("Account created successfully" in response.text or "Login" in response.text)
        print_test("User signup works", success)
        return success, test_email
    except Exception as e:
        print_test(f"User signup works - Error: {e}", False)
        return False, None

def test_admin_login():
    """Test admin login"""
    try:
        data = {
            'email': 'admin@agrisense.com',
            'password': 'admin123'
        }
        response = session.post(f"{BASE_URL}/login", data=data, allow_redirects=True)
        success = response.status_code == 200 and "Admin" in response.text
        print_test("Admin login works", success)
        return success
    except Exception as e:
        print_test(f"Admin login works - Error: {e}", False)
        return False

def test_admin_dashboard():
    """Test admin dashboard access"""
    try:
        response = session.get(f"{BASE_URL}/admin")
        success = response.status_code == 200 and "Admin Dashboard" in response.text
        print_test("Admin dashboard accessible", success)
        return success
    except Exception as e:
        print_test(f"Admin dashboard accessible - Error: {e}", False)
        return False

def test_logout():
    """Test logout functionality"""
    try:
        response = session.get(f"{BASE_URL}/logout", allow_redirects=True)
        success = response.status_code == 200
        print_test("Logout works", success)
        return success
    except Exception as e:
        print_test(f"Logout works - Error: {e}", False)
        return False

def test_protected_routes():
    """Test that protected routes require login"""
    try:
        # Try to access crop recommendation without login
        response = session.get(f"{BASE_URL}/crop-recommend", allow_redirects=False)
        success = response.status_code in [302, 401]  # Should redirect to login
        print_test("Protected routes require authentication", success)
        return success
    except Exception as e:
        print_test(f"Protected routes require authentication - Error: {e}", False)
        return False

def test_navigation():
    """Test navigation shows correct links"""
    try:
        # Check navigation before login
        response = session.get(f"{BASE_URL}/")
        has_login_button = "Login" in response.text and "Sign Up" in response.text
        print_test("Navigation shows Login/Signup when not authenticated", has_login_button)
        return has_login_button
    except Exception as e:
        print_test(f"Navigation test - Error: {e}", False)
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("AgriSense AI - Authentication System Test Suite")
    print("=" * 60)
    print()
    
    print("📋 Running Tests...")
    print("-" * 60)
    
    # Run tests
    results = []
    
    # Basic page tests
    results.append(test_homepage())
    results.append(test_login_page())
    results.append(test_signup_page())
    
    # Navigation test
    results.append(test_navigation())
    
    # Signup test
    signup_success, test_email = test_signup()
    results.append(signup_success)
    
    # Protected routes test
    results.append(test_protected_routes())
    
    # Admin tests
    results.append(test_admin_login())
    results.append(test_admin_dashboard())
    results.append(test_logout())
    
    print()
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Authentication system is working correctly.")
    else:
        print(f"⚠️  {total - passed} test(s) failed. Please review the errors above.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
