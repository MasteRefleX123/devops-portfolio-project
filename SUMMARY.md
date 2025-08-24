# DevOps Portfolio Project – Summary

## מצב נוכחי
- אפליקציה: Flask עם `/metrics`, רצה ב-Kubernetes (namespace: `oriyan-portfolio`), Service `portfolio-service` מאזין ל-HTTP.
- CI/CD (Jenkins): Job `devops-portfolio` על `feature/day2-docker-kubernetes`, טריגר GitHub Webhook פעיל (ngrok OK).
- סודות/קרדנשלז ב-Jenkins (מאושרים):
  - `docker-hub-credentials` (Username/Password)
  - `github-credentials` (Username/Password לטוקן GitHub, בשימוש ל-SCM/טריגר)
  - `kubeconfig` (Secret file בשם `config`)
- שיפורים שבוצעו היום:
  - תוקנו בדיקות Pytest (fixture `client`, תמיכת UTF‑8, מטריקות Prometheus עם Registry ייעודי).
  - `Jenkinsfile`: שלב Setup Tools (Python, Docker CLI, kubectl), יישור IDs של קרדנשלז, הפעלת venv תואמת sh.
  - /api/contact מחזיר כעת `success=true` בהתאם לבדיקות.

## סטטוס Pipeline
- שלבים: Test → Build Docker Image → Push (Docker Hub) → Deploy (kubectl set image + rollout)
- תנאי ריצה ל-Push/Deploy: סניף `main` או `feature/day2-docker-kubernetes` (אנחנו על feature, כך שמורשה).

## בעיות/סיכונים שנותרו
- Docker Push: תלוי בהרשאות ותפוסת דיסק. אם push ייכשל → לאמת `docker-hub-credentials` ולבדוק קצב/ratelimit.
- Deploy: דורש kubeconfig תקין והרשאות לקלאסטר. אם `kubectl` ייכשל → לבדוק את ה־Secret file `kubeconfig` ולוודא שהקלאסטר נגיש.
- Monitoring: לאחר Deploy לאמת מטריקות ב‑Prometheus וגרפים ב‑Grafana (kube‑prometheus‑stack).

## מה נשאר כדי לסגור את היום (Day 5)
1) להריץ Build ירוק עד הסוף (כולל Push/Deploy).
2) לאשר rollout תקין ולבדוק `/health` ו‑`/metrics` (200).
3) לאמת ב‑Prometheus שה‑Service נבחר ע"י ServiceMonitor; וב‑Grafana שהדאשבורד מציג נתונים.

## צעדים הבאים (לקראת Argo CD)
- להכין/לתקף Helm chart (תיקיית `helm/`).
- התקנת Argo CD (`namespace: argocd`) והגדרת Application (או App‑of‑Apps) שמצביע על הריפו.
- לחבר את הפייפליין: bump גרסת image ב‑values → commit → Argo מסנכרן אוטומטית לקלאסטר.

## פעולות מהירות
```
# הפעלה כוללת (לוקאלית)
./start-all.sh

# עדכון Webhook לאחר פתיחת ngrok
./update-github-webhook-safe.sh

# בדיקות מקומיות
pytest tests/ --cov=oriyan_portfolio --cov-report=term-missing
```

## איך אפשר לעזור כעת
- לאשר שה־Docker Hub creds מעודכנים (משתמש/סיסמה פעילים).
- לוודא שיש מקום בדיסק ל‑build/push.
- אם ה‑Deploy ייפול: לשלוח לי את 30 השורות האחרונות מה‑Console של Jenkins.
