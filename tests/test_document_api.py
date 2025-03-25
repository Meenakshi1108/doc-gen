import json
import pytest
import os
import sys

# Import create_app from the app module
from app.main import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'
    assert response.json['service'] == 'Document Generation Service'

def test_validation_missing_fields(client):
    """Test validation when required fields are missing"""
    data = {
        'content_html': '<p>Test content</p>'
        # Missing document_type
    }
    
    response = client.post(
        '/api/v1/generate',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    assert 'Missing required field' in response.json['error']

def test_validation_invalid_document_type(client):
    """Test validation when document_type is invalid"""
    data = {
        'content_html': '<p>Test content</p>',
        'document_type': 'invalid_type'
    }
    
    response = client.post(
        '/api/v1/generate',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 400
    assert 'Invalid document_type' in response.json['error']