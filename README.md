# DevOps Portfolio Project 🚀

פרויקט פורטפוליו DevOps מקיף - **Oriyan Rask**

## 📋 תיאור הפרויקט
אפליקציית Flask מתקדמת עם MongoDB, Docker, Kubernetes ו-CI/CD pipeline מלא.

## ✨ תכונות עיקריות
- 🌐 Flask Web Application
- 📊 MongoDB Database
- 🐳 Docker Containerization  
- ☸️ Kubernetes Orchestration
- ✅ 92% Test Coverage

## 🚀 התחלה מהירה

### הרצה מקומית
```bash
git clone https://github.com/OriyanHemo/devops-portfolio-project.git
cd devops-portfolio-project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python oriyan_portfolio.py
```

### הרצה עם Docker
```bash
docker build -t portfolio:v1.1 .
docker run -d -p 5000:5000 portfolio:v1.1
```

### הרצה עם Docker Compose
```bash
docker compose up -d
```

## 📊 בדיקות
```bash
pytest tests/ --cov=oriyan_portfolio --cov-report=term-missing
```
- ✅ 28/28 tests passing
- 📊 92% code coverage

## 👤 Contact
**Oriyan Rask**
- 📧 oriyanrwork99@gmail.com
- 💼 GitHub: [MasteRefleX123](https://github.com/MasteRefleX123)

---
Built with ❤️ by Oriyan Rask | DevOps Course 2024
