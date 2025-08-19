pipeline {
    agent any
    
    environment {
        DOCKER_REGISTRY = 'docker.io'
        DOCKER_IMAGE = 'mastereflex123/portfolio'
        DOCKER_CREDENTIALS = 'docker-hub'
        GITHUB_CREDENTIALS = 'github-token'
        KUBECONFIG_CREDENTIALS = 'kubeconfig'
    }
    
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
                script {
                    env.GIT_COMMIT_SHORT = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    env.DOCKER_TAG = "v${env.BUILD_NUMBER}"
                }
            }
        }
        
        stage('Test') {
            steps {
                echo 'Running tests...'
                sh '''
                    python3 -m venv venv
                    source venv/bin/activate
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
            when { branch 'main' }
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
            when { branch 'main' }
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
