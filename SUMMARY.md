# DevOps Portfolio Project – Summary

## סיכום קצר של היום
- הועברנו ל‑GitOps: ה‑Jenkinsfile מעדכן את `gitops-staging` עם תגית התמונה (GITOPS_MODE=true) + רענון ArgoCD.
- נוספו ArgoCD Gates (אופציונלי, skip‑safe) לאחר פריסה.
- הוסר `k8s/mongodb.yaml` מסניף `gitops-staging` כדי למנוע Drift; נשאר רק StatefulSet.
- תיעוד חדש: `docs/Architecture.md`, `docs/Operations.md` (מפה ארכיטקטונית ומדריך תפעולי מהיר).
- שמירה על הקשחה נגד `:latest` בכל השלבים.

מה נותר קצר לפני PR:
- להגדיר Branch Protection ל‑`main` (נבצע בסוף, לפי החלטתך).
- אופציונלי: הפעלת עדכון תגובה אוטומטי ב‑PR (כבר מוכן בפייפליין כ‑optional).

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

## מצב נוכחי (מעודכן)
- אפליקציה: Flask עם `/metrics`, רצה ב‑Kubernetes (`namespace: oriyan-portfolio`).
  - Deployment: `oriyan-portfolio-app` על `mastereflex123/portfolio:v37-0000360` — rollout ירוק 2/2.
  - Service: `portfolio-service` (80→5000). Smoke: `/health=200`, `/api/contact=201`.
- CI/CD (Jenkins): multibranch `devops-portfolio` עם Webhook פעיל (ngrok). Build→Test→BuildKit→Push→Deploy→Smoke.
  - הקשחות: כשל על `:latest`; בדיקת מניפסטים נגד `:latest`.
- GitOps (ArgoCD): Application `portfolio-app` מסונכרן ל‑`gitops-staging` (נתיב `k8s/`).
  - image בקבצי GitOps מקובע ל‑`v37-0000360` למניעת drift.
- Monitoring: Prometheus (9090) + Grafana (3000) פעילים; דשבורד "Portfolio App Overview" פרוביז׳נד; חוקים ל‑5xx/p90 latency נטענו.
- קרדנשלז ב‑Jenkins:
  - `docker-hub-credentials` (Username/Password)
  - `github-credentials` (token)
  - `kubeconfig` (Secret file `config`)

## סטטוס Pipeline
- שלבים: Test → Build (Docker BuildKit) → Push (Docker Hub) → Deploy (kubectl set image + rollout) → Smoke.
- תנאי ריצה ל‑Push/Deploy: `main` או `feature/day2-docker-kubernetes`.

## בעיות/סיכונים שנותרו
- Drift (נפתר): ArgoCD החזיר בעבר `:latest`. ננעל בקבצים ל‑`v37-0000360`. להקפיד commits דרך GitOps בלבד.
- Branch protection: להפעיל בסיום (Required status + review) — מתוכנן.
- Helm: יש Helm chart, אך ArgoCD עוד מסנכרן מניפסטים — הסבה ל‑Helm אחרי ה‑PR.

## מה נשאר (לפני ה‑PR)
1) לעדכן/לנקות מסמכים: SUMMARY (מסמך זה) + Runbook קצר (rollout).  
2) ArgoCD gates בפייפליין (skip‑safe כשאין CLI).  
3) Lighten Setup בשלב Jenkins (שיפור זמני build).  
4) Refactor docs (docs/Architecture, docs/Operations) — ניווט קל.

## אחרי ה‑PR (להשלמת הדרישות)
- להעביר את ArgoCD לצרוך Helm chart (`helm/`) ו‑values (image.tag).  
- להרחיב Jenkinsfile: feature → helm lint/template; main → helm package/push (OCI/DockerHub).  
- להעביר Prometheus+Grafana להתקנת Helm (kube‑prometheus‑stack) ולהשבית compose.  
- להפעיל Branch protection ל‑`main`.

## פעולות מהירות
```
# הפעלה כוללת (לוקאלית)
./start-all.sh

# עדכון Webhook לאחר פתיחת ngrok
./update-github-webhook-safe.sh

# בדיקות מקומיות
pytest tests/ --cov=oriyan_portfolio --cov-report=term-missing

# אימות מהיר (לאחר פריסה)
kubectl -n oriyan-portfolio get deploy oriyan-portfolio-app -o jsonpath='{.status.readyReplicas}/{.status.replicas} {.spec.template.spec.containers[0].image}{"\n"}'
pkill -f "port-forward.*5001:80" 2>/dev/null || true; nohup kubectl -n oriyan-portfolio port-forward svc/portfolio-service 5001:80 >/dev/null 2>&1 &
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:5001/health   # מצופה 200
curl -s -X POST -H "Content-Type: application/json" -d '{"name":"t","email":"a@b.c","message":"x"}' -o /dev/null -w "%{http_code}\n" http://localhost:5001/api/contact  # מצופה 201
```

## איך אפשר לעזור כעת
- לאשר שה־Docker Hub creds מעודכנים (משתמש/סיסמה פעילים).
- לוודא שיש מקום בדיסק ל‑build/push.
- אם ה‑Deploy ייפול: לשלוח לי את 30 השורות האחרונות מה‑Console של Jenkins.
