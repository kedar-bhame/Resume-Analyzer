from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from analyzer import analyze_resume
from chatbot import chatbot_response
from auth import register_user, login_user, verify_token, logout_user

app = Flask(__name__, static_folder='static', static_url_path='/')
CORS(app)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
TEMPLATE_FOLDER = os.path.join(os.path.dirname(__file__), 'templates')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# store last analysis in memory for a simple session-less flow
_last_analysis = None

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/login')
def login_page():
    return app.send_static_file('login.html')

@app.route('/signup')
def signup_page():
    return app.send_static_file('signup.html')

@app.route('/api/upload', methods=['POST'])
def upload_resume():
    global _last_analysis
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    f = request.files['file']
    if f.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    path = os.path.join(UPLOAD_FOLDER, f.filename)
    f.save(path)
    result = analyze_resume(path)
    _last_analysis = result
    return jsonify(result)

@app.route('/api/chat', methods=['POST'])
def chat():
    global _last_analysis
    data = request.json
    q = data.get('message', '')
    # allow client to send an analysis override
    analysis = data.get('analysis') or _last_analysis
    resp = chatbot_response(q, analysis)
    return jsonify({'response': resp})

@app.route('/templates/<path:filename>')
def download_template(filename):
    return send_from_directory(TEMPLATE_FOLDER, filename, as_attachment=True)

# Authentication routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email', '').strip()
    password = data.get('password', '')
    name = data.get('name', '').strip()
    
    if not email or not password or not name:
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400
    
    result = register_user(email, password, name)
    status = 200 if result['success'] else 400
    return jsonify(result), status

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email', '').strip()
    password = data.get('password', '')
    
    if not email or not password:
        return jsonify({'success': False, 'error': 'Missing email or password'}), 400
    
    result = login_user(email, password)
    status = 200 if result['success'] else 401
    return jsonify(result), status

@app.route('/api/auth/verify', methods=['POST'])
def verify():
    data = request.json
    token = data.get('token', '')
    result = verify_token(token)
    return jsonify(result)

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    data = request.json
    token = data.get('token', '')
    result = logout_user(token)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
