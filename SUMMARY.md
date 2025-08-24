# DevOps Portfolio Project – Summary

## מצב נוכחי (עדכני)
- אפליקציה: Flask עם `/metrics`, רצה ב‑Kubernetes (`namespace`: `oriyan-portfolio`), Service `portfolio-service` מאזין ל‑HTTP (NodePort + port‑forward ל‑5001).
- GitOps: Argo CD מותקן ורץ; ה‑Application מצביע ל‑`gitops-staging` (לא נוגעים ב‑`main` עד שהכול ירוק).
- CI/CD (Jenkins): Job על `feature/day2-docker-kubernetes`, טריגר GitHub Webhook פעיל (ngrok מעודכן).
- תלויות/סודות ב‑Jenkins: `docker-hub-credentials`, `github-credentials`, `kubeconfig` (Secret file).
- מצב פריסה: מיוצב על image `mastereflex123/portfolio:v3.2` כדי למנוע CrashLoop; התמונה החדשה עם תיקון `prometheus_client` תיפרס כשתהליך ה‑build יסתיים.
- Monitoring: kube‑prometheus‑stack מותקן; Grafana בפורט‑פורוורד 3000; Prometheus בפורט‑פורוורד 9090; ServiceMonitor מוגדר ל‑`portfolio-service`.
- UI/תוכן: עודכנו צבעים (כחול/תכלת/טורקיז), תכני 2025, Azure/GCP, הוסף דף `/status` (יזדקק לפריסה עם image עדכני), טופס `/contact` שומר ל‑MongoDB; תמיכה בהתראה באימייל דרך Gmail (ENV: `GMAIL_USER`/`GMAIL_APP_PASSWORD`).

## סטטוס Pipeline
- שלבים: Test → Build Docker Image → Push (Docker Hub) → Deploy (kubectl set image + rollout)
- Push/Deploy רצים על `main` או `feature/day2-docker-kubernetes`. נדרשת השלמת build כדי לפרוס את ה‑image העדכני (עם `prometheus_client`).

## בעיות/סיכונים שנותרו
- Jenkins build ל‑image עדכני טרם הושלם → כרגע רץ `v3.2`; נעבור ל‑`latest` כש‑build יסתיים.
- Grafana login redirect loop בדפדפן מסוים: לפתור ע"י ניקוי cookies/site‑data או להגדיר `root_url` אם נדרש; ניתן גם לבצע restart לפוד Grafana.
- Prometheus: לאשר שה‑target של האפליקציה UP (דרך Status → Targets) וש‑ServiceMonitor קולט את ה‑Service.
- Gmail התראה מהטופס: דורש `GMAIL_USER` ו‑`GMAIL_APP_PASSWORD` (App Password) ו/או `GMAIL_NOTIFY_TO`.
- /status יופיע רק לאחר פריסת ה‑image החדש (נכון לעכשיו בקוד, לא בתמונה היציבה).

## צ'ק‑ליסט לפני מיזוג ל‑main
1) Jenkins: להשלים build+push של image עדכני (עם תיקון `prometheus_client`).
2) GitOps‑staging: לעדכן ל‑`image:latest` (או תגית ספציפית חדשה), לבצע rollout ולוודא שכל הפודים Ready.
3) אפליקציה: לוודא `http://localhost:5001/` נטען; `/status`, `/health` ו‑`/metrics` מחזירים 200.
4) Monitoring: ב‑Prometheus ה‑target UP; ב‑Grafana הדאשבורד "portfolio‑overview" נטען ועם נתונים.
5) Grafana: אם יש redirect loop, לנקות cookies+cache לדומיין `localhost:3000` או לבצע restart לפוד; כניסה עם `admin/prom-operator` (ברירת מחדל).
6) כש‑staging ירוק לגמרי: להחזיר את Argo CD ל‑`main` ולמזג PR.

## צעדים הבאים (גימור והברקה)
- Grafana: להבטיח `root_url` תקין אם יש צורך (בעת חשיפה מאחורי proxy), ולהוסיף דשבורדים משלימים.
- אבטחה: שקילת TLS עם cert‑manager ל‑Ingress; Sealed‑Secrets/External‑Secrets לסודות.
- GitOps מלא: לעבור לתגיות image ספציפיות (לא `latest`), ולהסיר Deploy אימפרטיבי מג'נקינס.

## פעולות מהירות
```
# הפעלה כוללת (לוקאלית)
./start-all.sh

# עדכון Webhook לאחר פתיחת ngrok
./update-github-webhook-safe.sh

# בדיקות מקומיות
pytest tests/ --cov=oriyan_portfolio --cov-report=term-missing
```

## מה צריך לעשות עכשיו (רשימת ביצוע קצרה)
- לאשר ש‑Jenkins מסיים build+push לתמונה העדכנית.
- לעדכן את ה‑Deployment ב‑staging ל‑image החדש ולהמתין ל‑rollout ירוק.
- לאמת אתר/סטטוס/מטריקות, Prometheus Targets, ו‑Grafana Dashboard.
- להחזיר את Argo CD ל‑`main` ולמזג.
