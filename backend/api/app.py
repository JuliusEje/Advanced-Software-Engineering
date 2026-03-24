from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import requests
from dotenv import load_dotenv
import chardet
from google import genai
from google.genai import types
import pathlib
import uuid
from datetime import datetime
import json
import re
import jwt
from functools import wraps
from supabase import create_client, Client

# Load environment variables
load_dotenv()
API_KEY = os.getenv('GENERATIVE_API_KEY')
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')
JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key-change-in-production')

app = Flask(__name__)
CORS(app, supports_credentials=True)  # Enable CORS for all routes

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'pdf', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def token_required(f):
    """Decorator to protect routes requiring authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({'error': 'Invalid Authorization header'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
            request.user_id = data['user_id']
            request.email = data['email']
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def home():
    return jsonify({'message': 'Resume Optimizer API', 'version': '2.0'}), 200

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'}), 200

@app.route('/resume/upload', methods=['POST'])
@token_required
def resume_upload():
    """Upload and analyze resume - requires authentication"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        if file and allowed_file(file.filename):
            # Generate unique ID
            resume_id = str(uuid.uuid4())
            
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{resume_id}_{filename}")
            file.save(file_path)

            try:
                summary = process_with_google_ai(file_path)
                
                # Parse the summary into structured format
                score_data = parse_ai_summary(summary)
                
                # Store in Supabase instead of memory
                user_id = int(request.user_id)
                resume_record = {
                    'user_id': user_id,
                    'filename': filename,
                    'file_path': file_path,
                    'score': score_data['score'],
                    'feedback': score_data['feedback'],
                    'suggestions': score_data['suggestions'],
                    'created_at': datetime.utcnow().isoformat()
                }
                
                # Insert into Supabase
                response = supabase.table('resumes').insert(resume_record).execute()
                
                if not response.data:
                    return jsonify({'error': 'Failed to save resume data'}), 500
                
                resume_db = response.data[0]
                
                return jsonify({
                    'id': str(resume_db['id']),
                    'message': 'Resume uploaded and analyzed successfully',
                    'score': score_data['score'],
                    'feedback': score_data['feedback'],
                    'suggestions': score_data['suggestions']
                }), 200
            except Exception as e:
                return jsonify({'error': f'AI processing error: {str(e)}'}), 500

        return jsonify({'error': 'Invalid file type'}), 400
    except Exception as e:
        return jsonify({'error': f'Upload error: {str(e)}'}), 500

@app.route('/resume/<resume_id>/score', methods=['GET'])
@token_required
def get_resume_score(resume_id):
    """Get resume score - requires authentication and ownership"""
    try:
        user_id = int(request.user_id)
        
        # Fetch from Supabase with user ownership check
        response = supabase.table('resumes').select('*').eq('id', resume_id).eq('user_id', user_id).execute()
        
        if not response.data:
            return jsonify({'error': 'Resume not found'}), 404
        
        resume_data = response.data[0]
        
        return jsonify({
            'id': str(resume_data['id']),
            'score': resume_data['score'],
            'feedback': resume_data['feedback'],
            'suggestions': resume_data['suggestions'],
            'createdAt': resume_data['created_at']
        }), 200
    except Exception as e:
        return jsonify({'error': f'Error fetching resume: {str(e)}'}), 500

@app.route('/resume/history', methods=['GET'])
@token_required
def get_resume_history():
    """Get all resumes for current user"""
    try:
        user_id = int(request.user_id)
        
        # Fetch all resumes for user, ordered by most recent
        response = supabase.table('resumes').select('id, filename, score, created_at').eq('user_id', user_id).order('created_at', desc=True).execute()
        
        resumes = []
        for resume in response.data:
            resumes.append({
                'id': str(resume['id']),
                'filename': resume['filename'],
                'score': resume['score'],
                'createdAt': resume['created_at']
            })
        
        return jsonify({'resumes': resumes}), 200
    except Exception as e:
        return jsonify({'error': f'Error fetching history: {str(e)}'}), 500

