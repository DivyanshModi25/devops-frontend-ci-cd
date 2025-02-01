pipeline {
    agent any

    stages {
        stage('build') {
            agent{
                docker{
                    image 'node:18-alpine'
                    args '--workdir /workspace'
                    reuseNode true
                }
            }
            steps {
                sh '''
                    ls -a                    
                '''
            }
        }        
    }
}
