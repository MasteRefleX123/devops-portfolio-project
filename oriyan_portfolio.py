from flask import Flask, jsonify, request
from pymongo import MongoClient
from datetime import datetime, timezone
import os

from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST, CollectorRegistry

app = Flask(__name__)

# Metrics
metrics_registry = CollectorRegistry()
REQUEST_COUNT = Counter('portfolio_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'http_status'], registry=metrics_registry)
REQUEST_LATENCY = Histogram('portfolio_request_latency_seconds', 'Request latency', ['endpoint'], registry=metrics_registry)

# MongoDB Configuration
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/oriyan_portfolio')
try:
    mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
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
                'timestamp': datetime.now(timezone.utc),
                'page': request.path
            }
            visitors_collection.insert_one(visitor_data)
            
            # Update stats
            stats_collection.update_one(
                {},
                {'$inc': {'total_visitors': 1}, '$set': {'last_updated': datetime.now(timezone.utc)}},
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

@app.before_request
def before_request():
    request._start_time = datetime.now(timezone.utc)

@app.after_request
def after_request(response):
    try:
        latency = (datetime.now(timezone.utc) - getattr(request, '_start_time', datetime.now(timezone.utc))).total_seconds()
        REQUEST_LATENCY.labels(request.path).observe(latency)
        REQUEST_COUNT.labels(request.method, request.path, response.status_code).inc()
    except Exception:
        pass
    return response

@app.route('/metrics')
def metrics():
    return generate_latest(metrics_registry), 200, {'Content-Type': CONTENT_TYPE_LATEST}

@app.route('/')
def home():
    track_visitor()  # Track visitor to MongoDB
    return '''
    <!DOCTYPE html>
    <html lang="he" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>אוריין ראסק - DevOps Portfolio</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', Arial, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                color: #333;
            }
            .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
            
            /* Header */
            .hero { 
                background: rgba(255,255,255,0.95); 
                padding: 60px 40px; 
                border-radius: 20px; 
                text-align: center;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                margin-bottom: 30px;
                backdrop-filter: blur(10px);
            }
            .hero h1 { font-size: 3em; color: #2c3e50; margin-bottom: 10px; }
            .hero h2 { font-size: 1.5em; color: #3498db; margin-bottom: 20px; }
            .hero .subtitle { font-size: 1.2em; color: #7f8c8d; margin: 10px 0; }
            .quote { 
                font-style: italic; 
                font-size: 1.3em; 
                color: #e74c3c;
                margin: 20px 0;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 10px;
                border-left: 5px solid #e74c3c;
            }
            
            /* Navigation Buttons */
            .nav-buttons { margin: 30px 0; }
            .btn { 
                background: #3498db; 
                color: white; 
                padding: 15px 30px; 
                text-decoration: none; 
                border-radius: 50px; 
                margin: 10px; 
                display: inline-block;
                transition: all 0.3s ease;
                font-weight: bold;
                box-shadow: 0 5px 15px rgba(52, 152, 219, 0.3);
            }
            .btn:hover { 
                background: #2980b9; 
                transform: translateY(-3px);
                box-shadow: 0 10px 25px rgba(52, 152, 219, 0.4);
            }
            .btn i { margin-left: 8px; }
            
            /* Sections */
            .section { 
                background: rgba(255,255,255,0.95); 
                padding: 40px; 
                border-radius: 15px; 
                margin: 30px 0; 
                box-shadow: 0 10px 30px rgba(0,0,0,0.1);
                backdrop-filter: blur(10px);
            }
            .section h2 { color: #2c3e50; margin-bottom: 25px; font-size: 2.2em; }
            .section h3 { color: #3498db; margin: 20px 0 15px 0; font-size: 1.5em; }
            
            /* Skills Grid */
            .skills-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 25px;
                margin-top: 25px;
            }
            .skill-category {
                background: #f8f9fa;
                padding: 25px;
                border-radius: 15px;
                border-left: 5px solid #3498db;
                transition: transform 0.3s ease;
            }
            .skill-category:hover { transform: translateY(-5px); }
            .skill-category h4 { color: #2c3e50; margin-bottom: 15px; }
            .skill-list { list-style: none; }
            .skill-list li { 
                padding: 8px 0; 
                border-bottom: 1px solid #ecf0f1; 
                color: #34495e;
            }
            .skill-list li:last-child { border-bottom: none; }
            .skill-placeholder { 
                color: #95a5a6; 
                font-style: italic; 
                background: #ecf0f1;
                padding: 10px;
                border-radius: 5px;
            }
            
            /* Projects Grid */
            .projects-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
                gap: 25px;
                margin-top: 25px;
            }
            .project-card {
                background: #fff;
                padding: 25px;
                border-radius: 15px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                border-left: 5px solid #e74c3c;
                transition: transform 0.3s ease;
            }
            .project-card:hover { transform: translateY(-5px); }
            .project-card h4 { color: #2c3e50; margin-bottom: 15px; }
            .project-tech { margin: 15px 0; }
            .tech-tag { 
                background: #3498db; 
                color: white; 
                padding: 5px 12px; 
                border-radius: 20px; 
                font-size: 0.9em; 
                margin: 3px;
                display: inline-block;
            }
            
            /* Certifications */
            .certs-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
                margin-top: 25px;
            }
            .cert-card {
                background: linear-gradient(45deg, #f39c12, #e67e22);
                color: white;
                padding: 25px;
                border-radius: 15px;
                text-align: center;
                box-shadow: 0 8px 20px rgba(243, 156, 18, 0.3);
            }
            .cert-card i { font-size: 3em; margin-bottom: 15px; }
            
            /* Contact Section */
            .contact-info { 
                background: linear-gradient(45deg, #16a085, #27ae60);
                color: white;
                padding: 40px; 
                border-radius: 15px; 
                text-align: center;
            }
            .contact-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-top: 25px;
            }
            .contact-item { padding: 15px; }
            .contact-item i { font-size: 2em; margin-bottom: 10px; }
            
            /* Responsive */
            @media (max-width: 768px) {
                .hero { padding: 40px 20px; }
                .hero h1 { font-size: 2.2em; }
                .section { padding: 25px; }
                .skills-grid, .projects-grid { grid-template-columns: 1fr; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <!-- Hero Section -->
            <div class="hero">
                <h1><i class="fas fa-rocket"></i> אוריין ראסק</h1>
                <h2>Oriyan Rask - DevOps Junior Engineer</h2>
                <p class="subtitle"><strong>בוגר מכללת SELA</strong> | בן 21 | מודיעין, ישראל 🇮🇱</p>
                <p class="subtitle">שאפתני ומקצועי עם רקע ברשתות ובתכנות</p>
                <p class="subtitle">מתקדם ללמידה של <strong>אבטחת מידע</strong> 🔒</p>
                <div class="quote">
                    <i class="fas fa-quote-right"></i>
                    "מעוניין לשנות את העולם ולעשות את זה עם חיוך 😊"
                </div>
                
                <div class="nav-buttons">
                    <a href="https://github.com/MasteRefleX123" target="_blank" class="btn">
                        <i class="fab fa-github"></i> GitHub Profile
                    </a>
                    <a href="mailto:oriyanrwork99@gmail.com" class="btn">
                        <i class="fas fa-envelope"></i> צור קשר
                    </a>
                    <a href="#" class="btn" style="background: #0077b5;">
                        <i class="fab fa-linkedin"></i> LinkedIn (להוסיף)
                    </a>
                    <a href="/health" class="btn" style="background: #28a745;">
                        <i class="fas fa-heartbeat"></i> Health Check
                    </a>
                    <a href="/api/stats" class="btn" style="background: #6f42c1;">
                        <i class="fas fa-chart-bar"></i> API Stats
                    </a>
                </div>
            </div>
            
            <!-- About Section -->
            <div class="section">
                <h2><i class="fas fa-user"></i> אודותיי</h2>
                <p style="font-size: 1.2em; line-height: 1.8;">
                    DevOps ג'וניור עם <strong>תשוקה לטכנולוגיה וללמידה מתמדת</strong>. 
                    רקע חזק ברשתות ותכנות, עם התמחות בכלי DevOps מודרניים. 
                    שואף להביא חדשנות ויעילות לתהליכי פיתוח ופריסה. 
                    בוגר מכללת SELA עם מיקוד ב-DevOps ואבטחת מידע.
                </p>
            </div>
            
            <!-- Skills Section -->
            <div class="section">
                <h2><i class="fas fa-tools"></i> כישורים טכניים</h2>
                <div class="skills-grid">
                    <div class="skill-category">
                        <h4><i class="fab fa-docker"></i> DevOps & Containerization</h4>
                        <ul class="skill-list">
                            <li>Docker & Docker Compose</li>
                            <li>Kubernetes (K8s)</li>
                            <li class="skill-placeholder">Jenkins - להוסיף רמת ידע</li>
                            <li class="skill-placeholder">Ansible - להוסיף אם רלוונטי</li>
                            <li class="skill-placeholder">Terraform - להוסיף אם רלוונטי</li>
                        </ul>
                    </div>
                    
                    <div class="skill-category">
                        <h4><i class="fas fa-cloud"></i> Cloud Platforms</h4>
                        <ul class="skill-list">
                            <li class="skill-placeholder">AWS - להוסיף שירותים ספציפיים</li>
                            <li class="skill-placeholder">Azure - להוסיף אם רלוונטי</li>
                            <li class="skill-placeholder">GCP - להוסיף אם רלוונטי</li>
                        </ul>
                    </div>
                    
                    <div class="skill-category">
                        <h4><i class="fas fa-network-wired"></i> רשתות ואבטחה</h4>
                        <ul class="skill-list">
                            <li>Network Administration</li>
                            <li>Network Security</li>
                            <li class="skill-placeholder">אבטחת מידע - להוסיף פרטים</li>
                            <li class="skill-placeholder">Monitoring Tools</li>
                        </ul>
                    </div>
                    
                    <div class="skill-category">
                        <h4><i class="fas fa-code"></i> תכנות ופיתוח</h4>
                        <ul class="skill-list">
                            <li>Python</li>
                            <li>Bash Scripting</li>
                            <li>YAML</li>
                            <li class="skill-placeholder">שפות נוספות - להוסיף</li>
                        </ul>
                    </div>
                    
                    <div class="skill-category">
                        <h4><i class="fas fa-chart-line"></i> Monitoring & CI/CD</h4>
                        <ul class="skill-list">
                            <li class="skill-placeholder">Prometheus - להוסיף אם רלוונטי</li>
                            <li class="skill-placeholder">Grafana - להוסיף אם רלוונטי</li>
                            <li class="skill-placeholder">GitLab CI - להוסיף אם רלוונטי</li>
                            <li class="skill-placeholder">GitHub Actions - להוסיף אם רלוונטי</li>
                        </ul>
                    </div>
                    
                    <div class="skill-category">
                        <h4><i class="fas fa-graduation-cap"></i> למידה נוכחית</h4>
                        <ul class="skill-list">
                            <li>אבטחת מידע - בתהליך למידה</li>
                            <li class="skill-placeholder">נושאים נוספים - להוסיף</li>
                        </ul>
                    </div>
                </div>
            </div>
            
            <!-- Projects Section -->
            <div class="section">
                <h2><i class="fas fa-project-diagram"></i> פרויקטים</h2>
                <div class="projects-grid">
                    <div class="project-card">
                        <h4><i class="fas fa-rocket"></i> DevOps Portfolio Project</h4>
                        <p>פרויקט גמר DevOps מקיף עם Flask, Docker, Kubernetes ו-CI/CD pipeline מלא.</p>
                        <div class="project-tech">
                            <span class="tech-tag">Flask</span>
                            <span class="tech-tag">Docker</span>
                            <span class="tech-tag">Kubernetes</span>
                            <span class="tech-tag">Jenkins</span>
                            <span class="tech-tag">MongoDB</span>
                        </div>
                        <p><a href="https://github.com/MasteRefleX123/devops-portfolio-project" target="_blank">
                            <i class="fab fa-github"></i> View on GitHub
                        </a></p>
                    </div>
                    
                    <div class="project-card">
                        <h4><i class="fas fa-plus"></i> פרויקט נוסף #1</h4>
                        <p class="skill-placeholder">תיאור פרויקט - להוסיף פרטים על פרויקט שעשית</p>
                        <div class="project-tech">
                            <span class="tech-tag skill-placeholder">טכנולוגיה 1</span>
                            <span class="tech-tag skill-placeholder">טכנולוגיה 2</span>
                        </div>
                        <p class="skill-placeholder">קישור GitHub - להוסיף</p>
                    </div>
                    
                    <div class="project-card">
                        <h4><i class="fas fa-plus"></i> פרויקט נוסף #2</h4>
                        <p class="skill-placeholder">תיאור פרויקט - להוסיף פרטים על פרויקט שעשית</p>
                        <div class="project-tech">
                            <span class="tech-tag skill-placeholder">טכנולוגיה 1</span>
                            <span class="tech-tag skill-placeholder">טכנולוגיה 2</span>
                        </div>
                        <p class="skill-placeholder">קישור GitHub - להוסיף</p>
                    </div>
                </div>
            </div>
            
            <!-- Certifications Section -->
            <div class="section">
                <h2><i class="fas fa-certificate"></i> תעודות מקצועיות</h2>
                <div class="certs-grid">
                    <div class="cert-card">
                        <i class="fas fa-graduation-cap"></i>
                        <h4>בוגר מכללת SELA</h4>
                        <p>DevOps Engineering</p>
                        <p><strong>2024</strong></p>
                    </div>
                    
                    <div class="cert-card" style="background: linear-gradient(45deg, #95a5a6, #7f8c8d);">
                        <i class="fab fa-aws"></i>
                        <h4>AWS Certification</h4>
                        <p class="skill-placeholder">להוסייף אם יש/מתוכנן</p>
                        <p class="skill-placeholder">תאריך</p>
                    </div>
                    
                    <div class="cert-card" style="background: linear-gradient(45deg, #3498db, #2980b9);">
                        <i class="fas fa-dharmachakra"></i>
                        <h4>Kubernetes Certification</h4>
                        <p class="skill-placeholder">CKA/CKAD - להוסיף אם יש/מתוכנן</p>
                        <p class="skill-placeholder">תאריך</p>
                    </div>
                    
                    <div class="cert-card" style="background: linear-gradient(45deg, #e67e22, #d35400);">
                        <i class="fab fa-docker"></i>
                        <h4>Docker Certification</h4>
                        <p class="skill-placeholder">להוסיף אם יש/מתוכנן</p>
                        <p class="skill-placeholder">תאריך</p>
                    </div>
                </div>
            </div>
            
            <!-- Contact Section -->
            <div class="contact-info">
                <h2><i class="fas fa-address-card"></i> פרטי יצירת קשר</h2>
                <div class="contact-grid">
                    <div class="contact-item">
                        <i class="fas fa-envelope"></i>
                        <h4>אימייל</h4>
                        <p><a href="mailto:oriyanrwork99@gmail.com" style="color: white;">oriyanrwork99@gmail.com</a></p>
                    </div>
                    
                    <div class="contact-item">
                        <i class="fas fa-map-marker-alt"></i>
                        <h4>מיקום</h4>
                        <p>מודיעין, ישראל</p>
                    </div>
                    
                    <div class="contact-item">
                        <i class="fab fa-github"></i>
                        <h4>GitHub</h4>
                        <p><a href="https://github.com/MasteRefleX123" target="_blank" style="color: white;">MasteRefleX123</a></p>
                    </div>
                    
                    <div class="contact-item">
                        <i class="fab fa-linkedin"></i>
                        <h4>LinkedIn</h4>
                        <p style="color: #ecf0f1;">להוסיף קישור</p>
                    </div>
                    
                    <div class="contact-item">
                        <i class="fas fa-birthday-cake"></i>
                        <h4>גיל</h4>
                        <p>21</p>
                    </div>
                    
                    <div class="contact-item">
                        <i class="fas fa-university"></i>
                        <h4>השכלה</h4>
                        <p>בוגר מכללת SELA - DevOps</p>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy', 
        'app': 'Oriyan Rask DevOps Portfolio',
        'owner': 'אוריין ראסק (Oriyan Rask)',
        'email': 'oriyanrwork99@gmail.com',
        'location': 'מודיעין, ישראל',
        'age': 21,
        'education': 'SELA College Graduate',
        'github': 'https://github.com/MasteRefleX123'
    })

@app.route('/api/stats')
def stats():
    return jsonify({
        'portfolio_owner': 'Oriyan Rask (אוריין ראסק)',
        'email': 'oriyanrwork99@gmail.com',
        'github': 'https://github.com/MasteRefleX123',
        'location': 'מודיעין, ישראל',
        'age': 21,
        'visitors': get_visitor_count(),
        'projects': 3,
        'certifications': 1,
        'experience': 'DevOps Junior Engineer',
        'education': 'SELA College Graduate',
        'specialization': 'DevOps, Networks, Security'
    })

@app.route('/api/skills')
def skills():
    return jsonify({
        'devops_tools': ['Docker', 'Kubernetes', 'Jenkins', 'Git'],
        'cloud_platforms': ['AWS (בתהליך)', 'Azure (בתהליך)'],
        'networking': ['Network Administration', 'Network Security'],
        'programming': ['Python', 'Bash', 'YAML'],
        'security': ['Information Security (בלמידה)'],
        'monitoring': ['בתהליך למידה'],
        'current_learning': ['אבטחת מידע', 'Cloud Technologies']
    })

@app.route('/api/projects')
def projects():
    return jsonify([
        {
            'name': 'DevOps Portfolio Project',
            'description': 'פרויקט גמר DevOps מקיף',
            'technologies': ['Flask', 'Docker', 'Kubernetes', 'Jenkins', 'MongoDB'],
            'github': 'https://github.com/MasteRefleX123/devops-portfolio-project',
            'status': 'בפיתוח'
        }
    ])


# ============================================
# Contact Form Feature
# ============================================

# Initialize contacts collection
try:
    if db is not None:
        contacts_collection = db.contacts
        print("✅ Contacts collection initialized")
except:
    contacts_collection = None
    print("⚠️ Contacts collection not available")

@app.route('/contact')
def contact_page():
    """Render contact form page"""
    html = """
    <!DOCTYPE html>
    <html lang="he" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>צור קשר - אוריין ראסק</title>
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: 'Segoe UI', Arial, sans-serif; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .contact-container {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                max-width: 600px;
                width: 100%;
                padding: 40px;
                animation: slideIn 0.5s ease;
            }
            @keyframes slideIn {
                from { opacity: 0; transform: translateY(30px); }
                to { opacity: 1; transform: translateY(0); }
            }
            h1 {
                color: #333;
                margin-bottom: 10px;
                font-size: 2.5em;
            }
            .subtitle {
                color: #666;
                margin-bottom: 30px;
                font-size: 1.1em;
            }
            .form-group {
                margin-bottom: 25px;
            }
            label {
                display: block;
                margin-bottom: 8px;
                color: #555;
                font-weight: 600;
            }
            input, textarea {
                width: 100%;
                padding: 12px 15px;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                font-size: 16px;
                transition: all 0.3s;
                font-family: inherit;
            }
            input:focus, textarea:focus {
                outline: none;
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            textarea {
                resize: vertical;
                min-height: 120px;
            }
            .btn-submit {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                padding: 15px 40px;
                border-radius: 30px;
                font-size: 18px;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.3s, box-shadow 0.3s;
                width: 100%;
            }
            .btn-submit:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
            }
            .back-link {
                display: inline-block;
                margin-top: 20px;
                color: #667eea;
                text-decoration: none;
                font-weight: 600;
                transition: color 0.3s;
            }
            .back-link:hover {
                color: #764ba2;
            }
            .success-message, .error-message {
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 20px;
                display: none;
            }
            .success-message {
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            .error-message {
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
        </style>
    </head>
    <body>
        <div class="contact-container">
            <h1>צור קשר</h1>
            <p class="subtitle">אשמח לשמוע ממך! מלא את הטופס ואחזור אליך בהקדם</p>
            
            <div class="success-message" id="successMsg">
                <i class="fas fa-check-circle"></i> ההודעה נשלחה בהצלחה! אחזור אליך בקרוב.
            </div>
            
            <div class="error-message" id="errorMsg">
                <i class="fas fa-exclamation-circle"></i> אופס! משהו השתבש. אנא נסה שוב.
            </div>
            
            <form id="contactForm">
                <div class="form-group">
                    <label for="name">שם מלא *</label>
                    <input type="text" id="name" name="name" required>
                </div>
                
                <div class="form-group">
                    <label for="email">כתובת אימייל *</label>
                    <input type="email" id="email" name="email" required>
                </div>
                
                <div class="form-group">
                    <label for="message">הודעה *</label>
                    <textarea id="message" name="message" required></textarea>
                </div>
                
                <button type="submit" class="btn-submit">
                    <i class="fas fa-paper-plane"></i> שלח הודעה
                </button>
            </form>
            
            <a href="/" class="back-link">
                <i class="fas fa-arrow-right"></i> חזרה לדף הבית
            </a>
        </div>
        
        <script>
            document.getElementById('contactForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const formData = {
                    name: document.getElementById('name').value,
                    email: document.getElementById('email').value,
                    message: document.getElementById('message').value
                };
                
                try {
                    const response = await fetch('/api/contact', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(formData)
                    });
                    
                    const result = await response.json();
                    
                    if (response.ok) {
                        document.getElementById('successMsg').style.display = 'block';
                        document.getElementById('errorMsg').style.display = 'none';
                        document.getElementById('contactForm').reset();
                        
                        setTimeout(() => {
                            document.getElementById('successMsg').style.display = 'none';
                        }, 5000);
                    } else {
                        throw new Error(result.error || 'Failed to send message');
                    }
                } catch (error) {
                    document.getElementById('errorMsg').style.display = 'block';
                    document.getElementById('successMsg').style.display = 'none';
                    
                    setTimeout(() => {
                        document.getElementById('errorMsg').style.display = 'none';
                    }, 5000);
                }
            });
        </script>
    </body>
    </html>
    """
    return html

@app.route('/api/contact', methods=['POST'])
def submit_contact():
    """Handle contact form submission"""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['name', 'email', 'message']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        # Create contact document
        contact = {
            'name': data.get('name'),
            'email': data.get('email'),
            'message': data.get('message'),
            'timestamp': datetime.now(timezone.utc),
            'status': 'new',
            'ip': request.remote_addr
        }
        
        # Save to MongoDB if available
        if contacts_collection is not None:
            result = contacts_collection.insert_one(contact)
            contact['_id'] = str(result.inserted_id)
            print(f"✅ New contact form submission from {contact['name']}")
        else:
            print(f"⚠️ Contact form submitted but MongoDB not available: {contact['name']}")
        
        # Convert datetime for JSON response
        contact['timestamp'] = contact['timestamp'].isoformat()
        
        return jsonify({
            'status': 'success',
            'message': 'Thank you for your message! I will get back to you soon.',
            'contact_id': contact.get('_id', 'temp-id')
        }), 201
        
    except Exception as e:
        print(f"Error submitting contact form: {e}")
        return jsonify({'error': 'Failed to submit contact form'}), 500

@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    """Get all contact form submissions (admin endpoint)"""
    try:
        # Check for simple auth header
        auth = request.headers.get('Authorization')
        if auth != 'Bearer admin-secret-key':
            return jsonify({'error': 'Unauthorized'}), 401
        
        if contacts_collection is not None:
            contacts = list(contacts_collection.find().sort('timestamp', -1))
            
            # Convert ObjectId and datetime for JSON
            for contact in contacts:
                contact['_id'] = str(contact['_id'])
                contact['timestamp'] = contact['timestamp'].isoformat()
            
            return jsonify({
                'total': len(contacts),
                'contacts': contacts
            })
        else:
            return jsonify({'total': 0, 'contacts': []})
            
    except Exception as e:
        print(f"Error getting contacts: {e}")
        return jsonify({'error': 'Failed to retrieve contacts'}), 500

if __name__ == '__main__':
    print('🚀 Oriyan Rask DevOps Portfolio Starting...')
    print('📧 Contact: oriyanrwork99@gmail.com')
    print('🌐 Access at: http://localhost:5000')
    print('📂 GitHub: https://github.com/MasteRefleX123')
    # Disable debug by default for production safety; enable via FLASK_DEBUG=true if needed
    debug_flag = os.getenv('FLASK_DEBUG', 'False').lower() in ('1', 'true', 'yes')
    app.run(host='0.0.0.0', port=5000, debug=debug_flag)

@app.route('/api/visitors', methods=['GET', 'POST'])
def visitors_api():
    """Handle visitor tracking and retrieval"""
    if request.method == 'POST':
        # Manual visitor tracking
        track_visitor()
        return jsonify({'status': 'visitor tracked', 'total': get_visitor_count()})
    else:
        # Get visitor stats
        try:
            if visitors_collection is not None:
                total = get_visitor_count()
                recent = list(visitors_collection.find().sort('timestamp', -1).limit(10))
                # Convert ObjectId to string for JSON serialization
                for visit in recent:
                    visit['_id'] = str(visit['_id'])
                    visit['timestamp'] = visit['timestamp'].isoformat()
                
                return jsonify({
                    'total_visitors': total,
                    'recent_visitors': recent
                })
        except Exception as e:
            print(f"Error getting visitor data: {e}")
        
        return jsonify({'total_visitors': get_visitor_count(), 'recent_visitors': []})
