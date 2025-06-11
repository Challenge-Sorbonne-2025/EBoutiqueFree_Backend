pipeline {
    agent any

    environment {
        COMPOSE_FILE = 'docker-compose.yml'
//        PATH = "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
    }

    stages {

        stage('📥 Checkout code') {
            steps {
                echo "🔄 Cloning the repository..."
                checkout scm
            }
        }

        stage('🐳 Build & Start with Docker Compose') {
            steps {
                echo "📦 Build and up containers"
                sh '''
                    docker-compose down
                    docker-compose build
                    docker-compose up -d
                '''
            }
        }

        stage('✅ Health check') {
            steps {
                echo "✅ Checking if container is running"
                sh '''
                    docker ps
                '''
            }
        }
    }

    post {
        always {
            echo '🧹 Nettoyage...'
            sh 'docker-compose down || true'
            cleanWs()
        }
        success {
            echo '🎉 Pipeline terminé avec succès!'
        }
        failure {
            echo '❌ Échec du pipeline.'
        }
    }
}
