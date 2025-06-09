pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        IMAGE_NAME = "shop_app:${BUILD_NUMBER}"
        PYTHONUNBUFFERED = 1
        PATH = "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
    }

    stages {

        stage('📥 Checkout code') {
            steps {
                echo "🔄 Cloning the repository..."
                checkout scm
            }
        }
        stage('📎 Copier le .env local dans le workspace') {
            steps {
                echo "📄 Copie du fichier .env local dans le workspace Jenkins..."
                sh '''
                    set -e
                    cp "/Users/etiennesene/Documents/EBoutiqueFree_Backend/.env" .env
                '''
            }
        }
        stage('🐍 Setup Python & Install Dependencies') {
            steps {
                echo "⚙️ Creating virtualenv & installing requirements..."
                sh '''
                    python3.12 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip list
                '''
            }
        }

        stage('✅ Run Django tests') {
            steps {
                echo "🚀 Running tests..."
                sh '''
                    . ${VENV_DIR}/bin/activate
                    export PYTHONPATH=$PWD
                    python3.12 EBoutique_API/manage.py test
                '''
            }
        }

        stage('🐳 Docker build') {
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
            echo '🧼 Cleaning up (if needed)...'
        }
        success {
            echo '🎉 CI pipeline completed successfully!'
        }
        failure {
            echo '❌ CI pipeline failed!'
        }
    }
}
