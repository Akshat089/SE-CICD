pipeline {
    agent any
    
    environment {
        DOCKERHUB_USERNAME = 'akshat09128'
        REPO_NAME = 'cicd'                    // just the repo name
        IMAGE_TAG = "${BUILD_NUMBER}"

        GITHUB_CREDS = credentials('githubcreds')
        DOCKERHUB_CREDS = credentials('dockerhubcreds')

        PYTHON = 'C:\\Users\\Akshat\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'
    }
    
    stages {

        stage('Checkout') {
            steps {
                echo "Pulling code from GitHub..."
                git branch: 'main',
                    url: 'https://github.com/Akshat089/SE-CICD.git',
                    credentialsId: 'githubcreds'
            }
        }

        stage('Build - Install Dependencies') {
            steps {
                echo "Setting up Python virtual environment..."
                bat """
                    "%PYTHON%" -m venv venv
                    venv\\Scripts\\python.exe -m pip install --upgrade pip
                    venv\\Scripts\\python.exe -m pip install -r requirements.txt
                    venv\\Scripts\\python.exe -m pip install pytest
                """
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running Python tests..."
                bat "venv\\Scripts\\python.exe -m pytest tests\\test_todo.py -v"
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                bat "docker build -t ${DOCKERHUB_USERNAME}/${REPO_NAME}:${IMAGE_TAG} ."
                bat "docker tag ${DOCKERHUB_USERNAME}/${REPO_NAME}:${IMAGE_TAG} ${DOCKERHUB_USERNAME}/${REPO_NAME}:latest"
            }
        }

        stage('Push to Docker Hub') {
            steps {
                echo "Pushing Docker image..."
                bat "docker login -u %DOCKERHUB_CREDS_USR% -p %DOCKERHUB_CREDS_PSW%"
                bat "docker push ${DOCKERHUB_USERNAME}/${REPO_NAME}:${IMAGE_TAG}"
                bat "docker push ${DOCKERHUB_USERNAME}/${REPO_NAME}:latest"
                bat "docker logout"
            }
        }

        stage('Verify Docker Image') {
            steps {
                bat "docker images | findstr ${REPO_NAME}"
            }
        }
    }

    post {
        success { echo "✓ Pipeline completed successfully!" }
        failure { echo "✗ Pipeline failed!" }
        always {
            script { deleteDir() }
        }
    }
}
