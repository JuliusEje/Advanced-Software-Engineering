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
        response = client.post('/upload', data=data, content_type='multipart/form-data')
        assert response.status_code == 200
        assert 'File processed successfully' in response.get_json()['message']

def test_upload_invalid_file(client):
    data = {
        'file': (tempfile.NamedTemporaryFile(delete=False, suffix='.txt'), 'test_invalid.txt')
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert 'Invalid file type' in response.get_json()['error']