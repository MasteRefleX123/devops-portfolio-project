#!/usr/bin/env python3
"""
Basic Unit Tests for Oriyan Portfolio Application
"""

import pytest
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from oriyan_portfolio import app

class TestBasicEndpoints:
    """Basic tests for all endpoints"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    def test_home_page_loads(self, client):
        """Test home page loads successfully"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'html' in response.data.lower()

    def test_health_endpoint(self, client):
        """Test health endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'DevOps Portfolio' in data['app']

    def test_stats_endpoint(self, client):
        """Test stats API endpoint"""
        response = client.get('/api/stats')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'portfolio_owner' in data
        assert data['age'] == 21

    def test_skills_endpoint(self, client):
        """Test skills API endpoint"""
        response = client.get('/api/skills')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'devops_tools' in data
        assert 'Docker' in data['devops_tools']

    def test_projects_endpoint(self, client):
        """Test projects API endpoint"""
        response = client.get('/api/projects')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) > 0

    def test_nonexistent_endpoint(self, client):
        """Test 404 for non-existent endpoint"""
        response = client.get('/nonexistent')
        assert response.status_code == 404

    def test_visitors_api_get(self, client):
        """Test visitors API GET endpoint"""
        response = client.get('/api/visitors')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'total_visitors' in data
        assert 'recent_visitors' in data
        assert isinstance(data['total_visitors'], int)

    def test_visitors_api_post(self, client):
        """Test visitors API POST endpoint"""
        response = client.post('/api/visitors')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'status' in data
        assert 'total' in data
        assert data['status'] == 'visitor tracked'
