pipeline {
    agent any

    stages {

        stage('Start Pipeline') {
            steps {
                echo 'MLOps Pipeline Started'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip install -r requirements.txt || true'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t heart-mlops .'
            }
        }

        stage('Run Container') {
            steps {
                sh 'docker run -d -p 5000:5000 heart-mlops || true'
            }
        }
    }
}
