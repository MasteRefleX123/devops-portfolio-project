# DevOps Portfolio Project – Summary

## עדכון מהיום (CI/CD + Deploy)
- Build+Tests: ירוקים ב‑Jenkins.
- Push: תוקן `Jenkinsfile` – התחברות לדוקר דרך Credentials (`docker-hub`) עם נפילה חזרה ל‑ENV אם חסר.
- Deploy: תוקן `Jenkinsfile` לשימוש ב‑`kubectl config set-cluster` ולקישור לרשת `kind` (עודכן `jenkins/docker-compose.yml`).
- Root cause של עיכוב rollout: kubeconfig לא הוזרק ל‑Jenkins. נדרש `KUBECONFIG_BASE64` בעת הפעלת compose.

### עדכון מהסשן הנוכחי
- עודכן ngrok וה‑Webhook הוגדר אוטומטית ל‑URL הנוכחי (לדוגמה: `https://1669a04e3ddc.ngrok-free.app/github-webhook/`).
- הופעלה דחיפה/טריגר ל‑Jenkins (עם Crumb+Cookie) אחרי ריסטרט; ה‑Job רץ תקין עד שלב ה‑Build.
- כשל Build #36: Docker build נפל כי `requirements.txt` לא עבר לקונטקסט (בגלל כלל ב‑`.dockerignore`).
- תיקון: עודכן `.dockerignore` כדי לא לחסום קבצי `.txt` וכדי לכלול `requirements.txt` בקונטקסט.
- Build #37: עבר את ה‑Build+Push, הגיע ל‑Deploy; ה‑rollout נכשל ב‑timeout (180s) – יש לאבחן את מצב ה‑Deployment/Pods.

### מה בוצע בקוד
- `Jenkinsfile`:
  - הסרה של דחיפת `latest` והקשחה של תנאי ריצה.
  - התחברות Docker Hub: קודם Credentials, fallback ל‑`DOCKERHUB_USER/PASS`.
  - Deploy: הכנת kubeconfig זמני והפניה ל‑`https://devops-portfolio-control-plane:6443`, `rollout status` עם timeout.
- `jenkins/docker-compose.yml`: חיבור לרשת `kind` כדי לאפשר גישה ל‑API Server.

### מה נשאר לסגור
1) לוודא שב‑Jenkins קיימים ENV: `KUBECONFIG_BASE64`, `DOCKERHUB_USER`, `DOCKERHUB_PASS` (נטען דרך `.env` או סוד). לאחר מכן להריץ Pipeline עד סוף Deploy.
2) לאחר rollout: לאמת `http://localhost:5001/` + `/:200`, `/status:200`, `/health:200`, `/metrics:200`.
3) Prometheus: ה‑Target של `portfolio-service` במצב `UP`; לתקן `ServiceMonitor`/תוויות אם צריך.
4) לקבע תגית image לא‑`latest` ב‑`k8s/deployment.yaml` (לתג שבנינו) ולדחוף ל‑`gitops-staging`.
5) להחזיר Argo CD ל‑`main` ולבצע Sync → Merge.

### הפעלה מהירה ל‑Jenkins עם kubeconfig
```
cd /mnt/c/Users/momir/devops-portfolio-project
set +H
cat > .env <<EOF
GITHUB_TOKEN=
DOCKERHUB_USER=mastereflex123
DOCKERHUB_PASS=***
KUBECONFIG_BASE64=$(kubectl config view --raw | base64 -w0)
EOF
docker compose -f jenkins/docker-compose.yml --env-file .env up -d
```

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
