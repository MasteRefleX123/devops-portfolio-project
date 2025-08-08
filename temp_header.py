from flask import Flask, jsonify, request
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

# MongoDB Configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/oriyan_portfolio')
try:
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client.get_default_database()
    visitors_collection = db.visitors
    stats_collection = db.stats
    print("✅ MongoDB connected successfully")
    
    # Initialize stats if not exists
    if stats_collection.count_documents({}) == 0:
        stats_collection.insert_one({
            'total_visitors': 0,
            'last_updated': datetime.utcnow()
        })
        
except Exception as e:
    print(f"⚠️  MongoDB connection failed: {e}")
    mongo_client = None
    db = None
    visitors_collection = None
    stats_collection = None

def track_visitor():
    """Track visitor to database"""
    try:
        if visitors_collection is not None:
            visitor_data = {
                'ip': request.environ.get('REMOTE_ADDR', 'unknown'),
                'user_agent': request.environ.get('HTTP_USER_AGENT', 'unknown'),
                'timestamp': datetime.utcnow(),
                'page': request.path
            }
            visitors_collection.insert_one(visitor_data)
            
            # Update stats
            stats_collection.update_one(
                {},
                {'$inc': {'total_visitors': 1}, '$set': {'last_updated': datetime.utcnow()}},
                upsert=True
            )
            return True
    except Exception as e:
        print(f"Error tracking visitor: {e}")
    return False

def get_visitor_count():
    """Get total visitor count from database"""
    try:
        if stats_collection is not None:
            stats = stats_collection.find_one({})
            return stats.get('total_visitors', 42) if stats else 42
    except:
        pass
    return 42  # Fallback

