pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        IMAGE_NAME = "shop_app:${BUILD_NUMBER}"
        PYTHONUNBUFFERED = 1
    }

    stages {
        stage('📥 Checkout code') {
            steps {
                echo "🔄 Cloning the repository..."
                checkout scm
            }
        }

        stage('🔑 Écriture du .env depuis les credentials Jenkins') {
            steps {
                echo "✍️ Écriture du fichier .env depuis Jenkins credentials..."
                withCredentials([string(credentialsId: '.env', variable: 'ENV_CONTENT')]) {
                    writeFile file: '.env', text: "${ENV_CONTENT}"
                }
            }
        }

        stage('🐍 Setup Python & Install Dependencies') {
            steps {
                echo "⚙️ Creating virtualenv & installing requirements..."
                sh '''
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip list
                '''
            }
        }

        stage('✅ Run Django tests') {
            steps {
                echo "🚀 Running Django tests..."
                sh '''
                    . ${VENV_DIR}/bin/activate
                    export PYTHONPATH=$PWD
                    export $(cat .env | xargs)
                    python3 EBoutique_API/manage.py test
                '''
            }
        }

        stage('🐳 Docker build') {
            environment {
                PATH = "/opt/homebrew/bin:$PATH"
            }
            steps {
                echo "📦 Building Docker image ${IMAGE_NAME}..."
                sh '''
                    docker build -t ${IMAGE_NAME} .
                    docker tag ${IMAGE_NAME} shop_app:latest
                '''
            }
        }
    }

    post {
        always {
            echo '🧼 Suppression du fichier .env...'
            sh 'rm -f .env'
        }
        success {
            echo '✅ Pipeline terminé avec succès.'
        }
        failure {
            echo '❌ Pipeline échoué.'
        }
    }
}
