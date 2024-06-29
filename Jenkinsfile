pipeline{

    // Agent Configuration

    agent{

        label "localwindows"

    }

    // Environment Setup

    environment{

        VENV_DIR  = 'JenkinsEnvironment'
        def PR = env.JOB_NAME.split('/').last()
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
                            python -m venv ${env.VENV_NAME}
                            . ${env.VENV_NAME}/bin/activate
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
                        sh """
                            python tests/run_tests.py
                        """
                    } else {
                        bat """
                            python tests/run_tests.py
                        """
                    }
                }
            }

            post {

                success{
                        emailext(
                                subject: "${env.JOB_NAME} - Build #${env.BUILD_NUMBER} - SUCCESS - Unit tests: Successfully passed",
                                body: """<p style="font-size:16px; font-family:Arial;">Build #${env.BUILD_NUMBER} of project '${env.JOB_NAME}' was successful.</p>
                                        <p style="font-size:16px; font-family:Arial;">Unit tests have passed successfully.</p>
                                        <p style="font-size:16px; font-family:Arial;">${PR} initiated by: ${env.CHANGE_AUTHOR}</p>
                                        <p style="font-size:16px; font-family:Arial;">Check the build details: <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                                        <p style="font-size:16px; font-family:Arial;">Best Regards,<br>Jenkins</p>""",
                                to: "gokulvignesh1234@gmail.com"
                            )
                    
                }

                failure{
                        emailext(
                            subject: "${env.JOB_NAME} - Build #${env.BUILD_NUMBER} - FAILURE - Unit tests: Failed",
                            body: """<p style="font-size:16px; font-family:Arial;">Build #${env.BUILD_NUMBER} of project '${env.JOB_NAME}' failed.</p>
                                    <p style="font-size:16px; font-family:Arial;">Unit tests have failed.</p>
                                    <p style="font-size:16px; font-family:Arial;">${PR} initiated by: ${env.CHANGE_AUTHOR}</p>
                                    <p style="font-size:16px; font-family:Arial;">Check the build details: <a href="${env.BUILD_URL}">${env.BUILD_URL}</a></p>
                                    <p style="font-size:16px; font-family:Arial;">Best Regards,<br>Jenkins</p>""",
                            to: "gokulvignesh1234@gmail.com"
                        )
                }
                
            }
        }


    }

    // Post Build Actions

    post{

        always{
        echo "========Successfully Cloned the Repo========"
        }
    }
}
