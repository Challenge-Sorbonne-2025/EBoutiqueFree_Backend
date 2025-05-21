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

        stage('🔑 Générer .env temporairement') {
            steps {
                echo "✍️ Récupération des variables d’environnement depuis Jenkins Credentials..."
                withCredentials([string(credentialsId: '.env', variable: 'ENV_CONTENT')]) {
                    writeFile file: '.env', text: "${ENV_CONTENT}"
                }
            }
        }

        stage('🐍 Setup Python & Install Requirements') {
            steps {
                echo "⚙️ Création de l’environnement virtuel & installation des dépendances..."
                sh '''
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('✅ Run Django tests') {
            steps {
                echo "🚀 Lancement des tests Django..."
                sh '''
                    . ${VENV_DIR}/bin/activate
                    export PYTHONPATH=$PWD
                    export $(cat .env | xargs)
                    python3 EBoutique_API/manage.py test
                '''
            }
        }

        stage('🐳 Build Docker image') {
            environment {
                PATH = "/opt/homebrew/bin:$PATH" // si Docker est installé via Homebrew
            }
            steps {
                echo "📦 Création de l’image Docker : ${IMAGE_NAME}"
                sh '''
                    docker build -t ${IMAGE_NAME} .
                    docker tag ${IMAGE_NAME} shop_app:latest
                '''
            }
        }

        stage('🚀 Run Docker container with .env') {
            steps {
                echo "🚀 Démarrage du conteneur avec les variables d’environnement..."
                sh '''
                    docker rm -f shop_container || true
                    docker run --env-file .env -d --name shop_container -p 8000:8000 ${IMAGE_NAME}
                '''
            }
        }
    }

    post {
        always {
            echo '🧹 Nettoyage des fichiers temporaires...'
            sh 'rm -f .env'
        }
        success {
            echo '✅ Pipeline terminé avec succès.'
        }
        failure {
            echo '❌ Échec du pipeline.'
        }
    }
}
