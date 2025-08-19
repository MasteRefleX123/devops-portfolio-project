pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_REPO = 'oriyanrask/devops-portfolio'
        KUBECONFIG = credentials('kubeconfig')
        DOCKER_CREDENTIALS = credentials('docker-hub-credentials')
        GITHUB_TOKEN = credentials('github-token')
    }
    
    stages {
        stage('🔍 Checkout') {
            steps {
                echo '📥 Checking out source code...'
                checkout scm
                script {
                    env.GIT_COMMIT_SHORT = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()
                    env.BUILD_TAG = "${env.BUILD_NUMBER}-${env.GIT_COMMIT_SHORT}"
                }
            }
        }
        
        stage('🧪 Test') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        echo '🧪 Running unit tests...'
                        sh '''
                            python3 -m venv test-env
                            source test-env/bin/activate
                            pip install -r requirements.txt
                            pip install pytest pytest-cov
                            pytest tests/ -v --cov=app --cov-report=xml
                        '''
                    }
                    post {
                        always {
                            publishCoverageResults([
                                [
                                    parser: 'COBERTURA',
                                    pattern: 'coverage.xml'
                                ]
                            ])
                        }
                    }
                }
                
                stage('Security Scan') {
                    steps {
                        echo '🔒 Running security scan...'
                        sh '''
                            pip install safety bandit
                            safety check -r requirements.txt
                            bandit -r app/ -f json -o bandit-report.json
                        '''
                    }
                }
                
                stage('Code Quality') {
                    steps {
                        echo '📊 Running code quality checks...'
                        sh '''
                            pip install flake8 black isort
                            flake8 app/ --max-line-length=88
                            black --check app/
                            isort --check-only app/
                        '''
                    }
                }
            }
        }
        
        stage('🐳 Build Docker Image') {
            steps {
                echo '🐳 Building Docker image...'
                script {
                    def image = docker.build("${DOCKER_REPO}:${BUILD_TAG}")
                    env.DOCKER_IMAGE = "${DOCKER_REPO}:${BUILD_TAG}"
                }
            }
        }
        
        stage('🔍 Container Security Scan') {
            steps {
                echo '🔍 Scanning Docker image for vulnerabilities...'
                sh '''
                    docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
                        aquasec/trivy image --format json --output trivy-report.json \
                        ${DOCKER_IMAGE}
                '''
            }
        }
        
        stage('📤 Push to Registry') {
            when {
                anyOf {
                    branch 'main'
                    branch 'develop'
                }
            }
            steps {
                echo '📤 Pushing Docker image to registry...'
                script {
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-credentials') {
                        docker.image("${DOCKER_IMAGE}").push()
                        docker.image("${DOCKER_IMAGE}").push('latest')
                    }
                }
            }
        }
        
        stage('🚀 Deploy to Staging') {
            when {
                branch 'develop'
            }
            steps {
                echo '🚀 Deploying to staging environment...'
                sh '''
                    helm upgrade --install portfolio-staging ./helm/portfolio \
                        --namespace oriyan-portfolio-staging \
                        --create-namespace \
                        --set image.tag=${BUILD_TAG} \
                        --set environment=staging \
                        --wait --timeout=10m
                '''
            }
        }
        
        stage('🧪 Integration Tests') {
            when {
                branch 'develop'
            }
            steps {
                echo '🧪 Running integration tests...'
                sh '''
                    sleep 30  # Wait for deployment to be ready
                    python3 -m pytest tests/integration/ -v \
                        --base-url=http://portfolio-staging.local
                '''
            }
        }
        
        stage('🎯 Deploy to Production') {
            when {
                branch 'main'
            }
            steps {
                echo '🎯 Deploying to production environment...'
                input message: 'Deploy to production?', ok: 'Deploy',
                      submitterParameter: 'DEPLOYER'
                sh '''
                    helm upgrade --install portfolio-prod ./helm/portfolio \
                        --namespace oriyan-portfolio \
                        --create-namespace \
                        --set image.tag=${BUILD_TAG} \
                        --set environment=production \
                        --set replicaCount=3 \
                        --wait --timeout=15m
                '''
            }
        }
        
        stage('📊 Performance Tests') {
            when {
                branch 'main'
            }
            steps {
                echo '📊 Running performance tests...'
                sh '''
                    docker run --rm -v $(pwd):/workspace \
                        loadimpact/k6 run /workspace/tests/performance/load-test.js
                '''
            }
        }
    }
    
    post {
        always {
            echo '🧹 Cleaning up...'
            sh '''
                docker system prune -f
                rm -rf test-env/
            '''
        }
        
        success {
            echo '✅ Pipeline completed successfully!'
            slackSend(
                channel: '#devops-alerts',
                color: 'good',
                message: "✅ *Oriyan's Portfolio* - Build #${BUILD_NUMBER} succeeded!\n" +
                        "Branch: ${BRANCH_NAME}\n" +
                        "Commit: ${GIT_COMMIT_SHORT}\n" +
                        "Deployer: ${env.DEPLOYER ?: 'Auto'}"
            )
        }
        
        failure {
            echo '❌ Pipeline failed!'
            slackSend(
                channel: '#devops-alerts',
                color: 'danger',
                message: "❌ *Oriyan's Portfolio* - Build #${BUILD_NUMBER} failed!\n" +
                        "Branch: ${BRANCH_NAME}\n" +
                        "Commit: ${GIT_COMMIT_SHORT}\n" +
                        "Check: ${BUILD_URL}"
            )
        }
        
        unstable {
            echo '⚠️ Pipeline completed with warnings!'
        }
    }
}
