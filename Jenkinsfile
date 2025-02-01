pipeline {
    agent any

    stages {
        stage('docker debug'){
            steps {
                sh ''' 
                    echo debuged something
                '''
            }
        }
        stage('build') {
            agent{
                docker{
                    image 'node:18-alpine'
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
