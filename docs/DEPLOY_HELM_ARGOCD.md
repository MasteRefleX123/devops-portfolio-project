## פריסה עם Helm ו-ArgoCD

### דרישות מוקדמות
- kubectl מחובר לקלאסטר
- helm 3+
- (אופציונלי) argocd CLI

### פריסה עם Helm (ידני)
```bash
# DEV
kubectl create ns portfolio-dev --dry-run=client -o yaml | kubectl apply -f -
helm upgrade --install portfolio-dev ./helm/portfolio \
  -n portfolio-dev \
  --create-namespace \
  --set image.tag=<IMAGE_TAG>

# STAGING
kubectl create ns portfolio-staging --dry-run=client -o yaml | kubectl apply -f -
helm upgrade --install portfolio-staging ./helm/portfolio \
  -n portfolio-staging \
  --create-namespace \
  --set image.tag=<IMAGE_TAG>

# PROD
kubectl create ns portfolio-prod --dry-run=client -o yaml | kubectl apply -f -
helm upgrade --install portfolio-prod ./helm/portfolio \
  -n portfolio-prod \
  --create-namespace \
  --set image.tag=<IMAGE_TAG>
```

הערות:
- אין להשתמש ב-`latest`. יש להציב תג תמונה מפורש (`v<build>-<sha>`).
- ניתן לשנות משאבים/Probes ב-`helm/portfolio/values.yaml` או עם `--set`.

### פריסה עם ArgoCD (Pull)
```bash
# התקנת יישומי ArgoCD (לא יצירת ArgoCD עצמו)
kubectl apply -f argocd/apps/dev.yaml
kubectl apply -f argocd/apps/staging.yaml
kubectl apply -f argocd/apps/prod.yaml

# בדיקה
kubectl -n argocd get applications

# (אופציונלי) המתנה לסנכרון דרך CLI
argocd app wait portfolio-dev --sync --health --timeout 180 || true
```

שינוי גרסת תמונה דרך GitOps:
- עדכנו את `image.tag` ב-`helm/portfolio/values.yaml` ופתחו PR. ArgoCD יבצע Sync לאחר מיזוג.

### Smoke Test אחרי פריסה
```bash
kubectl -n portfolio-dev run curl --image=curlimages/curl:8.8.0 --rm -it --restart=Never \
  -- sh -lc 'curl -sS http://portfolio-dev-svc/health'
```

### HPA ו-מדדים
- מותאם ל-HPA (autoscaling/v2). מומלץ להתקין metrics-server. בקלאסטר kind יש להפעיל:
```bash
kubectl -n kube-system patch deploy metrics-server --type=json -p='[
 {"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-insecure-tls"},
 {"op":"add","path":"/spec/template/spec/containers/0/args/-","value":"--kubelet-preferred-address-types=InternalIP,Hostname,ExternalIP"}
]'
```

### קווים מנחים
- להימנע לחלוטין מ-`latest`.
- לעבוד עם Namespaces נפרדים: `portfolio-dev`, `portfolio-staging`, `portfolio-prod`.
- ב-Prod מומלץ לחייב PR Gate וסטטוסי בדיקות ירוקים לפני מיזוג.


