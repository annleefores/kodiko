pipeline {
  agent none

  stages {
    stage('Backend') {
      agent {
        docker {image 'python:3.10.12-buster'}
      }
      steps {
        sh 'python3 --version'
      }
    }
    stage('Frontend') {
      agent {
        docker {image 'node:18-alpine'}
      }
      steps {
        sh 'node --version'
      }
    }
  }
}