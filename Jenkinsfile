pipeline {
    agent any

    environment{
        DOCKER_IMAGE="techsavvydivyansh/react-app-cicd"
    }

    stages {
        stage('hello world') {
            steps {
                sh ''' 
                    echo hello world server has started
                '''
            }
        }
        stage('build docker image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE:latest .'
            }
        } 
               
    }


    post {
        success {
            echo 'Deployment Successful!'
        }
        failure {
            echo 'Deployment Failed!'
        }
    }
}