def parse_ai_summary(summary: str) -> dict:
    """
    Parse the AI-generated summary into structured CV optimization data.
    Extracts or generates: score, feedback, and suggestions.
    """
    lines = summary.split('\n')
    
    # Extract score with more specific pattern matching
    score = 75  # Default score
    score_pattern = re.compile(r'Resume Score:\s*(\d+)/100', re.IGNORECASE)
    for line in lines:
        match = score_pattern.search(line)
        if match:
            try:
                potential_score = int(match.group(1))
                if 0 <= potential_score <= 100:
                    score = potential_score
                    break
            except:
                pass
    
    # Extract feedback (look for section starting with "Overall Feedback")
    feedback = "Your resume has been analyzed by our AI system."
    feedback_start = False
    feedback_lines = []
    
    for i, line in enumerate(lines):
        if 'Overall Feedback' in line:
            feedback_start = True
            continue
        
        if feedback_start:
            line = line.strip()
            # Stop at next major section (marked with ###)
            if line.startswith('###') or line.startswith('##'):
                break
            # Skip empty lines at the start of section
            if line and not line.startswith('**Strengths') and not line.startswith('**Weaknesses'):
                if line.startswith('*') or line.startswith('-'):
                    # Skip bullet points under Strengths/Weaknesses
                    continue
                feedback_lines.append(line)
            # Stop after collecting the intro paragraph
            if feedback_lines and line == '':
                break
    
    if feedback_lines:
        feedback = ' '.join([l for l in feedback_lines if l and not l.startswith('**')])
    
    # Extract suggestions from "Specific Improvement Suggestions" section
    suggestions = []
    suggestion_start = False
    
    for i, line in enumerate(lines):
        if 'Specific Improvement Suggestions' in line or 'Improvement Suggestions' in line:
            suggestion_start = True
            continue
        
        if suggestion_start:
            line = line.strip()
            # Look for numbered sections like "**1. Something**" or "#### **1. Something**"
            if re.match(r'#+\s*\*{0,2}\d+\.\s+', line):
                # Extract title of suggestion (remove markdown formatting)
                title = re.sub(r'^#+\s*\*{0,2}\d+\.\s+', '', line)
                title = title.rstrip('*').strip()
                if title:
                    suggestions.append(title)
    
    # If we got suggestions with titles, look for their Action lines
    if suggestions:
        suggestion_idx = 0
        for i, line in enumerate(lines):
            if '**Action:**' in line:
                action = line.replace('**Action:**', '').strip()
                # Clean up markdown formatting
                action = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', action)
                action = action.strip('* ').strip()
                if action and suggestion_idx < len(suggestions):
                    suggestions[suggestion_idx] = f"{suggestions[suggestion_idx]}: {action}"
                    suggestion_idx += 1
    
    # If we don't have enough suggestions, try extracting from Action lines directly
    if len(suggestions) < 3:
        suggestions = []
        for line in lines:
            line = line.strip()
            # Look for action items marked with **Action:**
            if '**Action:**' in line:
                action = line.replace('**Action:**', '').strip()
                # Clean up markdown formatting
                action = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', action)
                action = action.strip('* ').strip()
                if action:
                    # Truncate long actions to ~100 chars
                    if len(action) > 100:
                        action = action[:100].rsplit(' ', 1)[0] + '...'
                    suggestions.append(action)
    
    # Final fallback if still no suggestions
    if len(suggestions) < 3:
        suggestions = [
            "Clarify future dates to avoid confusion about timeline",
            "Add a dedicated Technical Skills section for ATS optimization",
            "Enhance bullet points with more quantifiable metrics",
            "Include a professional summary at the top of your resume",
            "Standardize bullet point formatting and punctuation"
        ]
    
    return {
        'score': score,
        'feedback': feedback,
        'suggestions': suggestions[:5]  # Limit to 5 suggestions
    }

def process_with_google_ai(file_path):
    client = genai.Client(api_key=API_KEY)

    filepath = pathlib.Path(file_path)
    prompt = "Analyze this resume for a CV optimization system. Provide: 1) A resume score (0-100) based on quality and completeness, 2) Overall feedback about the resume, 3) 3-5 specific improvement suggestions. Format your response clearly with sections for each."

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=[
            types.Part.from_bytes(
                data=filepath.read_bytes(),
                mime_type='application/pdf',
            ),
            prompt
        ]
    )

    # Ensure the response is properly handled
    if hasattr(response, 'text'):
        print(response.text)  # Debugging output
        return response.text
    else:
        raise Exception("Unexpected response format: Missing 'text' attribute.")

# Register auth blueprint
from api.auth.routes import auth_bp
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True, port=8000)