## Rollout Runbook – Portfolio App

מטרה: להחזיר rollout לירוק (2/2 Ready), למנוע drift, ולאשר smoke (/health, /api/contact).

### 1) זיהוי מצב
```bash
kubectl -n oriyan-portfolio get deploy oriyan-portfolio-app \
  -o jsonpath='{.status.readyReplicas}/{.status.replicas} {.spec.template.spec.containers[0].image}{"\n"}'
kubectl -n oriyan-portfolio get rs -l app=portfolio,component=backend \
  -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.template.spec.containers[0].image}{"\n"}{end}'
kubectl -n oriyan-portfolio get pods -l app=portfolio,component=backend \
  -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[0].image}{"\t"}{.status.phase}{"\n"}{end}'
```

אם מזהים drift (תמונה `:latest`): לרוב ArgoCD מחזיר לשם.

### 2) טיפול ב‑drift (ArgoCD)
```bash
# השהיית sync זמנית (אם automated קיים)
kubectl -n argocd patch application portfolio-app --type=json \
  -p='[{"op":"remove","path":"/spec/syncPolicy/automated"}]' || true

# הצמדה ל‑tag התקין בקלאסטר
kubectl -n oriyan-portfolio set image deploy/oriyan-portfolio-app \
  portfolio-app=mastereflex123/portfolio:<TAG>

# ניקוי RS/Pods של :latest (אם קיימים)
kubectl -n oriyan-portfolio delete rs -l app=portfolio,component=backend --ignore-not-found
kubectl -n oriyan-portfolio rollout status deploy/oriyan-portfolio-app --timeout=180s
```

### 3) Smoke – שירות אפליקציה
```bash
pkill -f "port-forward.*5001:80" 2>/dev/null || true
nohup kubectl -n oriyan-portfolio port-forward svc/portfolio-service 5001:80 >/dev/null 2>&1 &
sleep 2
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:5001/health    # מצופה 200
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"name":"t","email":"a@b.c","message":"x"}' \
  -o /dev/null -w "%{http_code}\n" http://localhost:5001/api/contact     # מצופה 201
```

### 4) תיקון בקבצי GitOps (קבוע)
```bash
git checkout gitops-staging
sed -i 's|image: mastereflex123/portfolio:.*|image: mastereflex123/portfolio:<TAG>|' k8s/deployment.yaml
git add k8s/deployment.yaml && git commit -m "gitops: pin portfolio image to <TAG>" && git push
kubectl -n argocd annotate application portfolio-app argocd.argoproj.io/refresh=hard --overwrite
```

לאחר מכן ניתן להחזיר automated אם רוצים:
```bash
kubectl -n argocd patch application portfolio-app --type=merge \
  -p='{"spec":{"syncPolicy":{"automated":{"prune":true,"selfHeal":true}}}}'
```

### 5) MongoDB – מקור אמת אחד
אם קיימים גם Deployment וגם StatefulSet ל‑MongoDB:
```bash
kubectl -n oriyan-portfolio delete deploy mongodb   # להשאיר רק StatefulSet
git checkout gitops-staging && git rm k8s/mongodb-deployment.yaml && git commit -m "gitops: drop mongodb Deployment" && git push
```

### 6) תקלות נפוצות
- ArgoCD מחזיר drift: השהה sync → תקן בקבצים → refresh → החזר automated.
- CrashLoopBackOff: בדוק לוגים (`kubectl logs`), ספריות חסרות, config/env, probes.
- rollout timeout: בדוק RS/Pods/Events; ודא image/tag קיים בדוקר; העלה `initialDelaySeconds` אם צריך.
- metrics לא נאספות: בדוק `/metrics` ו‑Prometheus job; בצע `POST /-/reload` ל‑Prometheus.

### 7) אימות סופי
```bash
kubectl -n oriyan-portfolio get deploy oriyan-portfolio-app -o jsonpath='{.status.readyReplicas}/{.status.replicas} {.spec.template.spec.containers[0].image}{"\n"}'
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:5001/health
```


