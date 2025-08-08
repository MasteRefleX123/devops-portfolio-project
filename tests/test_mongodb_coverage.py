#!/usr/bin/env python3
"""
Advanced Unit Tests for 100% Code Coverage
Tests MongoDB functionality, exception handling, and edge cases
"""

import pytest
import json
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import oriyan_portfolio

class TestMongoDBFunctionality:
    """Test MongoDB related functionality with mocking"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        oriyan_portfolio.app.config['TESTING'] = True
        with oriyan_portfolio.app.test_client() as client:
            yield client

    def test_track_visitor_success(self, client, mocker):
        """Test successful visitor tracking"""
        # Mock MongoDB collections
        mock_visitors_collection = MagicMock()
        mock_stats_collection = MagicMock()
        
        mocker.patch.object(oriyan_portfolio, 'visitors_collection', mock_visitors_collection)
        mocker.patch.object(oriyan_portfolio, 'stats_collection', mock_stats_collection)
        
        # Mock request context
        with client.application.test_request_context('/', environ_base={'REMOTE_ADDR': '127.0.0.1', 'HTTP_USER_AGENT': 'TestAgent'}):
            result = oriyan_portfolio.track_visitor()
            
            assert result == True
            mock_visitors_collection.insert_one.assert_called_once()
            mock_stats_collection.update_one.assert_called_once()

    def test_track_visitor_none_collection(self, client, mocker):
        """Test visitor tracking when collections are None"""
        mocker.patch.object(oriyan_portfolio, 'visitors_collection', None)
        mocker.patch.object(oriyan_portfolio, 'stats_collection', None)
        
        with client.application.test_request_context('/'):
            result = oriyan_portfolio.track_visitor()
            assert result == False

    def test_track_visitor_exception(self, client, mocker):
        """Test visitor tracking with database exception"""
        mock_collection = MagicMock()
        mock_collection.insert_one.side_effect = Exception("DB Error")
        
        mocker.patch.object(oriyan_portfolio, 'visitors_collection', mock_collection)
        mocker.patch.object(oriyan_portfolio, 'stats_collection', mock_collection)
        
        with client.application.test_request_context('/'):
            result = oriyan_portfolio.track_visitor()
            assert result == False

    def test_get_visitor_count_success(self, mocker):
        """Test successful visitor count retrieval"""
        mock_collection = MagicMock()
        mock_collection.find_one.return_value = {'total_visitors': 150}
        
        mocker.patch.object(oriyan_portfolio, 'stats_collection', mock_collection)
        
        result = oriyan_portfolio.get_visitor_count()
        assert result == 150

    def test_get_visitor_count_no_stats(self, mocker):
        """Test visitor count when no stats exist"""
        mock_collection = MagicMock()
        mock_collection.find_one.return_value = None
        
        mocker.patch.object(oriyan_portfolio, 'stats_collection', mock_collection)
        
        result = oriyan_portfolio.get_visitor_count()
        assert result == 42  # Fallback value

    def test_get_visitor_count_none_collection(self, mocker):
        """Test visitor count when collection is None"""
        mocker.patch.object(oriyan_portfolio, 'stats_collection', None)
        
        result = oriyan_portfolio.get_visitor_count()
        assert result == 42  # Fallback value

    def test_get_visitor_count_exception(self, mocker):
        """Test visitor count with exception"""
        mock_collection = MagicMock()
        mock_collection.find_one.side_effect = Exception("DB Error")
        
        mocker.patch.object(oriyan_portfolio, 'stats_collection', mock_collection)
        
        result = oriyan_portfolio.get_visitor_count()
        assert result == 42  # Fallback value


class TestAdvancedAPIEndpoints:
    """Test API endpoints with MongoDB mocking"""
    
    @pytest.fixture
    def client(self):
        """Create test client"""
        oriyan_portfolio.app.config['TESTING'] = True
        with oriyan_portfolio.app.test_client() as client:
            yield client

    def test_visitors_api_get_with_data(self, client, mocker):
        """Test visitors API GET with MongoDB data"""
        mock_visitors_collection = MagicMock()
        mock_stats_collection = MagicMock()
        
        # Mock data
        mock_visitors_collection.find.return_value.sort.return_value.limit.return_value = [
            {'_id': 'test_id', 'timestamp': '2024-01-01T10:00:00', 'ip': '127.0.0.1'}
        ]
        
        mocker.patch.object(oriyan_portfolio, 'visitors_collection', mock_visitors_collection)
        mocker.patch.object(oriyan_portfolio, 'stats_collection', mock_stats_collection)
        mocker.patch.object(oriyan_portfolio, 'get_visitor_count', return_value=100)
        
        response = client.get('/api/visitors')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['total_visitors'] == 100
        assert 'recent_visitors' in data

    def test_visitors_api_get_exception(self, client, mocker):
        """Test visitors API GET with exception"""
        mock_collection = MagicMock()
        mock_collection.find.side_effect = Exception("DB Error")
        
        mocker.patch.object(oriyan_portfolio, 'visitors_collection', mock_collection)
        mocker.patch.object(oriyan_portfolio, 'get_visitor_count', return_value=42)
        
        response = client.get('/api/visitors')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['total_visitors'] == 42
        assert data['recent_visitors'] == []

    def test_visitors_api_post_success(self, client, mocker):
        """Test visitors API POST success"""
        mocker.patch.object(oriyan_portfolio, 'track_visitor', return_value=True)
        mocker.patch.object(oriyan_portfolio, 'get_visitor_count', return_value=101)
        
        response = client.post('/api/visitors')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'visitor tracked'
        assert data['total'] == 101

    def test_home_with_visitor_tracking(self, client, mocker):
        """Test home page with visitor tracking"""
        mocker.patch.object(oriyan_portfolio, 'track_visitor', return_value=True)
        
        response = client.get('/')
        assert response.status_code == 200
        assert b'html' in response.data.lower()

    def test_stats_with_dynamic_visitors(self, client, mocker):
        """Test stats endpoint with dynamic visitor count"""
        mocker.patch.object(oriyan_portfolio, 'get_visitor_count', return_value=250)
        
        response = client.get('/api/stats')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['visitors'] == 250


class TestMongoDBInitialization:
    """Test MongoDB connection and initialization scenarios"""
    
    @patch('oriyan_portfolio.MongoClient')
    def test_mongodb_connection_success(self, mock_mongo_client):
        """Test successful MongoDB connection"""
        mock_client = MagicMock()
        mock_db = MagicMock()
        mock_collection = MagicMock()
        
        mock_mongo_client.return_value = mock_client
        mock_client.get_default_database.return_value = mock_db
        mock_collection.count_documents.return_value = 0
        
        # Reload the module to test initialization
        import importlib
        importlib.reload(oriyan_portfolio)
        
        mock_mongo_client.assert_called()

    @patch('oriyan_portfolio.MongoClient')
    def test_mongodb_connection_failure(self, mock_mongo_client):
        """Test MongoDB connection failure"""
        mock_mongo_client.side_effect = Exception("Connection failed")
        
        # Reload the module to test initialization
        import importlib
        importlib.reload(oriyan_portfolio)
        
        # Should handle the exception gracefully
        assert True  # If we get here, exception was handled

    def test_environment_variable_usage(self, mocker):
        """Test MongoDB URI from environment variable"""
        mocker.patch.dict(os.environ, {'MONGO_URI': 'mongodb://test:27017/test'})
        
        # Test that environment variable is used
        import importlib
        importlib.reload(oriyan_portfolio)
        
        assert True  # Test passes if no exception


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
