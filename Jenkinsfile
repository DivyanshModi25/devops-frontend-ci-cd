pipeline {
    agent any
    environment {
        DOCKER_IMAGE = 'node:18-alpine'
    }
    stages {
        stage('Build') {
            steps {
                script {
                    // Ensure Docker is running
                    if (!sh(script: 'docker ps', returnStatus: true)) {
                        error "Docker daemon is not running"
                    }

                    // Use Unix-style paths for volume mounts in Docker
                    docker.image(DOCKER_IMAGE).inside("-w /workspace -v /c/ProgramData/Jenkins/.jenkins/workspace/test-docker-pipeline:/workspace") {
                        // Verifying working directory inside the container
                        sh 'pwd'
                        sh 'ls -la' // List files to verify volume mount and working directory

                        // Your build steps here, for example:
                        sh 'node -v'  // Example: Check Node.js version inside the container
                    }
                }
            }
        }
    }
}
