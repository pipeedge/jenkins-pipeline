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
                stage('Code Formatting with Black') {
                    steps {
                        echo 'Checking code formatting with Black...'
                        sh '''
                            . ${VIRTUAL_ENV}/bin/activate
                            echo "Checking code formatting..."
                            black --check --line-length=100 calculator.py test_calculator.py
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
        
        // Security Scan stage disabled as requested
        // stage('Security Scan') {
        //     steps {
        //         echo 'Running security scan with Bandit...'
        //         sh '''
        //             . ${VIRTUAL_ENV}/bin/activate
        //             echo "Running Bandit security scan..."
        //             bandit -r . -f json -o bandit-report.json --exclude ${VIRTUAL_ENV} || true
        //             bandit -r . --exclude ${VIRTUAL_ENV}
        //             echo "Security scan completed!"
        //         '''
        //     }
        //     post {
        //         always {
        //             // Archive the security report
        //             archiveArtifacts artifacts: 'bandit-report.json', allowEmptyArchive: true
        //         }
        //     }
        // }
        
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
                    
                    // Note: Coverage publishing disabled - Cobertura plugin not available
                    // publishCoverage adapters: [coberturaAdapter('coverage.xml')], sourceFileResolver: sourceFiles('STORE_LAST_BUILD')
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
            
            // Send success notification
            script {
                echo 'Sending success notification...'
                emailext (
                    subject: "SUCCESS: ${JOB_NAME} - Build #${BUILD_NUMBER}",
                    body: """
                        <h2>Pipeline Execution Successful!</h2>
                        <p><strong>Job:</strong> ${JOB_NAME}</p>
                        <p><strong>Build Number:</strong> ${BUILD_NUMBER}</p>
                        <p><strong>Branch:</strong> ${env.BRANCH_NAME ?: 'N/A'}</p>
                        <p><strong>Build URL:</strong> <a href="${BUILD_URL}">${BUILD_URL}</a></p>
                        <p><strong>Duration:</strong> ${currentBuild.durationString}</p>
                        <br>
                        <p>All stages completed successfully including:</p>
                        <ul>
                            <li>Code quality checks (Black, MyPy)</li>
                            <li>Unit tests with coverage</li>
                            <li>Integration tests</li>
                            <li>Build artifacts creation</li>
                        </ul>
                        <br>
                        <p>This is an automated notification from Jenkins Pipeline.</p>
                    """,
                    to: "yuanliangyyy@gmail.com",
                    mimeType: "text/html"
                )
            }
        }
        
        failure {
            echo 'Pipeline execution failed!'
            
            // Send failure notification
            script {
                echo 'Sending failure notification...'
                emailext (
                    subject: "FAILURE: ${JOB_NAME} - Build #${BUILD_NUMBER}",
                    body: """
                        <h2>Pipeline Execution Failed!</h2>
                        <p><strong>Job:</strong> ${JOB_NAME}</p>
                        <p><strong>Build Number:</strong> ${BUILD_NUMBER}</p>
                        <p><strong>Branch:</strong> ${env.BRANCH_NAME ?: 'N/A'}</p>
                        <p><strong>Build URL:</strong> <a href="${BUILD_URL}">${BUILD_URL}</a></p>
                        <p><strong>Duration:</strong> ${currentBuild.durationString}</p>
                        <br>
                        <p><strong>Failed Stage:</strong> ${currentBuild.description ?: 'Unknown'}</p>
                        <br>
                        <p>Please check the Jenkins console output for detailed error information.</p>
                        <p>Common failure points:</p>
                        <ul>
                            <li>Code quality checks (Black, MyPy)</li>
                            <li>Unit tests</li>
                            <li>Integration tests</li>
                            <li>Build artifacts creation</li>
                        </ul>
                        <br>
                        <p>This is an automated notification from Jenkins Pipeline.</p>
                    """,
                    to: "yuanliangyyy@gmail.com",
                    mimeType: "text/html"
                )
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