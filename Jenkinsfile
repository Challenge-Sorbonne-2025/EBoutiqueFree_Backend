pipeline {
    agent any

    environment {
        IMAGE_NAME = "shop_app:${BUILD_NUMBER}"
        PYTHONUNBUFFERED = 1
//      PATH = "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
        //docker-compose up -d
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
                    # Build avec image versionnée
                    docker-compose build
        
                    # Récupérer l’image construite
                    docker tag shop_app:${BUILD_NUMBER} shop_app:latest
                    docker run -d --name ecommerce_backend -p 9000:9000 shop_app:${BUILD_NUMBER}

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
