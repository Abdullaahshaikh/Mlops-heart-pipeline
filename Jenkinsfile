pipeline {
    agent any

    environment {
        ELECTRICITY_MAPS_API_KEY = credentials('electricity_maps_api_key')
    }

    stages {

        stage('Clone') {
            steps {
                echo 'Repository cloned successfully'
            }
        }

        stage('Carbon Decision Gate') {
            steps {
                echo 'Checking grid carbon intensity...'
                sh 'python3 carbon_decision.py'
            }
        }

        stage('Train Model') {
            steps {
                echo 'Training clean ML model...'
                sh 'python3 train.py'
            }
        }

        stage('Drift Detection & Auto-Retraining') {
            steps {
                echo 'Checking data drift...'
                sh 'python3 -m pipeline.auto_pipeline'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t green-mlops:latest .'
            }
        }

        stage('Run Container') {
            steps {
                echo 'Running Docker container...'
                sh 'docker rm -f green-mlops-container || true'
                sh 'docker run -d --name green-mlops-container -p 5000:5000 green-mlops:latest'
            }
        }
    }
}
