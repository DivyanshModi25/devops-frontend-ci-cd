pipeline {
    agent any

    environment {
        DOCKER_IMAGE="techsavvydivyansh/react-app-cicd"
        DOCKER_TAG="latest"
    }

    stages {
        stage('hello world') {
            steps {
                sh 'echo "Hello world server has started"'
            }
        }

        stage('Login to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-creds', 
                                                  usernameVariable: 'DOCKER_HUB_USER', 
                                                  passwordVariable: 'DOCKER_HUB_PASS')]) {
                    sh 'echo $DOCKER_HUB_PASS | docker login -u $DOCKER_HUB_USER --password-stdin'
                }
            }  
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE:$DOCKER_TAG .'
            }
        } 

        stage('Push Image to Docker Hub') {
            steps {
                sh 'docker push $DOCKER_IMAGE:latest'
            }
        }

        // stage('Terraform Init , Apply') {
        //     steps {
        //         withCredentials([
        //             string(credentialsId: 'AWS_ACCESS_KEY_ID', variable: 'AWS_ACCESS_KEY_ID'),
        //             string(credentialsId: 'AWS_SECRET_ACCESS_KEY', variable: 'AWS_SECRET_ACCESS_KEY')
        //         ]) {
        //             sh '''
        //                 export AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
        //                 export AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
        //                 cd terraform
        //                 terraform init
        //                 terraform apply -auto-approve
        //             '''
        //         }
        //     }
        // }

        stage('Deploy New Docker Image to EC2') {
            steps {
                script {
                    def ec2_ip = '3.231.214.106'

                    echo "Deploying new Docker image to EC2 at: $ec2_ip"

                    withCredentials([sshUserPrivateKey(credentialsId: 'ec2-ssh-key', keyFileVariable: 'SSH_KEY')]) {
                        sh """
                        ssh -o StrictHostKeyChecking=no -i $SSH_KEY ubuntu@$ec2_ip <<-'EOF'
                            docker pull $DOCKER_IMAGE:$DOCKER_TAG
                            docker stop app || true
                            docker rm app || true
                            docker run -d -p 80:80 --name app $DOCKER_IMAGE:$DOCKER_TAG
                        EOF
                        """
                    }
                }
            }
        }
    } // <- Closing braces added here to properly close "stages"

    post {
        success {
            echo 'Deployment Successful!'
        }
        failure {
            echo 'Deployment Failed!'
        }
    }
}
