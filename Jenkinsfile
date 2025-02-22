pipeline {
    agent any

    environment {
        DOCKER_IMAGE="techsavvydivyansh/react-app-cicd"
        DOCKER_TAG="latest"
    }

    stages {
        stage('hello world') {
            steps {
                sh ''' 
                    echo hello world server has started
                '''
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', usernameVariable: 'DOCKER_HUB_USER', passwordVariable: 'DOCKER_HUB_PASS')]) {
                    sh 'echo $DOCKER_HUB_PASS | docker login -u $DOCKER_HUB_USER --password-stdin'
                }
            }  
        }

        stage('build docker image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE:$DOCKER_TAG .'
            }
        } 

        stage('push image to docker hub') {
            steps {
                sh 'docker push $DOCKER_IMAGE:latest'
            }
        }

        stage('Terraform Init & Apply') {
            steps {
                withEnv(["AWS_PROFILE=default"]) {
                    sh '''
                        cd terraform
                        terraform init
                        terraform apply -auto-approve
                    '''
                }
            }
        }  // ✅ Properly closed the 'Terraform Init & Apply' stage
    }  // ✅ Properly closed the 'stages' block

    post {
        success {
            echo 'Deployment Successful!'
        }
        failure {
            echo 'Deployment Failed!'
        }
    }
}
