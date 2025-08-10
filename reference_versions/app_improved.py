#!/usr/bin/env python3
"""
DevOps Portfolio Application - Improved Structure
Oriyan Hemo - DevOps Course 2024
"""

import os
from flask import Flask, jsonify, request
from pymongo import MongoClient
from datetime import datetime, timezone
from bson import ObjectId

def create_app(config=None):
    """Factory function to create Flask application"""
    app = Flask(__name__)
    
    # Configuration
    app.config.update(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-secret-key'),
        MONGO_URI=os.environ.get('MONGO_URI', 'mongodb://localhost:27017/oriyan_portfolio'),
        DEBUG=os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    )
    
    if config:
        app.config.update(config)
    
    # Initialize MongoDB
    mongo_client = None
    db = None
    visitors_collection = None
    stats_collection = None
    
    try:
        mongo_client = MongoClient(app.config['MONGO_URI'], serverSelectionTimeoutMS=2000)
        db = mongo_client.get_default_database()
        visitors_collection = db.visitors
        stats_collection = db.stats
        print("✅ MongoDB connected successfully")
        
        # Initialize stats if not exists
        if stats_collection.count_documents({}) == 0:
            stats_collection.insert_one({
                'total_visitors': 0,
                'last_updated': datetime.now(timezone.utc)
            })
    except Exception as e:
        print(f"⚠️  MongoDB connection failed: {e}")
        visitors_collection = None
        stats_collection = None
    
    # Helper functions
    def track_visitor():
        """Track visitor information"""
        if visitors_collection is None:
            return
        
        try:
            visitor_data = {
                'ip': request.remote_addr,
                'user_agent': request.user_agent.string,
                'timestamp': datetime.now(timezone.utc),
                'path': request.path
            }
            visitors_collection.insert_one(visitor_data)
            
            # Update total visitors count
            stats_collection.update_one(
                {},
                {'$inc': {'total_visitors': 1}, '$set': {'last_updated': datetime.now(timezone.utc)}},
                upsert=True
            )
        except Exception as e:
            print(f"Error tracking visitor: {e}")
    
    def get_visitor_count():
        """Get total visitor count"""
        if stats_collection is None:
            return 0
        
        try:
            stats = stats_collection.find_one()
            return stats.get('total_visitors', 0) if stats else 0
        except Exception:
            return 0
    
    # Store helper functions in app context
    app.track_visitor = track_visitor
    app.get_visitor_count = get_visitor_count
    app.visitors_collection = visitors_collection
    
    # Import and register routes
    register_routes(app)
    
    return app

def register_routes(app):
    """Register all application routes"""
    
    @app.route('/')
    def home():
        app.track_visitor()
        return get_portfolio_html()
    
    @app.route('/health')
    def health():
        return jsonify({'status': 'healthy'}), 200
    
    @app.route('/api/stats')
    def stats():
        return jsonify({
            'visitors': app.get_visitor_count(),
            'projects': 15,
            'technologies': 25
        })
    
    @app.route('/api/skills')
    def skills():
        return jsonify({
            'devops': ['Docker', 'Kubernetes', 'Jenkins', 'ArgoCD', 'Terraform'],
            'cloud': ['AWS', 'Azure', 'GCP'],
            'programming': ['Python', 'Bash', 'JavaScript'],
            'monitoring': ['Prometheus', 'Grafana', 'ELK Stack']
        })
    
    @app.route('/api/projects')
    def projects():
        return jsonify([
            {'name': 'CI/CD Pipeline', 'tech': 'Jenkins, Docker, K8s'},
            {'name': 'Infrastructure as Code', 'tech': 'Terraform, Ansible'},
            {'name': 'Monitoring Solution', 'tech': 'Prometheus, Grafana'}
        ])
    
    @app.route('/api/visitors', methods=['GET', 'POST'])
    def visitors_api():
        if request.method == 'GET':
            if app.visitors_collection is None:
                return jsonify({'error': 'Database not connected'}), 503
            
            try:
                visitors_list = []
                for visitor in app.visitors_collection.find().limit(100):
                    visitor['_id'] = str(visitor['_id'])
                    if 'timestamp' in visitor:
                        visitor['timestamp'] = visitor['timestamp'].isoformat()
                    visitors_list.append(visitor)
                return jsonify(visitors_list)
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        elif request.method == 'POST':
            app.track_visitor()
            return jsonify({'message': 'Visitor tracked', 'total': app.get_visitor_count()})

