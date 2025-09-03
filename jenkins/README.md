# Jenkins Helm values

This folder contains simple Helm values for deploying Jenkins via the official chart.

- Chart: `https://charts.jenkins.io` (jenkins)
- Namespace: `jenkins`
- Values file: `jenkins/values.yaml`

To install with Helm directly:

```bash
helm repo add jenkins https://charts.jenkins.io
helm repo update
helm upgrade --install jenkins jenkins/jenkins -n jenkins -f jenkins/values.yaml --create-namespace
```

If using ArgoCD, point the Application to this `values.yaml`.


