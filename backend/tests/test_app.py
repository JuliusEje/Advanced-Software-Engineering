import os
import tempfile
import shutil
import pytest
from unittest.mock import patch, MagicMock
from api.app import app
import jwt
import time

# Use same secret as app
JWT_SECRET = os.getenv('JWT_SECRET', 'your-secret-key-change-in-production')

def generate_test_token(user_id=1, email="test@example.com"):
    """Generate a valid JWT token for testing"""
    payload = {
        'user_id': user_id,
        'email': email,
        'exp': time.time() + 3600  # expires in 1 hour
    }
    return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

@pytest.fixture
def client():
    temp_dir = tempfile.mkdtemp()
    app.config['UPLOAD_FOLDER'] = temp_dir
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

    shutil.rmtree(temp_dir)

@pytest.fixture
def auth_headers():
    """Auth headers fixture for protected routes"""
    token = generate_test_token()
    return {'Authorization': f'Bearer {token}'}

# --- Mocking Supabase so tests don't hit the real DB ---
@pytest.fixture(autouse=True)
def mock_supabase():
    """Mock supabase for all tests to avoid real DB calls"""
    with patch('api.app.supabase') as mock_sb:
        # Default mock for insert (upload)
        mock_insert_response = MagicMock()
        mock_insert_response.data = [{
            'id': 'test-resume-uuid-1234',
            'user_id': 1,
            'filename': 'test_resume.pdf',
            'score': 85,
            'feedback': 'Good resume.',
            'suggestions': ['Improve formatting', 'Add metrics', 'Fix dates'],
            'created_at': '2026-01-01 12:00:00'
        }]
        mock_sb.table.return_value.insert.return_value.execute.return_value = mock_insert_response

        # Default mock for select (score fetch)
        mock_select_response = MagicMock()
        mock_select_response.data = [{
            'id': 'test-resume-uuid-1234',
            'user_id': 1,
            'filename': 'test_resume.pdf',
            'score': 90,
            'feedback': 'Excellent resume.',
            'suggestions': ['Update skills', 'Add metrics', 'Fix dates'],
            'created_at': '2026-01-01 12:00:00'
        }]
        mock_sb.table.return_value.select.return_value.eq.return_value.eq.return_value.execute.return_value = mock_select_response

        # Mock for empty result (invalid ID)
        mock_empty_response = MagicMock()
        mock_empty_response.data = []

        yield mock_sb


def test_upload_file(client, auth_headers):
    with patch('api.app.process_with_google_ai') as mock_ai, \
         patch('api.app.parse_ai_summary') as mock_parse:

        mock_ai.return_value = '{"score": 85, "feedback": "Good resume.", "suggestions": ["Fix this", "Fix that", "Add more"]}'
        mock_parse.return_value = {
            'score': 85,
            'feedback': 'Good resume.',
            'suggestions': ['Fix this', 'Fix that', 'Add more']
        }

        pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        pdf_file.write(b'%PDF-1.4 mock content')
        pdf_file.close()

        with open(pdf_file.name, 'rb') as f:
            data = {'file': (f, 'test_resume.pdf')}
            response = client.post('/resume/upload', data=data,
                                   content_type='multipart/form-data',
                                   headers=auth_headers)

        assert response.status_code == 200
        assert 'Resume uploaded and analyzed successfully' in response.get_json()['message']


def test_upload_invalid_file(client, auth_headers):
    data = {
        'file': (tempfile.NamedTemporaryFile(delete=False, suffix='.txt'), 'test_invalid.txt')
    }
    response = client.post('/resume/upload', data=data,
                           content_type='multipart/form-data',
                           headers=auth_headers)
    assert response.status_code == 400
    assert 'Invalid file type' in response.get_json()['error']


def test_home_endpoint(client):
    """Home endpoint returns API info JSON"""
    response = client.get('/')
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'message' in json_data
    assert json_data['message'] == 'Resume Optimizer API'


def test_health_endpoint(client):
    """Health endpoint returns healthy status"""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'healthy'


