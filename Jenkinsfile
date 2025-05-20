pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        IMAGE_NAME = "shop_app:${BUILD_NUMBER}"
        PYTHONUNBUFFERED = 1
        ENV_CONTENT = credentials('.env') // 💡 Chargement du .env depuis Jenkins
    }

    stages {

        stage('📥 Checkout code') {
            steps {
                echo "🔄 Cloning the repository..."
                checkout scm
            }
        }

        stage('🔑 Write .env') {
            steps {
                echo "✍️ Writing environment variables to .env file..."
                writeFile file: '.env', text: "${ENV_CONTENT}"
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
                    export $(cat .env | xargs)  # 💡 Charge les variables d'environnement
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
            echo '🧼 Cleaning up (if needed)...'
            sh 'rm -f .env'  // 🔐 Supprime le .env après le build
        }
        success {
            echo '🎉 CI pipeline completed successfully!'
        }
        failure {
            echo '❌ CI pipeline failed!'
        }
    }
}
