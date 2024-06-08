pipeline {
    agent any
    triggers {
        pollSCM '* * * * *'
    }
    stages {
        stage('Workspace Cleanup') {
            steps {
                cleanWs()
            }
        }
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Set up Environment') {
            steps {
                script {
                    withCredentials([file(credentialsId: 'hyfish-model-env', variable: 'ENV_FILE')]) {
                        sh 'cp $ENV_FILE .env'
                    }
                    
                    withCredentials([file(credentialsId: 'hyfish-storage-key', variable: 'SERVICE_ACCOUNT_FILE')]) {
                        sh 'cp $SERVICE_ACCOUNT_FILE service-account.json'
                    }
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    sh 'docker stop hyfish-model-container || true'
                    sh 'docker system prune -af'
                    sh 'docker build -t hyfish-model .'
                }
            }
        }
        stage('Run Docker Container') {
            steps {
                script {
                    sh 'docker run -d -p 5000:5000 --name hyfish-model-container hyfish-model'
                }
            }
        }
    }
     post {
        success {
            script {
                def commitMessage = sh(script: 'git log -1 --pretty=%B', returnStdout: true).trim()

                withCredentials([
                    string(credentialsId: 'discord-webhook', variable: 'DISCORD_WEBHOOK_URL'),
                ]) {
                    discordSend description: "Last Commit:\n\"${commitMessage}\"", 
                                footer: 'Jenkins CI/CD', 
                                link: env.BUILD_URL, 
                                result: currentBuild.currentResult, 
                                title: 'Model Deployment Successful', 
                                webhookURL: DISCORD_WEBHOOK_URL
                }
            }
        }
        failure {
            script {
                withCredentials([string(credentialsId: 'discord-webhook', variable: 'DISCORD_WEBHOOK_URL')]) {
                    discordSend description: 'Deployment Failed', 
                                footer: 'Jenkins CI/CD', 
                                link: env.BUILD_URL, 
                                result: currentBuild.currentResult, 
                                title: 'Model Deployment Failed', 
                                webhookURL: DISCORD_WEBHOOK_URL
                }
            }
        }
    }
}
