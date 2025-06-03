#!/usr/bin/env python3
"""
Setup script to ensure there's a user for testing
"""

from cs50 import SQL
from werkzeug.security import generate_password_hash

db = SQL("sqlite:///project.db")

print("=== Current Users in Database ===")
users = db.execute("SELECT id, username FROM users")
if users:
    for user in users:
        print(f"ID: {user['id']}, Username: {user['username']}")
else:
    print("No users found.")

# Create a test user if none exist
if not users:
    print("\n=== Creating Test User ===")
    username = "admin"
    password = "admin123"
    
    try:
        user_id = db.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            username, generate_password_hash(password)
        )
        print(f"✓ Created test user:")
        print(f"  Username: {username}")
        print(f"  Password: {password}")
        print(f"  User ID: {user_id}")
    except Exception as e:
        print(f"✗ Error creating user: {e}")

print("\n=== Application Ready ===")
print("🌐 Open your browser to: http://127.0.0.1:5000")
print("🔑 Use the credentials above to log in")
print("🎉 Enjoy your enhanced Flask Forms application!")
