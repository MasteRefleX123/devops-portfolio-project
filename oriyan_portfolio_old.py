from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
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
                        <p class="skill-placeholder">להוסיف אם יש/מתוכנן</p>
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
        'visitors': 42,
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

if __name__ == '__main__':
    print('🚀 Oriyan Rask DevOps Portfolio Starting...')
    print('📧 Contact: oriyanrwork99@gmail.com')
    print('🌐 Access at: http://localhost:5000')
    print('📂 GitHub: https://github.com/MasteRefleX123')
    app.run(host='0.0.0.0', port=5000, debug=True)
