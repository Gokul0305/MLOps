pipeline{

    agent{
        label "localwindows"
    }

    triggers {
        githubPullRequest()
    }

    environment{

        PYTHON_VERSION = '3.9'
        VENV_NAME = 'JenkinsEnvironment'
    }

    stages{

        stage('Check PR') {
            when {
                allOf {
                    expression { 
                        def changeTarget = githubScmSource().getPRTargetBranch(env.CHANGE_ID)
                        def changeSource = githubScmSource().getPRSourceBranch(env.CHANGE_ID)
                        return changeSource == 'dev' && changeTarget == 'main'
                    }
                }
            }
            steps {
                echo 'Running pipeline for PR from dev to main'
                // Your build steps go here
            }
        }
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
                            pip install xmlrunner
                        """
                    } else {
                        bat """
                            python -m venv ${env.VENV_NAME}
                            ${env.VENV_NAME}\\Scripts\\activate
                            pip install -r requirements.txt
                            pip install .
                            pip install xmlrunner
                        """
                    }
                }
            }
        }

        stage('Run Unit Tests') {
            steps {
                script {
                    // Run unit tests and generate reports
                    if (isUnix()) {
                        sh """
                            . ${env.VENV_NAME}/bin/activate
                            python -m xmlrunner discover -s tests -o .
                        """
                    } else {
                        bat """
                            ${env.VENV_NAME}\\Scripts\\activate
                            python -m xmlrunner discover -s tests -o .
                        """
                    }
                }
            }
        }


    }
    post{
        always{
        echo "========Successfully Cloned the Repo========"
        }
    }
}