def get_portfolio_html():
    """Return the portfolio HTML content"""
    return '''
    <!DOCTYPE html>
    <html lang="he" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>אוריין המו - DevOps Portfolio</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 2rem;
            }
            header {
                text-align: center;
                color: white;
                padding: 3rem 0;
                animation: fadeIn 1s;
            }
            h1 {
                font-size: 3rem;
                margin-bottom: 1rem;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .subtitle {
                font-size: 1.5rem;
                opacity: 0.95;
            }
            .stats-container {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 2rem;
                margin: 3rem 0;
            }
            .stat-card {
                background: white;
                padding: 2rem;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                transition: transform 0.3s, box-shadow 0.3s;
            }
            .stat-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 15px 40px rgba(0,0,0,0.15);
            }
            .stat-number {
                font-size: 2.5rem;
                font-weight: bold;
                color: #667eea;
                display: block;
                margin-bottom: 0.5rem;
            }
            .section {
                background: white;
                padding: 3rem;
                border-radius: 20px;
                margin: 2rem 0;
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            }
            .section h2 {
                color: #667eea;
                margin-bottom: 2rem;
                font-size: 2rem;
                text-align: center;
            }
            .skills-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 2rem;
            }
            .skill-category h3 {
                color: #764ba2;
                margin-bottom: 1rem;
            }
            .skill-tag {
                display: inline-block;
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                padding: 0.5rem 1rem;
                border-radius: 20px;
                margin: 0.3rem;
                font-size: 0.9rem;
            }
            .project-card {
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                padding: 1.5rem;
                border-radius: 10px;
                margin: 1rem 0;
                transition: transform 0.3s;
            }
            .project-card:hover {
                transform: translateX(-10px);
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(-20px); }
                to { opacity: 1; transform: translateY(0); }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>אוריין המו</h1>
                <p class="subtitle">DevOps Engineer | Cloud Architect | Automation Expert</p>
            </header>
            
            <div class="stats-container">
                <div class="stat-card">
                    <i class="fas fa-users fa-2x" style="color: #667eea;"></i>
                    <span class="stat-number" id="visitors">0</span>
                    <span>מבקרים</span>
                </div>
                <div class="stat-card">
                    <i class="fas fa-project-diagram fa-2x" style="color: #764ba2;"></i>
                    <span class="stat-number" id="projects">0</span>
                    <span>פרויקטים</span>
                </div>
                <div class="stat-card">
                    <i class="fas fa-tools fa-2x" style="color: #667eea;"></i>
                    <span class="stat-number" id="technologies">0</span>
                    <span>טכנולוגיות</span>
                </div>
            </div>
            
            <div class="section">
                <h2>🚀 כישורים טכניים</h2>
                <div class="skills-grid" id="skills-container">
                    <!-- Skills will be loaded here -->
                </div>
            </div>
            
            <div class="section">
                <h2>💼 פרויקטים נבחרים</h2>
                <div id="projects-container">
                    <!-- Projects will be loaded here -->
                </div>
            </div>
        </div>
        
        <script>
            // Load stats
            fetch('/api/stats')
                .then(res => res.json())
                .then(data => {
                    document.getElementById('visitors').textContent = data.visitors;
                    document.getElementById('projects').textContent = data.projects;
                    document.getElementById('technologies').textContent = data.technologies;
                });
            
            // Load skills
            fetch('/api/skills')
                .then(res => res.json())
                .then(data => {
                    const container = document.getElementById('skills-container');
                    for (const [category, skills] of Object.entries(data)) {
                        const div = document.createElement('div');
                        div.className = 'skill-category';
                        div.innerHTML = '<h3>' + category.toUpperCase() + '</h3>' +
                            skills.map(skill => '<span class="skill-tag">' + skill + '</span>').join('');
                        container.appendChild(div);
                    }
                });
            
            // Load projects
            fetch('/api/projects')
                .then(res => res.json())
                .then(data => {
                    const container = document.getElementById('projects-container');
                    data.forEach(project => {
                        const div = document.createElement('div');
                        div.className = 'project-card';
                        div.innerHTML = '<h3>' + project.name + '</h3><p>Technologies: ' + project.tech + '</p>';
                        container.appendChild(div);
                    }
                });
            
            // Track visitor
            fetch('/api/visitors', { method: 'POST' });
        </script>
    </body>
    </html>
    '''

# Create app instance for module-level compatibility
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])
