pipeline {
    agent any
    
    // Define pipeline options
    options {
        // Keep only the last 10 builds
        buildDiscarder(logRotator(numToKeepStr: '10'))
        // Timeout the entire pipeline after 30 minutes
        timeout(time: 30, unit: 'MINUTES')
        // Add timestamps to console output
        timestamps()
    }
    
    // Define environment variables
    environment {
        PYTHON_VERSION = '3.9'
        VIRTUAL_ENV = 'venv'
        PATH = "${WORKSPACE}/${VIRTUAL_ENV}/bin:${PATH}"
    }
    
    // Define pipeline stages
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
                
                // Display build information
                script {
                    echo "Build Number: ${BUILD_NUMBER}"
                    echo "Build ID: ${BUILD_ID}"
                    echo "Job Name: ${JOB_NAME}"
                    echo "Workspace: ${WORKSPACE}"
                }
            }
        }
        
        stage('Setup Environment') {
            steps {
                echo 'Setting up Python environment...'
                sh '''
                    echo "Python version:"
                    python3 --version
                    
                    echo "Creating virtual environment..."
                    python3 -m venv ${VIRTUAL_ENV}
                    
                    echo "Activating virtual environment and upgrading pip..."
                    . ${VIRTUAL_ENV}/bin/activate
                    pip install --upgrade pip
                    
                    echo "Installing dependencies..."
                    pip install -r requirements.txt
                    
                    echo "Installed packages:"
                    pip list
                '''
            }
        }
        
        stage('Code Quality Checks') {
            parallel {
                stage('Linting with Flake8') {
                    steps {
                        echo 'Running code linting with Flake8...'
                        sh '''
                            . ${VIRTUAL_ENV}/bin/activate
                            echo "Running Flake8 linter..."
                            flake8 --max-line-length=100 --exclude=${VIRTUAL_ENV} --statistics --output-file=flake8-report.txt .
                            echo "Flake8 linting completed successfully!"
                        '''
                    }
                    post {
                        always {
                            // Archive the flake8 report
                            archiveArtifacts artifacts: 'flake8-report.txt', allowEmptyArchive: true
                        }
                    }
                }
                
                stage('Code Formatting with Black') {
                    steps {
                        echo 'Checking code formatting with Black...'
                        sh '''
                            . ${VIRTUAL_ENV}/bin/activate
                            echo "Checking code formatting..."
                            black --check --line-length=100 --exclude=${VIRTUAL_ENV} .
                            echo "Code formatting check completed!"
                        '''
                    }
                }
                
                stage('Type Checking with MyPy') {
                    steps {
                        echo 'Running type checking with MyPy...'
                        sh '''
                            . ${VIRTUAL_ENV}/bin/activate
                            echo "Running MyPy type checker..."
                            mypy --ignore-missing-imports --no-strict-optional calculator.py
                            echo "Type checking completed successfully!"
                        '''
                    }
                }
            }
        }
        
        stage('Security Scan') {
            steps {
                echo 'Running security scan with Bandit...'
                sh '''
                    . ${VIRTUAL_ENV}/bin/activate
                    echo "Running Bandit security scan..."
                    bandit -r . -f json -o bandit-report.json --exclude ${VIRTUAL_ENV} || true
                    bandit -r . --exclude ${VIRTUAL_ENV}
                    echo "Security scan completed!"
                '''
            }
            post {
                always {
                    // Archive the security report
                    archiveArtifacts artifacts: 'bandit-report.json', allowEmptyArchive: true
                }
            }
        }
        
        stage('Unit Tests') {
            steps {
                echo 'Running unit tests with pytest...'
                sh '''
                    . ${VIRTUAL_ENV}/bin/activate
                    echo "Running pytest with coverage..."
                    pytest -v --cov=calculator --cov-report=xml --cov-report=html --cov-report=term-missing --junitxml=pytest-results.xml
                    echo "Unit tests completed successfully!"
                '''
            }
            post {
                always {
                    // Publish test results
                    junit 'pytest-results.xml'
                    
                    // Archive coverage reports
                    archiveArtifacts artifacts: 'htmlcov/**', allowEmptyArchive: true
                    archiveArtifacts artifacts: 'coverage.xml', allowEmptyArchive: true
                    
                    // Publish coverage report (if Coverage plugin is installed)
                    publishCoverage adapters: [coberturaAdapter('coverage.xml')], sourceFileResolver: sourceFiles('STORE_LAST_BUILD')
                }
            }
        }
        
        stage('Integration Tests') {
            steps {
                echo 'Running integration tests...'
                sh '''
                    . ${VIRTUAL_ENV}/bin/activate
                    echo "Running calculator demo to verify functionality..."
                    python calculator.py
                    echo "Integration tests completed successfully!"
                '''
            }
        }
        
        stage('Build Artifacts') {
            steps {
                echo 'Creating build artifacts...'
                sh '''
                    echo "Creating deployment package..."
                    mkdir -p dist
                    cp calculator.py dist/
                    cp requirements.txt dist/
                    
                    echo "Build artifacts created in dist/ directory"
                    ls -la dist/
                '''
            }
            post {
                always {
                    // Archive build artifacts
                    archiveArtifacts artifacts: 'dist/**', allowEmptyArchive: false
                }
            }
        }
        
        stage('Deploy to Staging') {
            when {
                // Only deploy on main/master branch
                anyOf {
                    branch 'main'
                    branch 'master'
                }
            }
            steps {
                echo 'Deploying to staging environment...'
                script {
                    // Simulate deployment process
                    sh '''
                        echo "Simulating deployment to staging..."
                        echo "Deployment package ready at: ${WORKSPACE}/dist/"
                        echo "Calculator application deployed successfully to staging!"
                        
                        # In a real scenario, you would copy files to staging server
                        # scp dist/* user@staging-server:/path/to/app/
                        # ssh user@staging-server "systemctl restart calculator-app"
                    '''
                }
            }
        }
    }
    
    // Post-build actions
    post {
        always {
            echo 'Pipeline execution completed!'
            
            // Clean up workspace (optional)
            // cleanWs()
        }
        
        success {
            echo 'Pipeline executed successfully!'
            
            // Send success notification (configure as needed)
            script {
                if (env.BRANCH_NAME == 'main' || env.BRANCH_NAME == 'master') {
                    echo 'Sending success notification for main branch...'
                    // emailext (
                    //     subject: "SUCCESS: ${JOB_NAME} - Build #${BUILD_NUMBER}",
                    //     body: "The pipeline executed successfully. Build details: ${BUILD_URL}",
                    //     to: "${DEFAULT_RECIPIENTS}"
                    // )
                }
            }
        }
        
        failure {
            echo 'Pipeline execution failed!'
            
            // Send failure notification
            script {
                echo 'Sending failure notification...'
                // emailext (
                //     subject: "FAILURE: ${JOB_NAME} - Build #${BUILD_NUMBER}",
                //     body: "The pipeline failed. Please check the logs: ${BUILD_URL}",
                //     to: "${DEFAULT_RECIPIENTS}"
                // )
            }
        }
        
        unstable {
            echo 'Pipeline execution was unstable!'
        }
        
        changed {
            echo 'Pipeline status changed from previous build!'
        }
    }
} 