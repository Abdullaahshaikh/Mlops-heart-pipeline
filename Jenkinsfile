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

        stage('Build Docker Image') {
            steps {
                echo 'Docker build stage - proceeding after carbon approval'
            }
        }

        stage('Run Container') {
            steps {
                echo 'Container stage - proceeding after carbon approval'
            }
        }
    }
}