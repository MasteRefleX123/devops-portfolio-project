#!/usr/bin/env python3
"""
DevOps Portfolio Application
Main application entry point
"""

import os
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config.update(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-secret-key'),
        MONGO_URI=os.environ.get('MONGO_URI', 'mongodb://localhost:27017/portfolio'),
        DEBUG=os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    )
    
    # Portfolio data
    PORTFOLIO_DATA = {
        "personal_info": {
            "name": "DevOps Engineer Portfolio",
            "title": "Cloud & DevOps Specialist",
            "email": "your.email@example.com",
            "linkedin": "https://linkedin.com/in/your-profile",
            "github": "https://github.com/your-username",
            "location": "Israel",
            "summary": "Passionate DevOps engineer with expertise in containerization, orchestration, CI/CD, and cloud infrastructure."
        },
        "skills": {
            "Cloud Platforms": ["AWS", "Azure", "GCP"],
            "Containers": ["Docker", "Kubernetes", "Helm"],
            "CI/CD": ["Jenkins", "GitLab CI", "ArgoCD"],
            "Monitoring": ["Prometheus", "Grafana", "ELK Stack"]
        },
        "projects": [
            {
                "name": "Cloud-Native Platform",
                "description": "Microservices architecture on Kubernetes",
                "technologies": ["Kubernetes", "Docker", "Jenkins"],
                "github_url": "https://github.com/your-username/project1"
            }
        ],
        "certifications": [
            {
                "name": "AWS Solutions Architect",
                "issuer": "Amazon Web Services",
                "date": "2024",
                "credential_id": "AWS-SAA-XXXX"
            }
        ]
    }
    
    @app.route('/')
    def index():
        return render_template('index.html', data=PORTFOLIO_DATA)
    
    @app.route('/health')
    def health_check():
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0"
        })
    
    @app.route('/api/stats')
    def get_stats():
        return jsonify({
            "total_visitors": 100,
            "projects_count": len(PORTFOLIO_DATA["projects"]),
            "certifications_count": len(PORTFOLIO_DATA["certifications"])
        })
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("🚀 Starting DevOps Portfolio Application")
    app.run(host='0.0.0.0', port=5000, debug=True)
