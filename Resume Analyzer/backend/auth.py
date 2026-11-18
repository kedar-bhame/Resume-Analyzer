import json
import os
from datetime import datetime, timedelta
import hashlib
import secrets

# Simple file-based user storage (replace with database in production)
USERS_FILE = os.path.join(os.path.dirname(__file__), 'users.json')

def hash_password(password):
    """Hash password with a salt"""
    salt = secrets.token_hex(16)
    pwd_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return f"{salt}${pwd_hash.hex()}"

def verify_password(password, hashed):
    """Verify password against hash"""
    try:
        salt, pwd_hash = hashed.split('$')
        new_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return new_hash.hex() == pwd_hash
    except:
        return False

def load_users():
    """Load users from JSON file"""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    """Save users to JSON file"""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def register_user(email, password, name):
    """Register a new user and auto-login"""
    users = load_users()
    
    if email in users:
        return {'success': False, 'error': 'Email already exists'}
    
    if len(password) < 6:
        return {'success': False, 'error': 'Password must be at least 6 characters'}
    
    # Generate token for auto-login
    token = secrets.token_urlsafe(32)
    
    users[email] = {
        'name': name,
        'password': hash_password(password),
        'created_at': datetime.now().isoformat(),
        'token': token,
        'token_created': datetime.now().isoformat()
    }
    
    save_users(users)
    return {
        'success': True,
        'message': 'User registered successfully',
        'token': token,
        'name': name,
        'email': email
    }

def login_user(email, password):
    """Login user and return token"""
    users = load_users()
    
    if email not in users:
        return {'success': False, 'error': 'Invalid email or password'}
    
    user = users[email]
    if not verify_password(password, user['password']):
        return {'success': False, 'error': 'Invalid email or password'}
    
    # Generate simple token (in production, use JWT)
    token = secrets.token_urlsafe(32)
    user['token'] = token
    user['token_created'] = datetime.now().isoformat()
    save_users(users)
    
    return {
        'success': True,
        'token': token,
        'name': user['name'],
        'email': email
    }

def verify_token(token):
    """Verify if token is valid"""
    users = load_users()
    for email, user in users.items():
        if user.get('token') == token:
            return {'valid': True, 'email': email, 'name': user['name']}
    return {'valid': False}

def logout_user(token):
    """Logout user by removing token"""
    users = load_users()
    for user in users.values():
        if user.get('token') == token:
            user['token'] = None
            save_users(users)
            return {'success': True}
    return {'success': False}
