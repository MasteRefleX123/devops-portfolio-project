## Architecture Overview

This project is a small, production‑like portfolio system built around a Python/Flask backend, packaged into a Docker image, deployed to a local Kubernetes (kind) cluster, and operated via CI/CD (Jenkins) with optional GitOps (ArgoCD). Monitoring is provided by Prometheus and Grafana.

### Components
- **Application (Flask)**: Exposes HTTP APIs (e.g., `/health`, `/api/contact`) and Prometheus metrics at `/metrics`.
- **Docker**: Multi‑stage build creates a minimal runtime image published to Docker Hub `mastereflex123/portfolio` with a versioned tag.
- **Kubernetes (kind)**: Runs the app in namespace `oriyan-portfolio` with a `Deployment` and `Service`. MongoDB runs as a StatefulSet with a `Service`.
- **CI/CD (Jenkins)**: Jenkins pipeline builds, tests, pushes the image, deploys to the cluster, runs smoke tests, and optionally validates ArgoCD health.
- **GitOps (ArgoCD)**: ArgoCD watches the Git repository/branch (`gitops-staging`) and keeps Kubernetes resources synced.
- **Monitoring**: Prometheus scrapes metrics; Grafana provides dashboards and alerting via rules in `monitoring/rules/`.
- **Webhook/Ingress (ngrok)**: ngrok provides a public URL for GitHub webhooks to trigger Jenkins builds.

### CI/CD Flow
1. Developer pushes to the feature branch.
2. Jenkins pipeline (Jenkinsfile):
   - Checkout and compute `${DOCKER_TAG}` as `v${BUILD_NUMBER}-${GIT_COMMIT_SHORT}`.
   - Install tools if missing (python, docker, kubectl).
   - Run unit tests (pytest).
   - Build image and guard against using `:latest`.
   - Push image to Docker Hub (using Jenkins credentials).
   - Deploy to Kubernetes: `kubectl set image` on `deployment/oriyan-portfolio-app` with the new tag and wait for rollout.
   - Smoke test inside cluster using a temporary curl pod.
   - Optional ArgoCD gates: `argocd app wait` if enabled.

### Runtime Topology (Kubernetes)
- Namespace: `oriyan-portfolio`.
- Workloads:
  - `Deployment/oriyan-portfolio-app` (replicas >= 1) → `Service/portfolio-service` (ClusterIP).
  - `StatefulSet/mongodb-stateful` → `Service/mongodb-service`.
- Networking:
  - Local dev access via `kubectl port-forward svc/portfolio-service 5001:80`.
  - Jenkins reachable at `http://localhost:8080`.
- Policies and resources (examples): HPA in `k8s/hpa.yaml`, NetworkPolicy in `k8s/network-policy.yaml`.

### Monitoring & Alerting
- Prometheus scrapes the Flask app at `/metrics` and evaluates alert rules from `monitoring/rules/alerts.yml`.
- Grafana provides the `portfolio-overview` dashboard from `monitoring/grafana/dashboards/`.
- Example alerts: missing metrics, high HTTP 5xx rate, high p90 latency.

### GitOps
- ArgoCD Application (e.g., `portfolio-app`) points to this repo and `gitops-staging` branch, path `k8s/`.
- Automated sync and self‑heal keep the cluster aligned to Git.
- Image tags are pinned (no `:latest`). Update desired image by PR to the GitOps branch.

### Operational Guardrails
- Jenkinsfile rejects `:latest` tags at build and deploy.
- Runbook for rollout issues: see `docs/Runbook-Rollout.md`.






