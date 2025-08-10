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
        <style>
            body { 
                font-family: 'Segoe UI', Arial, sans-serif; 
                margin: 0; 
                padding: 20px;
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                min-height: 100vh;
            }
            .container { max-width: 1000px; margin: 0 auto; }
            .hero { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; 
                padding: 50px; 
                border-radius: 15px; 
                text-align: center;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                margin-bottom: 30px;
            }
            .hero h1 { margin: 0 0 10px 0; font-size: 2.5em; }
            .hero h2 { margin: 0 0 20px 0; font-size: 1.5em; opacity: 0.9; }
            .hero p { margin: 10px 0; font-size: 1.1em; }
            .quote { 
                font-style: italic; 
                font-size: 1.2em; 
                border: 2px solid rgba(255,255,255,0.3); 
                padding: 15px; 
                border-radius: 10px; 
                margin: 20px 0;
                background: rgba(255,255,255,0.1);
            }
            .btn { 
                background: #007bff; 
                color: white; 
                padding: 12px 25px; 
                text-decoration: none; 
                border-radius: 25px; 
                margin: 10px; 
                display: inline-block;
                transition: all 0.3s ease;
                border: 2px solid transparent;
            }
            .btn:hover { 
                background: white; 
                color: #007bff; 
                border: 2px solid #007bff;
                transform: translateY(-2px);
            }
            .section { 
                background: white; 
                padding: 30px; 
                border-radius: 15px; 
                margin: 20px 0; 
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }
            .skills-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }
            .skill-item {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                border-left: 4px solid #007bff;
            }
            .contact-info { 
                background: #e3f2fd; 
                padding: 25px; 
                border-radius: 10px; 
                text-align: center;
                border: 2px solid #2196f3;
            }
            .emoji { font-size: 1.5em; margin-left: 10px; }
            .highlight { color: #007bff; font-weight: bold; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="hero">
                <h1>🚀 אוריין ראסק</h1>
                <h2>Oriyan Rask - DevOps Junior Engineer</h2>
                <p><strong>בוגר מכללת SELA</strong> | בן 21 | מודיעין, ישראל 🇮🇱</p>
                <p>שאפתני ומקצועי עם רקע ברשתות ובתכנות</p>
                <p>מתקדם ללמידה של <span class="highlight">אבטחת מידע</span> 🔒</p>
                <div class="quote">
                    "מעוניין לשנות את העולם ולעשות את זה עם חיוך 😊"
                </div>
                <a href="https://github.com/MasteRefleX123" target="_blank" class="btn">
                    <span class="emoji">📂</span> GitHub Profile
                </a>
                <a href="mailto:oriyanrwork99@gmail.com" class="btn">
                    <span class="emoji">📧</span> צור קשר
                </a>
                <a href="/health" class="btn">
                    <span class="emoji">❤️</span> Health Check
                </a>
                <a href="/api/stats" class="btn">
                    <span class="emoji">📊</span> API Stats
                </a>
            </div>
            
            <div class="section">
                <h2>🎯 אודותיי</h2>
                <p>DevOps ג'וניור עם <strong>תשוקה לטכנולוגיה וללמידה מתמדת</strong>.</p>
                <p>רקע חזק ברשתות ותכנות, עם התמחות בכלי DevOps מודרניים.</p>
                <p>שואף להביא חדשנות ויעילות לתהליכי פיתוח ופריסה.</p>
                <p>בוגר מכללת SELA עם מיקוד ב-DevOps ואבטחת מידע.</p>
            </div>
            
            <div class="section">
                <h2>🛠️ כישורים טכניים</h2>
                <div class="skills-grid">
                    <div class="skill-item">
                        <h3>🐳 DevOps Tools</h3>
                        <p>Docker, Kubernetes, Jenkins, Git</p>
                    </div>
                    <div class="skill-item">
                        <h3>🌐 רשתות</h3>
                        <p>Network Administration, Security</p>
                    </div>
                    <div class="skill-item">
                        <h3>💻 תכנות</h3>
                        <p>Python, Bash, YAML</p>
                    </div>
                    <div class="skill-item">
                        <h3>🔒 אבטחת מידע</h3>
                        <p>Security Best Practices, Monitoring</p>
                    </div>
                </div>
            </div>
            
            <div class="contact-info">
                <h3>📧 פרטי יצירת קשר</h3>
                <p><strong>אימייל:</strong> <a href="mailto:oriyanrwork99@gmail.com">oriyanrwork99@gmail.com</a></p>
                <p><strong>מיקום:</strong> מודיעין, ישראל</p>
                <p><strong>GitHub:</strong> <a href="https://github.com/MasteRefleX123" target="_blank">MasteRefleX123</a></p>
                <p><strong>גיל:</strong> 21</p>
                <p><strong>השכלה:</strong> בוגר מכללת SELA - DevOps</p>
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
        'owner': 'אוריין ראסק',
        'email': 'oriyanrwork99@gmail.com',
        'location': 'מודיעין, ישראל'
    })

@app.route('/api/stats')
def stats():
    return jsonify({
        'portfolio_owner': 'Oriyan Rask',
        'email': 'oriyanrwork99@gmail.com',
        'github': 'https://github.com/MasteRefleX123',
        'visitors': 42,
        'projects': 3,
        'certifications': 'בהכנה',
        'experience': 'DevOps Junior',
        'education': 'SELA College Graduate'
    })

@app.route('/api/about')
def about():
    return jsonify({
        'name': 'אוריין ראסק (Oriyan Rask)',
        'age': 21,
        'location': 'מודיעין, ישראל',
        'role': 'DevOps Junior Engineer',
        'education': 'בוגר מכללת SELA',
        'background': 'רקע ברשתות ובתכנות',
        'learning': 'מתקדם ללמידה של אבטחת מידע',
        'motto': 'מעוניין לשנות את העולם ולעשות את זה עם חיוך',
        'passion': 'תשוקה לטכנולוגיה וללמידה'
    })

if __name__ == '__main__':
    print('�� Oriyan Rask DevOps Portfolio Starting...')
    print('📧 Contact: oriyanrwork99@gmail.com')
    print('🌐 Access at: http://localhost:5000')
    app.run(host='0.0.0.0', port=5000, debug=True)
