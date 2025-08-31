## Operations Quick Reference

### Start/Stop Local Stack
```bash
cd /mnt/c/Users/momir/devops-portfolio-project
./start-all.sh
./stop-all.sh
```

### Jenkins
- URL: http://localhost:8080
- Initial admin password (if reset): stored in repo summary / memory
- Job: `devops-portfolio` on branch `feature/day2-docker-kubernetes`

### Trigger Build Manually (with CSRF)
```bash
crumb=$(curl -s -u "$J_USER:$J_TOKEN" http://localhost:8080/crumbIssuer/api/json | jq -r '.crumb')
curl -X POST -u "$J_USER:$J_TOKEN" -H "Jenkins-Crumb: $crumb" \
  http://localhost:8080/job/devops-portfolio/build
```

### Kubernetes Access
```bash
kubectl -n oriyan-portfolio get deploy,sts,svc
kubectl -n oriyan-portfolio rollout status deploy/oriyan-portfolio-app --timeout=180s
kubectl -n oriyan-portfolio logs deploy/oriyan-portfolio-app --tail=200
```

### Port-Forward App
```bash
pkill -f "port-forward.*5001:80" 2>/dev/null || true
kubectl -n oriyan-portfolio port-forward svc/portfolio-service 5001:80
```

### Smoke Tests
```bash
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:5001/health
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"a@b.c","message":"hi"}' \
  -o /dev/null -w "%{http_code}\n" http://localhost:5001/api/contact
```

### Prometheus & Grafana
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (user: `oriyan`, pass: `devops2024`)
- Dashboard: `portfolio-overview`

### ArgoCD
```bash
kubectl -n argocd get applications
kubectl -n argocd get application portfolio-app -o yaml | less
kubectl -n argocd patch application portfolio-app --type=merge -p='{"spec":{"syncPolicy":{"automated":{"prune":true,"selfHeal":true}}}}'
```

### Rollout Troubleshooting
See: `docs/Runbook-Rollout.md`


