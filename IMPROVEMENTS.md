# רשימת שיפורים מומלצים

## אבטחה וקונפיג
- להעביר סודות של docker-compose לקובץ `.env` ולהשתמש ב-`env_file:`
- לאחד גרסת MongoDB (למשל 7.0 בקוברנטיס וב-compose)
- לחזק סיסמאות של MongoDB וממשק mongo-express

## ייצור וניטור
- להעביר Prometheus+Grafana לקלאסטר (Helm/ kube-prometheus-stack)
- להוסיף חוקי התראות בסיסיים (CPU, Memory, Errors rate)
- ליצור Dashboards ייעודיים לאפליקציה (HTTP, Latency)

## CI/CD
- לאמת ש-Jenkins job מסומן עם "GitHub hook trigger for GITScm polling"
- להוסיף דוחות כיסוי בדיקות לפייפליין (pytest-cov HTML)
- להוסיף סריקת תמונה (Trivy) ו-lint ל-Helm/K8s

## אפליקציה
- להפריד קובץ קונפיג ולהעמיס משתני סביבה מסודרים
- להקטין לוגים/PII וליצור rotation לתיקיית `logs/`

## תפעול
- לשקול Helm chart מלא ולשלב ArgoCD לפריסה אוטומטית
- להוסיף README ל-monitoring עם הוראות הפעלה קצרות
