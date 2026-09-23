pipeline {
    agent any

    stages {

        stage('Clone') {
            steps {
                echo 'Repository cloned successfully'
            }
        }

        stage('Carbon Decision') {
            steps {
                echo 'Checking carbon intensity...'
                bat 'python carbon_decision.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Docker build stage'
            }
        }

        stage('Run Container') {
            steps {
                echo 'Container running'
            }
        }
    }
}
