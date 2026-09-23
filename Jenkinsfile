Ab Jenkinsfile ko actual gate ke liye update karte hain.

Current Jenkinsfile ko pura replace karo:

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
Important

Ab carbon_decision.py mein:

raise SystemExit(1)

hai, isliye high carbon intensity par Jenkins pipeline automatically FAIL/STOP hogi.

Save → Git commit → push:

git add Jenkinsfile carbon_decision.py
git commit -m "Add carbon-aware Jenkins decision gate"
git push origin main

Phir Jenkins mein Build Now.

Build ka result bhejna.

raise SystemExit(1)

ye kaha

raise SystemExit(1) carbon_decision.py mein already hai — jo code humne abhi add kiya tha.

Ye isi block mein hai:

if carbon_intensity > 500:
    print("DECISION: High grid carbon intensity - training delayed.")
    raise SystemExit(1)

Jenkinsfile mein ye line nahi dalni.
Jenkinsfile mein sirf sh 'python3 carbon_decision.py' rahega.

Ab next: Jenkinsfile save → Git commit → push.

pura code plz

Bilkul. Jenkinsfile ka pura code ye hai:

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

Abhi sirf Jenkinsfile replace karke save karo.
Uske baad mujhe done bolo.