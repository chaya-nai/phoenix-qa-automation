# Phoenix QA Automation
A QA automation portfolio project built with Python, PyTest, Playwright, and Flask.

The project demonstrates API and UI automated testing, Page Object Model (POM), data-driven testing, test reporting, and CI with GitHub Actions.

## Tech Stack
    - Python
    - PyTest
    - Playwright
    - Requests
    - Flask
    - pytest-html
    - GitHub Actions

## Test Coverage
### API Tests
    - Login API
    - Character API
    - Battle API
    - Status and health endpoints
    - Positive and negative scenarios

### UI Tests
    - Login
    - Battle
    - Shop / item purchasing
    - Inventory
    - Equipment management
    - Positive and negative scenarios

## Project Structure
```text
    phoenix-qa-automation/
    ├── api_test/       # API automated tests
    ├── ui_test/        # Playwright UI tests
    ├── pages/          # Page Object Model
    ├── data/           # Test data
    ├── templates/      # Flask HTML templates
    ├── static/         # Flask static files
    ├── .github/
    │   └── workflows/  # CI workflow
    ├── app.py           # Demo application
    ├── conftest.py      # Shared PyTest fixtures/hooks
    ├── pytest.ini       # PyTest configuration
    └── requirements.txt
```
## Setup
### 1. Clone the repository

```bash
git clone https://github.com/chaya-nai/phoenix-qa-automation.git
cd phoenix-qa-automation
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows:

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Install Playwright Chromium

```bash
playwright install chromium
```

## Running the Application
Start the Flask application:

```bash
python app.py
```

The application will run at:

```text
http://127.0.0.1:5000
```

## Running Tests
Make sure the Flask application is running before executing the tests.

### Run all tests

```bash
python -m pytest -v
```

### Run API tests

```bash
python -m pytest api_test -v
```

### Run UI tests

```bash
python -m pytest ui_test -v
```

### Run Smoke tests

```bash
python -m pytest -v -m smoke
```

### Generate HTML report

```bash
python -m pytest -v --html=reports/report.html --self-contained-html
```

## Parallel Execution
Tests that do not share test data can be executed in parallel using pytest-xdist.

```bash
python -m pytest -v -n 2
```
Tests that share or modify the same test data should be executed serially to avoid race conditions.

## Continuous Integration
This project uses GitHub Actions for Continuous Integration.

On every push to the `main` branch, the CI pipeline automatically:

1. Checks out the source code
2. Sets up Python
3. Installs project dependencies
4. Installs Playwright Chromium
5. Starts the Flask application
6. Runs the automated test suite
7. Generates an HTML test report
8. Uploads the test report as a GitHub Actions artifact

UI tests run in headless mode in the CI environment.

## Test Design
The automation framework includes:

- Page Object Model (POM) for UI tests
- Data-driven testing with JSON test data
- PyTest fixtures for test setup and teardown
- Positive and negative test scenarios
- Smoke test markers
- Failure screenshots and Playwright traces
- HTML test reports
- Parallel test execution
- CI execution with GitHub Actions