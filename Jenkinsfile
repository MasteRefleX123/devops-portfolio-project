pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_IMAGE = 'mastereflex123/portfolio'
        DOCKER_CREDENTIALS = 'docker-hub'
        GITHUB_CREDENTIALS = 'github-credentials'
        KUBECONFIG_CREDENTIALS = 'kubeconfig'
        DOCKER_BUILDKIT = '1'
        COMPOSE_DOCKER_CLI_BUILD = '1'
    }

    options {
        disableConcurrentBuilds()
        timestamps()
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
                script {
                    env.GIT_COMMIT_SHORT = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    env.DOCKER_TAG = "v${env.BUILD_NUMBER}-${env.GIT_COMMIT_SHORT}"
                    env.EFFECTIVE_BRANCH = sh(script: 'git rev-parse --abbrev-ref HEAD || echo feature/day2-docker-kubernetes', returnStdout: true).trim()
                }
            }
        }
        
        stage('Setup Tools') {
            steps {
                sh '''
                    set -e
                    apt-get update
                    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-venv python3-pip curl ca-certificates gnupg docker.io

                    # Install kubectl (latest stable)
                    KVERSION=$(curl -L -s https://dl.k8s.io/release/stable.txt)
                    curl -LO "https://dl.k8s.io/release/${KVERSION}/bin/linux/amd64/kubectl"
                    install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
                    rm -f kubectl

                    python3 --version
                    pip3 --version || true
                    docker --version || true
                    kubectl version --client --output=yaml || true
                '''
            }
        }
        
        stage('Test') {
            steps {
                echo 'Running tests...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                    pip install pytest pytest-cov
                    pytest tests/ -v --cov=oriyan_portfolio
                '''
            }
        }
        
        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                sh "docker build -t ${DOCKER_IMAGE}:${env.DOCKER_TAG} ."
            }
        }
        
        stage('Push to Registry') {
            steps {
                echo 'Pushing to Docker Hub...'
                script {
                    def usedCreds = false
                    try {
                        withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS, usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                            sh '''
                                set -eu
                                : "${DOCKER_CONFIG:=$HOME/.docker}"
                                mkdir -p "$DOCKER_CONFIG"
                                echo "$PASS" | docker login -u "$USER" --password-stdin
                                docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                            '''
                            usedCreds = true
                        }
                    } catch (err) {
                        echo "Credentials id '${DOCKER_CREDENTIALS}' unavailable; falling back to env."
                    }
                    if (!usedCreds) {
                        sh '''
                            set -eu
                            if [ -z "${DOCKERHUB_USER:-}" ] || [ -z "${DOCKERHUB_PASS:-}" ]; then
                              echo "Missing Docker Hub env credentials" >&2; exit 1
                            fi
                            : "${DOCKER_CONFIG:=$HOME/.docker}"
                            mkdir -p "$DOCKER_CONFIG"
                            echo "$DOCKERHUB_PASS" | docker login -u "$DOCKERHUB_USER" --password-stdin
                            docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                        '''
                    }
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                echo 'Deploying to Kubernetes...'
                withCredentials([file(credentialsId: KUBECONFIG_CREDENTIALS, variable: 'KUBECONFIG')]) {
                    sh '''
                        set -e
                        # Prepare kubeconfig: prefer env KUBECONFIG_BASE64 if provided, otherwise use Jenkins file credential
                        KCFG_TMP=$(mktemp)
                        if [ -n "${KUBECONFIG_BASE64:-}" ]; then
                          echo "$KUBECONFIG_BASE64" | base64 -d > "$KCFG_TMP"
                        else
                          cp "$KUBECONFIG" "$KCFG_TMP"
                        fi
                        export KUBECONFIG="$KCFG_TMP"

                        # Ensure kubectl talks to kind control-plane over Docker network DNS
                        CURRENT_CTX=$(kubectl config current-context 2>/dev/null || true)
                        if [ -n "$CURRENT_CTX" ]; then
                          CTX_CLUSTER=$(kubectl config view --kubeconfig "$KCFG_TMP" -o jsonpath="{.contexts[?(@.name=='$CURRENT_CTX')].context.cluster}")
                          if [ -n "$CTX_CLUSTER" ]; then
                            kubectl config set-cluster "$CTX_CLUSTER" --kubeconfig "$KCFG_TMP" --server=https://devops-portfolio-control-plane:6443 --insecure-skip-tls-verify=true
                          fi
                        fi
                        # Fallback: update all clusters in kubeconfig (robust in multi-cluster kubeconfigs)
                        for c in $(kubectl config view --kubeconfig "$KCFG_TMP" -o jsonpath='{.clusters[*].name}'); do
                          kubectl config set-cluster "$c" --kubeconfig "$KCFG_TMP" --server=https://devops-portfolio-control-plane:6443 --insecure-skip-tls-verify=true || true
                        done

                        # Attempt rollout
                        kubectl -n oriyan-portfolio get deploy oriyan-portfolio-app || true
                        kubectl set image deployment/oriyan-portfolio-app \
                          portfolio-app=${DOCKER_IMAGE}:${DOCKER_TAG} \
                          -n oriyan-portfolio --record
                        kubectl rollout status deployment/oriyan-portfolio-app -n oriyan-portfolio --timeout=180s
                    '''
                }
            }
        }

        stage('Post-deploy Smoke Test') {
            steps {
                echo 'Running smoke test on /health via in-cluster service...'
                withCredentials([file(credentialsId: KUBECONFIG_CREDENTIALS, variable: 'KUBECONFIG')]) {
                    sh '''
                        set -e
                        KCFG_TMP=$(mktemp)
                        if [ -n "${KUBECONFIG_BASE64:-}" ]; then
                          echo "$KUBECONFIG_BASE64" | base64 -d > "$KCFG_TMP"
                        else
                          cp "$KUBECONFIG" "$KCFG_TMP"
                        fi
                        export KUBECONFIG="$KCFG_TMP"
                        # Align server with kind DNS inside docker network
                        for c in $(kubectl config view --kubeconfig "$KCFG_TMP" -o jsonpath='{.clusters[*].name}'); do
                          kubectl config set-cluster "$c" --kubeconfig "$KCFG_TMP" --server=https://devops-portfolio-control-plane:6443 --insecure-skip-tls-verify=true || true
                        done

                        # Use ephemeral curl pod to query the service internally
                        kubectl -n oriyan-portfolio delete pod smoke-curl --ignore-not-found=true
                        kubectl -n oriyan-portfolio run smoke-curl --image=curlimages/curl:8.8.0 --restart=Never --command -- sh -c "curl -sS http://portfolio-service/health | tee /tmp/out"
                        # Wait for completion
                        kubectl -n oriyan-portfolio wait --for=condition=PodCompleted pod/smoke-curl --timeout=60s
                        # Fetch logs and validate
                        OUT=$(kubectl -n oriyan-portfolio logs pod/smoke-curl || true)
                        echo "$OUT"
                        echo "$OUT" | grep -q 'healthy' || { echo 'Smoke test failed: /health not healthy'; exit 1; }
                        kubectl -n oriyan-portfolio delete pod smoke-curl --ignore-not-found=true
                    '''
                }
            }
        }

        stage('ArgoCD Gates (optional)') {
            when {
                expression { return env.ARGOCD_ENABLED == 'true' }
            }
            steps {
                echo 'Validating ArgoCD Application health and sync...'
                sh '''
                    set -e
                    if ! command -v argocd >/dev/null 2>&1; then
                      echo "argocd CLI not installed; skipping gates"; exit 0
                    fi
                    APP_NAME=${ARGOCD_APP_NAME:-portfolio-dev}
                    # If app isn't reachable, skip without failing the pipeline
                    if ! argocd app get "$APP_NAME" >/dev/null 2>&1; then
                      echo "ArgoCD app $APP_NAME not found/reachable; skipping"; exit 0
                    fi
                    argocd app wait "$APP_NAME" --sync --health --timeout 180 || {
                      echo "ArgoCD gate failed for $APP_NAME"; exit 1;
                    }
                '''
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
