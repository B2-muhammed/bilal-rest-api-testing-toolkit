
# Bilal REST API Testing Toolkit

A Python-based toolkit for REST API testing, HTTP request inspection, and automated unit testing using `requests`, `pytest`, and [httpbin.org](https://httpbin.org/).

## Project Overview

This project provides a simple command-line interface (CLI) for sending HTTP requests and inspecting server responses.

It is designed as a practical learning project covering REST API fundamentals, HTTP methods, JSON payloads, response handling, exception management, and automated testing.

## Features

- Send GET, POST, PUT, PATCH, and DELETE requests.
- Inspect HTTP status codes and response content.
- Measure HTTP response time.
- Submit JSON request payloads.
- Configure request timeouts.
- Handle connection, timeout, and HTTP errors.
- Run automated unit tests with pytest.
- Mock HTTP requests for reliable offline testing.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Requests | HTTP communication |
| Pytest | Automated testing |
| unittest.mock | Mocking HTTP requests |
| httpbin.org | HTTP testing service |

## Project Structure

```text
bilal-rest-api-testing-toolkit/
├── main.py
├── requirements.txt
├── pytest.ini
├── README.md
└── tests/
    └── test_request_inspection.py
```

## Installation

Clone the repository:

```bash
git clone https://github.com/B2-muhammed/bilal-rest-api-testing-toolkit.git
```

Navigate into the project:

```bash
cd bilal-rest-api-testing-toolkit
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it:

**Windows PowerShell**

```powershell
.venv\Scripts\Activate.ps1
```

**macOS/Linux**

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Usage

### Default GET request

```bash
python main.py
```

### POST request with JSON payload

```bash
python main.py --method POST --json '{"task":"learn REST APIs","priority":"high"}'
```

### Send a request to another endpoint

```bash
python main.py --method GET --url https://httpbin.org/get
```

### Configure request timeout

```bash
python main.py --method GET --timeout 5
```

## Automated Testing

Run the test suite:

```bash
pytest -v
```

The current test suite covers:

1. Successful HTTP request inspection.
2. Non-JSON response handling.
3. Request timeout propagation.
4. Command-line argument parsing.

HTTP requests are mocked during unit testing, so these tests do not require a live connection to httpbin.org.

## Learning Objectives

This project supports practical learning in:

- REST API and HTTP communication.
- HTTP methods and request-response cycles.
- JSON serialization and deserialization.
- Python exception handling.
- Command-line application development.
- Unit testing and mocking.
- Test organization and maintainable code.

## Important Notes

- httpbin.org is an HTTP testing service, not a persistent database.
- Response times depend on the execution environment.
- Never commit passwords, API keys, access tokens, or other secrets.

## Project Status

**Learning and development project.**

Future improvements may include additional HTTP authentication tests, response-header inspection, request logging, and expanded test coverage.

## Author

**Bilal Abdulkadir Muhammed**

IT Support Specialist | Data Analyst | MSc Artificial Intelligence Student

- GitHub: [@B2-muhammed](https://github.com/B2-muhammed)
