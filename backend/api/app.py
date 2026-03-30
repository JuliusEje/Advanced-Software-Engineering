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
            resume_id = str(uuid.uuid4())
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{resume_id}_{filename}")
            file.save(file_path)

            try:
                user_id = int(request.user_id)

                # Upload to Supabase Storage
                storage_path = f"{user_id}/{resume_id}/{filename}"
                mime_type = 'application/pdf' if filename.endswith('.pdf') else 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

                with open(file_path, 'rb') as f:
                    file_bytes = f.read()

                try:
                    upload_response = supabase.storage.from_('resumes').upload(
                        path=storage_path,
                        file=file_bytes,
                        file_options={"content-type": mime_type}
                    )
                    print(f"Storage upload response: {upload_response}")
                except Exception as storage_error:
                    print(f"Storage upload FAILED: {str(storage_error)}")
                    return jsonify({'error': f'Storage upload failed: {str(storage_error)}'}), 500

                # AI analysis
                summary = process_with_google_ai(file_path)
                score_data = parse_ai_summary(summary)

                # Save record with storage path
                resume_record = {
                    'user_id': user_id,
                    'filename': filename,
                    'file_path': storage_path,  # storage path, not local path
                    'score': score_data['score'],
                    'feedback': score_data['feedback'],
                    'suggestions': score_data['suggestions'],
                    'created_at': datetime.utcnow().isoformat()
                }

                response = supabase.table('resumes').insert(resume_record).execute()

                if not response.data:
                    return jsonify({'error': 'Failed to save resume data'}), 500

                resume_db = response.data[0]

                # Clean up local file
                os.remove(file_path)

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

@app.route('/resume/<resume_id>/download', methods=['GET'])
@token_required
def download_resume(resume_id):
    """Generate a short-lived signed download URL - only for the owner"""
    try:
        user_id = int(request.user_id)

        # Verify ownership first
        response = (
            supabase.table('resumes')
            .select('file_path, filename')
            .eq('id', resume_id)
            .eq('user_id', user_id)  # ownership check
            .execute()
        )

        if not response.data:
            return jsonify({'error': 'Resume not found'}), 404

        storage_path = response.data[0]['file_path']

        # Generate signed URL valid for 60 seconds — enough to start a download
        signed = supabase.storage.from_('resumes').create_signed_url(
            path=storage_path,
            expires_in=60
        )

        return jsonify({'url': signed['signedURL']}), 200

    except Exception as e:
        return jsonify({'error': f'Could not generate download link: {str(e)}'}), 500

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
                'created_at': resume['created_at']
            })
        
        return jsonify({'resumes': resumes}), 200
    except Exception as e:
        return jsonify({'error': f'Error fetching history: {str(e)}'}), 500

def process_with_google_ai(file_path):
    client = genai.Client(api_key=API_KEY)
    filepath = pathlib.Path(file_path)
    
    prompt = """You are a brutally honest hiring manager in March of 2026. Analyze this resume harshly and honestly — the candidate wants real feedback, not flattery. Be specific and direct.

Respond with ONLY a valid JSON object, no markdown, no extra text:

{
  "score": <0-100, strict: 90+=exceptional, 70-89=good, 50-69=needs work, <50=poor>,
  "feedback": "<2-3 sentences, lead with the biggest problem, be blunt and specific>",
  "suggestions": [
    "<exact problem + exact fix>",
    "<exact problem + exact fix>",
    "<exact problem + exact fix>",
    "<exact problem + exact fix>",
    "<exact problem + exact fix>"
  ]
}"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_bytes(
                data=filepath.read_bytes(),
                mime_type='application/pdf',
            ),
            prompt
        ]
    )

    if hasattr(response, 'text'):
        return response.text
    else:
        raise Exception("Unexpected response format from Gemini.")


def parse_ai_summary(summary: str) -> dict:
    """Parse structured JSON response from AI."""
    # Strip markdown code blocks if model wraps response anyway
    cleaned = summary.strip()
    cleaned = re.sub(r'^```json\s*', '', cleaned)
    cleaned = re.sub(r'^```\s*', '', cleaned)
    cleaned = re.sub(r'\s*```$', '', cleaned)
    cleaned = cleaned.strip()

    try:
        data = json.loads(cleaned)

        score = int(data.get('score', 50))
        score = max(0, min(100, score))  # clamp to 0-100

        feedback = data.get('feedback', '').strip()
        if not feedback:
            raise ValueError("Empty feedback in response")

        suggestions = data.get('suggestions', [])
        suggestions = [s.strip() for s in suggestions if isinstance(s, str) and s.strip()]

        if len(suggestions) < 3:
            raise ValueError("Too few suggestions in response")

        return {
            'score': score,
            'feedback': feedback,
            'suggestions': suggestions[:5]
        }

    except (json.JSONDecodeError, ValueError, KeyError) as e:
        # Only fall back if the model genuinely failed to return valid JSON
        raise Exception(f"AI returned unparseable response: {str(e)}\nRaw: {summary[:300]}")

# Register auth blueprint
from api.auth.routes import auth_bp
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True, port=8000)