pipeline {
    agent any

    environment{
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

        // stage ('run test') {
        //     steps {
        //         sh '''
        //             npm i 
        //             npm test
        //         '''
        //     }
        // }

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

        stage ('push image to docker hub') {
            steps {
                  sh 'docker push $DOCKER_IMAGE:latest'
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
