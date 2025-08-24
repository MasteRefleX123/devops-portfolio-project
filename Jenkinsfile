pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_IMAGE = 'mastereflex123/portfolio'
        DOCKER_CREDENTIALS = 'docker-hub'
        GITHUB_CREDENTIALS = 'github-token'
        KUBECONFIG_CREDENTIALS = 'kubeconfig'
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
                    env.DOCKER_TAG = "v${env.BUILD_NUMBER}"
                    env.EFFECTIVE_BRANCH = sh(script: 'git rev-parse --abbrev-ref HEAD || echo feature/day2-docker-kubernetes', returnStdout: true).trim()
                }
            }
        }
        
        stage('Setup Python') {
            steps {
                sh '''
                    set -e
                    apt-get update
                    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-venv python3-pip
                    python3 --version
                    pip3 --version || true
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
                sh "docker tag ${DOCKER_IMAGE}:${env.DOCKER_TAG} ${DOCKER_IMAGE}:latest"
            }
        }
        
        stage('Push to Registry') {
            when {
                expression { return env.EFFECTIVE_BRANCH == 'main' || env.EFFECTIVE_BRANCH == 'feature/day2-docker-kubernetes' }
            }
            steps {
                echo 'Pushing to Docker Hub...'
                withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS, usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh "echo $PASS | docker login -u $USER --password-stdin"
                    sh "docker push ${DOCKER_IMAGE}:${env.DOCKER_TAG}"
                    sh "docker push ${DOCKER_IMAGE}:latest"
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            when {
                expression { return env.EFFECTIVE_BRANCH == 'main' || env.EFFECTIVE_BRANCH == 'feature/day2-docker-kubernetes' }
            }
            steps {
                echo 'Deploying to Kubernetes...'
                withCredentials([file(credentialsId: KUBECONFIG_CREDENTIALS, variable: 'KUBECONFIG')]) {
                    sh """
                        kubectl set image deployment/oriyan-portfolio-app \
                            portfolio-app=${DOCKER_IMAGE}:${env.DOCKER_TAG} \
                            -n oriyan-portfolio --record
                        kubectl rollout status deployment/oriyan-portfolio-app -n oriyan-portfolio
                    """
                }
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
