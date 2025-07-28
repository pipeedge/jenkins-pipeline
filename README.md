# Calculator Application - Jenkins Pipeline Demo

A Python calculator application with comprehensive CI/CD pipeline using Jenkins. This project demonstrates best practices for Python development including unit testing, code quality checks, security scanning, and automated deployment.

## 🚀 Features

- **Calculator Operations**: Basic arithmetic operations (add, subtract, multiply, divide, power, square root)
- **Comprehensive Testing**: Unit tests and integration tests with pytest
- **Code Quality**: Automated linting with Flake8, formatting with Black, and type checking with MyPy
- **Security Scanning**: Security vulnerability detection with Bandit
- **CI/CD Pipeline**: Complete Jenkins pipeline with multiple stages
- **Coverage Reports**: Test coverage reporting with pytest-cov
- **Logging**: Structured logging for all operations

## 📁 Project Structure

```
pipeline/
├── calculator.py          # Main calculator application
├── test_calculator.py     # Comprehensive unit tests
├── requirements.txt       # Python dependencies
├── Jenkinsfile           # Jenkins pipeline definition
├── pytest.ini           # Pytest configuration
├── setup.cfg            # Tool configurations (flake8, mypy, coverage)
├── .gitignore           # Git ignore patterns
└── README.md            # This file
```

## 🛠️ Local Development Setup

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd pipeline
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python calculator.py
   ```

5. **Run tests**
   ```bash
   pytest -v --cov=calculator --cov-report=html
   ```

6. **Run code quality checks**
   ```bash
   # Linting
   flake8 --max-line-length=100 .
   
   # Code formatting check
   black --check --line-length=100 .
   
   # Type checking
   mypy --ignore-missing-imports calculator.py
   
   # Security scan
   bandit -r .
   ```

## 🔧 Jenkins Setup Guide

### Prerequisites

- Jenkins server (version 2.400+)
- Git plugin
- Pipeline plugin
- Python 3.9+ installed on Jenkins agents

### Required Jenkins Plugins

Install the following plugins through Jenkins UI (Manage Jenkins → Manage Plugins):

1. **Essential Plugins**:
   - Pipeline
   - Git
   - Workspace Cleanup
   - Timestamper
   - Build Timeout

2. **Reporting Plugins**:
   - JUnit
   - Coverage (Cobertura)
   - HTML Publisher
   - Warnings Next Generation

3. **Notification Plugins** (optional):
   - Email Extension
   - Slack Notification

### Step-by-Step Jenkins UI Setup

#### 1. Create a New Pipeline Job

1. **Navigate to Jenkins Dashboard**
   - Open your Jenkins instance in a web browser
   - Click "New Item" on the left sidebar

2. **Configure Job Settings**
   - Enter job name: `calculator-pipeline-demo`
   - Select "Pipeline" as the project type
   - Click "OK"

#### 2. Configure General Settings

1. **Description**
   ```
   Calculator Application CI/CD Pipeline Demo
   Demonstrates Python testing, code quality, and deployment automation
   ```

2. **Build Triggers** (Optional)
   - ☑️ GitHub hook trigger for GITScm polling (if using GitHub webhooks)
   - ☑️ Poll SCM: `H/5 * * * *` (poll every 5 minutes)

3. **Advanced Project Options**
   - ☑️ Do not allow concurrent builds
   - Build timeout: 30 minutes

#### 3. Configure Pipeline

1. **Pipeline Definition**
   - Select "Pipeline script from SCM"

2. **SCM Configuration**
   - SCM: Git
   - Repository URL: `https://github.com/your-username/pipeline.git`
   - Credentials: Add your Git credentials if repository is private
   - Branch Specifier: `*/main` (or `*/master`)

3. **Script Path**
   - Script Path: `Jenkinsfile` (default)

4. **Additional Behaviours** (if needed)
   - Click "Add" → "Clean before checkout"
   - Click "Add" → "Checkout to sub-directory" if needed

#### 4. Configure Build Environment

1. **Build Environment**
   - ☑️ Delete workspace before build starts
   - ☑️ Add timestamps to the Console Output

#### 5. Save and Build

1. **Save Configuration**
   - Click "Save" to save the pipeline configuration

2. **Run First Build**
   - Click "Build Now" to trigger the first pipeline execution

### 🔧 Advanced Jenkins Configuration

#### Configure Global Tools

1. **Navigate to Global Tool Configuration**
   - Manage Jenkins → Global Tool Configuration

2. **Python Configuration**
   - Add Python installation
   - Name: `Python-3.9`
   - Install automatically or specify path: `/usr/bin/python3`

#### Configure Credentials

