from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1 style="text-align:center;color:#007bff;">🚀 DevOps Portfolio</h1>
    <div style="text-align:center;font-family:Arial;">
        <p>Cloud & DevOps Specialist Portfolio</p>
        <p><a href="/health">Health Check</a> | <a href="/api/stats">API Stats</a></p>
        <h3>Skills: Docker, Kubernetes, Jenkins, AWS</h3>
        <h3>Certifications: AWS SAA, CKA, Docker</h3>
    </div>
    '''

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'app': 'DevOps Portfolio'})

@app.route('/api/stats')
def stats():
    return jsonify({'visitors': 100, 'projects': 5, 'certs': 3})

if __name__ == '__main__':
    print('🚀 DevOps Portfolio Starting...')
    app.run(host='0.0.0.0', port=5000, debug=True)
