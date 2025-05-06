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
                echo "🚀 Running tests..."
                sh '''
                    . ${VENV_DIR}/bin/activate
                    export PYTHONPATH=$PWD
                    python3 EBoutique_API/manage.py test
                '''
            }
        }

stage('🐳 Docker Compose Build & Start') {
    steps {
        echo "📦 Building and starting containers using Docker Compose..."
        sh '''
            docker-compose up --build -d
        '''
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