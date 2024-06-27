pipeline{

    // Agent Configuration

    agent{

        label "localwindows"

    }

    // Environment Setup

    environment{

        VENV_DIR  = 'JenkinsEnvironment'
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
        }


    }

    // Post Build Actions

    post{

        always{
        echo "========Successfully Cloned the Repo========"
        }
    }
}