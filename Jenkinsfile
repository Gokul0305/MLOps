pipeline{

    // Agent Configuration

    agent{

        label "localwindows"

    }

    // Environment Setup

    environment{

        VENV_DIR  = 'JenkinsEnvironment'
        def PR = env.JOB_NAME.split('/').last()
        REPO = 'Python-Executables'
        PROJECT = 'Test'
        VERSION = '1.0.0'
        FILE_PATH = 'dist/main.exe'
    }

    // Stages

    stages{

        // Cloning Repository

        stage("Clone Repository"){
            steps{
                checkout scm
            }
            post{
                success{
                    echo "========Successfully Cloned the Repo========"
                }
                failure{
                    echo "========Cloning Failed========"
                }
            }
        }

        // Installing Requirements

stage('Set Up Environment') {
    steps {
        script {
            // Set up Python environment
            if (isUnix()) {
                sh """
                    python -m venv ${env.VENV_DIR}
                    . ${env.VENV_DIR}/bin/activate
                    pip install -r requirements.txt
                    pip install .
                    pip install html-testRunner
                """
            } else {
                bat """
                    call %VENV_DIR%\\Scripts\\activate
                    pip install -r requirements.txt
                    pip install .
                    pip install html-testRunner
                """
            }
        }
    }
}


        // Unittest

stage('Run Unit Tests') {
    steps {
        script {
            // Run unit tests and generate reports
            if (isUnix()) {
                sh "python tests/run_tests.py"
            } else {
                bat "python tests/run_tests.py"
            }
        }
    }
    post {
        success {
            echo "Unit tests passed. Proceeding to next stage."
        }
        failure {
            echo "Unit tests failed. Sending failure email notification."
            emailext(
                subject: "${env.JOB_NAME} - Build #${env.BUILD_NUMBER} - FAILURE - Unit tests: Failed",
                body: """<p style="font-size:16px; font-family:Arial;">Build #${env.BUILD_NUMBER} of project '${env.JOB_NAME}' failed.</p>
                        <p style="font-size:16px; font-family:Arial;">Unit tests have failed.</p>
                        <p style="font-size:16px; font-family:Arial;">${PR} initiated by: ${env.CHANGE_AUTHOR}</p>
                        <p style="font-size:16px; font-family:Arial;">Check the build details: <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                        <p style="font-size:16px; font-family:Arial;">Best Regards,<br>Jenkins</p>""",
                to: env.DEFAULT_RECIPIENTS
            )
        }
    }
}

        stage('Build Executable') {
            steps {
                // Build the .exe file using PyInstaller
                bat 'pyinstaller --onefile main.py'
            }
        }

        



        stage('Upload Artifact to Artifactory') {
            steps {
                script {
                    // Configure Artifactory server
                    def server = Artifactory.server(env.ARTIFACTORY_CREDENTIALS_ID)
                    
                    // Define upload specifications
                    def uploadSpec = """{
                        "files": [{
                            "pattern": "${FILE_PATH}",
                            "target": "${REPO}/${PROJECT}/${VERSION}/"
                        }]
                    }"""
                    
                    // Upload artifact
                    try {
                        server.upload(uploadSpec)
                    } catch (Exception e) {
                        echo "Error occurred during upload: ${e.getMessage()}"
                        throw e
                    }
                }
            }

        }

        stage('Tagging git source code') {
            steps {
                script {
                    bat "git tag v${VERSION}"
                    bat "git push origin v${VERSION}"
                }
            }
        }
        

        stage('Releasing New Build') {
            steps {
                script {
                    bat """
                    gh release create v${VERSION} --generate-notes --latest    --notes "[Download Artifact](http://192.168.1.40:8082/artifactory/Python-Executables/Test/1.0.0/main.exe)" --title "${PROJECT} v${VERSION}"
                    """
                }
            }
        }


    }

    

    // Post Build Actions

post {
    success {
        echo "Build successful. Sending success email notification."
        emailext(
            subject: "${env.JOB_NAME} - Build #${env.BUILD_NUMBER} - SUCCESS - Unit tests & Build: Successfully passed",
            body: """<p style="font-size:16px; font-family:Arial;">Build #${env.BUILD_NUMBER} of project '${env.JOB_NAME}' was successful.</p>
                    <p style="font-size:16px; font-family:Arial;">Unit tests and Build have passed successfully.</p>
                    <p style="font-size:16px; font-family:Arial;">${PR} initiated by: ${env.CHANGE_AUTHOR}</p>
                    <p style="font-size:16px; font-family:Arial;">Check the Jenkins build details: <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                    <p style="font-size:16px; font-family:Arial;">Check the JFrog Artifactory: <a href="${env.ARTIFACTORY_URL}/${REPO}/${PROJECT}/${VERSION}/">${env.ARTIFACTORY_URL}/${REPO}/${PROJECT}/${VERSION}/</a></p>
                    <p style="font-size:16px; font-family:Arial;">Best Regards,<br>Jenkins</p>""",
            to: env.DEFAULT_RECIPIENTS
        )
    }
}
}
