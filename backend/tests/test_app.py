import os
import tempfile
import shutil
import pytest
from unittest.mock import patch, MagicMock
from api.app import app

@pytest.fixture
def client():
    # Use mkdtemp() to create a temporary directory, not mkstemp() which creates a file
    temp_dir = tempfile.mkdtemp()
    app.config['UPLOAD_FOLDER'] = temp_dir
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client

    # Clean up the temporary directory
    shutil.rmtree(temp_dir)

def test_upload_file(client):
    with patch('api.app.process_with_google_ai') as mock_ai:
        # Mock the AI response
        mock_ai.return_value = "### **1. Resume Score: 85/100**\nThis is a good resume."
        
        data = {
            'file': (tempfile.NamedTemporaryFile(delete=False, suffix='.pdf'), 'test_resume.pdf')
        }
        response = client.post('/resume/upload', data=data, content_type='multipart/form-data')
        assert response.status_code == 200
        assert 'Resume uploaded and analyzed successfully' in response.get_json()['message']

def test_upload_invalid_file(client):
    data = {
        'file': (tempfile.NamedTemporaryFile(delete=False, suffix='.txt'), 'test_invalid.txt')
    }
    response = client.post('/resume/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert 'Invalid file type' in response.get_json()['error']

# test for: Home endpoint returns correct response
# explain the test: Tests the home page route to ensure it returns a successful response with expected content
def test_home_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.data == b'Hello, World!'

# test for: About endpoint returns correct response
# explain the test: Tests the about page route to ensure it returns a successful response with expected content
def test_about_endpoint(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert response.data == b'About'

# test for: Retrieve resume score with valid resume ID
# explain the test: Tests retrieving a stored resume score after successful upload to verify accurate data retrieval
def test_get_resume_score_valid(client):
    with patch('api.app.process_with_google_ai') as mock_ai:
        mock_ai.return_value = "### **1. Resume Score: 90/100**\nOverall Feedback: Excellent resume.\nSpecific Improvement Suggestions\n#### **1. Update Skills**\n**Action:** Add more technical skills"
        
        # First upload a resume
        data = {
            'file': (tempfile.NamedTemporaryFile(delete=False, suffix='.pdf'), 'test_resume.pdf')
        }
        upload_response = client.post('/resume/upload', data=data, content_type='multipart/form-data')
        resume_id = upload_response.get_json()['id']
        
        # Then retrieve its score
        response = client.get(f'/resume/{resume_id}/score')
        assert response.status_code == 200
        assert response.get_json()['score'] == 90
        assert 'feedback' in response.get_json()
        assert 'suggestions' in response.get_json()

# test for: Retrieve resume score with invalid resume ID
# explain the test: Tests error handling when requesting a non-existent resume to ensure 404 status is returned
def test_get_resume_score_invalid(client):
    response = client.get('/resume/invalid-id-12345/score')
    assert response.status_code == 404
    assert 'Resume not found' in response.get_json()['error']

# test for: Upload file without file part in request
# explain the test: Tests form validation by not including a file in the multipart request to verify error handling
def test_upload_no_file(client):
    response = client.post('/resume/upload', data={}, content_type='multipart/form-data')
    assert response.status_code == 400
    assert 'No file part' in response.get_json()['error']

# test for: Upload with empty filename
# explain the test: Tests filename validation by submitting an empty filename to verify proper error response
def test_upload_empty_filename(client):
    empty_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    empty_file.close()
    
    with open(empty_file.name, 'rb') as f:
        data = {'file': (f, '')}
        response = client.post('/resume/upload', data=data, content_type='multipart/form-data')
    
    assert response.status_code == 400
    assert 'No selected file' in response.get_json()['error']

# test for: Upload PDF file successfully and verify response structure
# explain the test: Tests successful upload with a PDF file and validates the response structure includes required fields (id, message)
def test_upload_pdf_success(client):
    with patch('api.app.process_with_google_ai') as mock_ai:
        mock_ai.return_value = "### **1. Resume Score: 80/100**\nOverall Feedback: Good resume.\nSpecific Improvement Suggestions\n#### **1. Improve Format**\n**Action:** Use consistent formatting"
        
        pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        pdf_file.write(b'%PDF-1.4 mock pdf content')
        pdf_file.close()
        
        with open(pdf_file.name, 'rb') as f:
            data = {'file': (f, 'resume.pdf')}
            response = client.post('/resume/upload', data=data, content_type='multipart/form-data')
        
        assert response.status_code == 200
        assert 'id' in response.get_json()
        assert 'message' in response.get_json()
        assert 'analyzed successfully' in response.get_json()['message']

# test for: Upload DOCX file successfully to verify multiple file type support
# explain the test: Tests that the application accepts DOCX files (not just PDF) and processes them correctly
def test_upload_docx_success(client):
    with patch('api.app.process_with_google_ai') as mock_ai:
        mock_ai.return_value = "### **1. Resume Score: 75/100**\nOverall Feedback: Average resume.\nSpecific Improvement Suggestions\n#### **1. Add Experience**\n**Action:** Include more work experience"
        
        docx_file = tempfile.NamedTemporaryFile(delete=False, suffix='.docx')
        docx_file.write(b'mock docx content')
        docx_file.close()
        
        with open(docx_file.name, 'rb') as f:
            data = {'file': (f, 'resume.docx')}
            response = client.post('/resume/upload', data=data, content_type='multipart/form-data')
        
        assert response.status_code == 200
        json_response = response.get_json()
        assert 'id' in json_response
        assert 'Resume uploaded and analyzed successfully' in json_response['message']