def test_get_resume_score_valid(client, auth_headers):
    with patch('api.app.process_with_google_ai') as mock_ai, \
         patch('api.app.parse_ai_summary') as mock_parse:

        mock_ai.return_value = '{"score": 90, "feedback": "Excellent.", "suggestions": ["a", "b", "c"]}'
        mock_parse.return_value = {
            'score': 90,
            'feedback': 'Excellent resume.',
            'suggestions': ['Update skills', 'Add metrics', 'Fix dates']
        }

        # Upload first
        pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        pdf_file.write(b'%PDF-1.4 mock content')
        pdf_file.close()

        with open(pdf_file.name, 'rb') as f:
            data = {'file': (f, 'test_resume.pdf')}
            upload_response = client.post('/resume/upload', data=data,
                                          content_type='multipart/form-data',
                                          headers=auth_headers)

        assert upload_response.status_code == 200
        resume_id = upload_response.get_json()['id']

        # Fetch score
        response = client.get(f'/resume/{resume_id}/score', headers=auth_headers)
        assert response.status_code == 200
        json_data = response.get_json()
        assert 'score' in json_data
        assert 'feedback' in json_data
        assert 'suggestions' in json_data


def test_get_resume_score_invalid(client, auth_headers, mock_supabase):
    """Returns 404 for non-existent resume ID"""
    # Override the default mock to return empty data for this test
    mock_empty = MagicMock()
    mock_empty.data = []
    mock_supabase.table.return_value.select.return_value.eq.return_value.eq.return_value.execute.return_value = mock_empty

    response = client.get('/resume/invalid-id-12345/score', headers=auth_headers)
    assert response.status_code == 404
    assert 'Resume not found' in response.get_json()['error']


def test_upload_no_file(client, auth_headers):
    response = client.post('/resume/upload', data={},
                           content_type='multipart/form-data',
                           headers=auth_headers)
    assert response.status_code == 400
    assert 'No file part' in response.get_json()['error']


def test_upload_empty_filename(client, auth_headers):
    empty_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    empty_file.close()

    with open(empty_file.name, 'rb') as f:
        data = {'file': (f, '')}
        response = client.post('/resume/upload', data=data,
                               content_type='multipart/form-data',
                               headers=auth_headers)

    assert response.status_code == 400
    assert 'No selected file' in response.get_json()['error']


def test_upload_pdf_success(client, auth_headers):
    with patch('api.app.process_with_google_ai') as mock_ai, \
         patch('api.app.parse_ai_summary') as mock_parse:

        mock_ai.return_value = '{"score": 80, "feedback": "Good.", "suggestions": ["a", "b", "c"]}'
        mock_parse.return_value = {
            'score': 80,
            'feedback': 'Good resume.',
            'suggestions': ['Improve format', 'Add metrics', 'Fix dates']
        }

        pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        pdf_file.write(b'%PDF-1.4 mock pdf content')
        pdf_file.close()

        with open(pdf_file.name, 'rb') as f:
            data = {'file': (f, 'resume.pdf')}
            response = client.post('/resume/upload', data=data,
                                   content_type='multipart/form-data',
                                   headers=auth_headers)

        assert response.status_code == 200
        json_data = response.get_json()
        assert 'id' in json_data
        assert 'message' in json_data
        assert 'analyzed successfully' in json_data['message']


def test_upload_docx_success(client, auth_headers):
    with patch('api.app.process_with_google_ai') as mock_ai, \
         patch('api.app.parse_ai_summary') as mock_parse:

        mock_ai.return_value = '{"score": 75, "feedback": "Average.", "suggestions": ["a", "b", "c"]}'
        mock_parse.return_value = {
            'score': 75,
            'feedback': 'Average resume.',
            'suggestions': ['Add experience', 'Quantify results', 'Fix format']
        }

        docx_file = tempfile.NamedTemporaryFile(delete=False, suffix='.docx')
        docx_file.write(b'mock docx content')
        docx_file.close()

        with open(docx_file.name, 'rb') as f:
            data = {'file': (f, 'resume.docx')}
            response = client.post('/resume/upload', data=data,
                                   content_type='multipart/form-data',
                                   headers=auth_headers)

        assert response.status_code == 200
        json_data = response.get_json()
        assert 'id' in json_data
        assert 'Resume uploaded and analyzed successfully' in json_data['message']


def test_upload_requires_auth(client):
    """Protected routes return 401 without token"""
    response = client.post('/resume/upload', data={},
                           content_type='multipart/form-data')
    assert response.status_code == 401


def test_expired_token(client):
    """Expired tokens are rejected"""
    expired_payload = {
        'user_id': 1,
        'email': 'test@example.com',
        'exp': time.time() - 3600  # already expired
    }
    expired_token = jwt.encode(expired_payload, JWT_SECRET, algorithm='HS256')
    headers = {'Authorization': f'Bearer {expired_token}'}

    response = client.post('/resume/upload', data={},
                           content_type='multipart/form-data',
                           headers=headers)
    assert response.status_code == 401
    assert 'expired' in response.get_json()['error'].lower()