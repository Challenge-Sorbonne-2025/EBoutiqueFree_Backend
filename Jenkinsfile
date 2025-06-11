pipeline {
    agent any

    environment {
        IMAGE_NAME = "shop_app:${BUILD_NUMBER}"
        PYTHONUNBUFFERED = 1
//      PATH = "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
    }

    stages {

        stage('📥 Checkout code') {
            steps {
                echo "🔄 Cloning the repository..."
                checkout scm
            }
        }

        stage('📎 Injecter le .env sécurisé') {
            steps {
                echo "🔐 Injection du fichier .env depuis Jenkins Credentials..."
                withCredentials([file(credentialsId: 'EBOUTIQUE_BACKEND_ENV', variable: 'DOTENV_FILE')]) {
                    sh '''
                        cp $DOTENV_FILE .env
                    '''
                }
            }
        }

        stage('🐳 Build Docker Compose') {
            steps {
                echo "🐳 Build avec docker-compose..."
                sh '''
                    docker-compose down || true         
                    echo "BUILD_NUMBER=${BUILD_NUMBER}" > .env
                    docker-compose build
                    docker-compose up -d
                '''
            }
        }

    }

    post {
        always {
            echo '🧹 Nettoyage du workspace et containers...'
            sh 'docker-compose down || true'
            cleanWs()
        }
    }
}
