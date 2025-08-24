# DevOps Portfolio Project – Summary

## מצב נוכחי
- אפליקציה: Flask עם `/metrics`, רצה ב-Kubernetes (namespace: `oriyan-portfolio`), Service `portfolio-service` מאזין ל-HTTP.
- CI/CD: Jenkins Job `devops-portfolio` על הסניף `feature/day2-docker-kubernetes`, טריגר GitHub Webhook פעיל.
- סודות: מנוהלים ב-JCasC (`jenkins/jenkins-casc.yaml`) – `github-token`, `docker-hub`, `kubeconfig` (מבוסס `KUBECONFIG_BASE64`).
- ניטור: Prometheus + Grafana מוגדרים; יש `ServiceMonitor` ו-`PrometheusRule` לאפליקציה.

## נקודות עיקריות
- Endpoints מקומיים:
  - Jenkins: http://localhost:8080
  - אפליקציה: http://localhost:5001
  - Health: http://localhost:5001/health
  - Metrics: http://localhost:5001/metrics
- Ngrok: נפתח ע"י `./start-all.sh`; עדכון ה-Webhook מתבצע ע"י `update-github-webhook-safe.sh`.

## סטטוס Pipeline
- שלבים: Build → Test (pytest+cov) → Docker Build/Tag → Push (main/feature) → Deploy (kubectl set image + rollout).
- Credentials נדרשים: `docker-hub`, `github-token`, `kubeconfig`.
- הערות יציבות:
  - `post { always { cleanWs() } }` קיים.
  - Push/Deploy רק על `main` או `feature/day2-docker-kubernetes`.

## פעולות מהירות
```bash
# הפעלה כוללת
./start-all.sh

# עדכון Webhook לאחר פתיחת Ngrok
./update-github-webhook-safe.sh

# בדיקות מקומיות
pytest tests/ --cov=oriyan_portfolio --cov-report=term-missing

# Grafana (אם 3000 תפוס)
kubectl -n monitoring port-forward svc/kps-grafana 3001:80
```

## בעיות ידועות/מעקב
- Jenkins Plugins/Setup: להשלים התקנה; ללא זה ייתכן CSRF ב-API.
- Pipeline: לוודא קיום Credentials ולפתור כשלים נקודתיים אם יצוצו.
- Monitoring: לוודא שה-`ServiceMonitor` מזהה Targets וה-`up` של האפליקציה = 1.

## צעדים הבאים
1) להשלים התקנת פלאגינים ב-Jenkins ולאמת גישת Admin.
2) לאמת/ליצור Credentials: `github-token`, `docker-hub`, `kubeconfig`.
3) להריץ Build ב-Jenkins ולטפל בכשלים במידת הצורך.
4) לוודא ש-Prometheus מגרד את `/metrics` ו-Dashboard מציג נתונים.