1. **Add Git Credentials** (if needed)
   - Manage Jenkins → Manage Credentials
   - Click "Global credentials"
   - Click "Add Credentials"
   - Kind: Username with password or SSH Username with private key
   - ID: `git-credentials`

2. **Add Email Configuration** (optional)
   - Manage Jenkins → Configure System
   - E-mail Notification section
   - Configure SMTP server settings

#### Set Up Webhooks (GitHub Integration)

1. **GitHub Repository Settings**
   - Navigate to your GitHub repository
   - Settings → Webhooks → Add webhook
   - Payload URL: `http://your-jenkins-url/github-webhook/`
   - Content type: application/json
   - Events: Push events, Pull requests

2. **Jenkins GitHub Configuration**
   - Manage Jenkins → Configure System
   - GitHub section → Add GitHub Server
   - Configure API URL and credentials

### 📊 Pipeline Stages Overview

The Jenkins pipeline includes the following stages:

1. **Checkout**: Source code retrieval from Git
2. **Setup Environment**: Python virtual environment creation and dependency installation
3. **Code Quality Checks** (Parallel):
   - Flake8 linting
   - Black code formatting check
   - MyPy type checking
4. **Security Scan**: Bandit security vulnerability scanning
5. **Unit Tests**: Pytest execution with coverage reporting
6. **Integration Tests**: Application functionality verification
7. **Build Artifacts**: Package creation for deployment
8. **Deploy to Staging**: Conditional deployment (main/master branch only)

### 📈 Viewing Results

#### Test Results
- Navigate to build → "Test Results"
- View detailed test reports and trends

#### Coverage Reports
- Build → "Coverage Report"
- HTML coverage reports archived as build artifacts

#### Code Quality Reports
- Build artifacts contain:
  - `flake8-report.txt`: Linting results
  - `bandit-report.json`: Security scan results
  - `htmlcov/`: Coverage HTML reports

#### Build Artifacts
- Navigate to build → "Build Artifacts"
- Download deployment packages from `dist/` directory

### 🚨 Troubleshooting

#### Common Issues

1. **Python Not Found**
   ```
   Solution: Ensure Python 3.9+ is installed on Jenkins agents
   Configure Global Tool Configuration → Python installations
   ```

2. **Permission Denied**
   ```
   Solution: Ensure Jenkins user has proper permissions
   sudo usermod -a -G docker jenkins (if using Docker)
   ```

3. **Virtual Environment Issues**
   ```
   Solution: Clean workspace and ensure python3-venv is installed
   sudo apt-get install python3-venv
   ```

4. **Plugin Missing**
   ```
   Solution: Install required plugins through Manage Plugins
   Restart Jenkins after plugin installation
   ```

#### Pipeline Debugging

1. **Enable Debug Logging**
   - Add `set -x` to shell scripts in Jenkinsfile
   - Use `echo` statements for variable inspection

2. **Workspace Inspection**
   - Navigate to build → "Workspace"
   - Examine files and directory structure

3. **Console Output**
   - Review full console output for detailed error messages
   - Look for specific stage failures

### 🔄 Pipeline Customization

#### Modifying the Pipeline

1. **Edit Jenkinsfile**
   - Modify stages, add new tools, or change configurations
   - Commit changes to trigger automatic pipeline updates

2. **Environment Variables**
   - Add custom environment variables in the `environment` block
   - Use `${VARIABLE_NAME}` syntax in pipeline scripts

3. **Conditional Deployment**
   - Modify `when` conditions for deployment stages
   - Add approval steps for production deployments

#### Adding New Stages

```groovy
stage('Custom Stage') {
    steps {
        echo 'Custom stage execution...'
        sh '''
            # Your custom commands here
        '''
    }
}
```

### 📧 Notifications

#### Email Notifications

Uncomment and configure email sections in Jenkinsfile:

```groovy
emailext (
    subject: "Build Status: ${JOB_NAME} - ${BUILD_NUMBER}",
    body: "Build details: ${BUILD_URL}",
    to: "team@company.com"
)
```

#### Slack Integration

Install Slack Notification plugin and add:

```groovy
slackSend (
    channel: '#devops',
    message: "Build ${BUILD_NUMBER} completed: ${BUILD_URL}"
)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Ensure all tests pass: `pytest`
5. Run code quality checks: `flake8`, `black --check`, `mypy`
6. Commit your changes: `git commit -am 'Add feature'`
7. Push to the branch: `git push origin feature-name`
8. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For questions and support:
- Create an issue in the GitHub repository
- Check the troubleshooting section above
- Review Jenkins logs and console output

---

**Happy Coding! 🚀** 