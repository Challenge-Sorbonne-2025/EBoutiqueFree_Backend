pipeline {
    agent any

    environment {
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
                    docker-compose rm -f || true
                    docker rm -f ecommerce_backend || true   # <-- LA CLE !!!
                    docker-compose build
                    docker tag shop_app:${BUILD_NUMBER} shop_app:latest
                    docker-compose --env-file .env up --force-recreate -d
                    

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
