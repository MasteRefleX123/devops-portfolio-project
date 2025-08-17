"""Tests for the contact form functionality"""
import pytest
import json
from unittest.mock import patch, MagicMock
from datetime import datetime, timezone

def test_contact_form_page(client):
    """Test that contact form page loads successfully"""
    response = client.get('/contact')
    assert response.status_code == 200
    assert b'צור קשר' in response.data

def test_submit_contact_success(client):
    """Test successful contact form submission"""
    with patch('oriyan_portfolio.contacts_collection', MagicMock()):
        contact_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'phone': '0501234567',
            'subject': 'Test Subject',
            'message': 'This is a test message'
        }
        
        response = client.post('/api/contact',
                              data=json.dumps(contact_data),
                              content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['success'] == True

def test_submit_contact_missing_fields(client):
    """Test contact form submission with missing required fields"""
    contact_data = {
        'name': 'Test User',
        'email': 'test@example.com'
    }
    
    response = client.post('/api/contact',
                          data=json.dumps(contact_data),
                          content_type='application/json')
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
