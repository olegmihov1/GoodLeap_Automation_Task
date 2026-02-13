# GoodLeap QA Home Task Project

A comprehensive test automation suite for **Swag Labs** (UI) and **Swagger Petstore** (API) built with Python, Playwright, and pytest.

## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running Tests](#running-tests)
- [Test Coverage](#test-coverage)
- [Reports](#reports)
- [Design Decisions](#design-decisions)

---

## Overview

| Component | Target Application | Framework |
|-----------|-------------------|-----------|
| **Part 1: UI Tests** | [Swag Labs](https://www.saucedemo.com/) | Playwright |
| **Part 2: API Tests** | [Swagger Petstore](https://petstore.swagger.io/) | pytest + requests |

---

## Project Structure

```
Project Task Goodleap/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── pytest.ini               # Pytest configuration
├── conftest.py              # Global pytest fixtures
├── flows.txt                # UI test scenarios documentation
│
├── pages/                   # Page Object Model classes
│   ├── __init__.py
│   ├── base_page.py         # Base page with common methods
│   ├── login_page.py        # Login page object
│   ├── inventory_page.py    # Products/inventory page object
│   ├── cart_page.py         # Shopping cart page object
│   └── checkout_page.py     # Checkout flow page object
│
├── tests/                   # UI automation tests
│   ├── __init__.py
│   ├── test_login.py        # Login functionality tests
│   ├── test_inventory.py    # Product page tests
│   ├── test_cart.py         # Shopping cart tests
│   └── test_checkout.py     # Checkout flow tests
│
└── api/                     # API automation tests
    ├── __init__.py
    ├── api-tests.md         # API test documentation
    ├── conftest.py          # API test fixtures
    ├── pet_client.py        # Pet API client class
    └── test_pet_api.py      # Pet endpoint tests
```

---

## Prerequisites

- **Python 3.10+** installed
- **pip** package manager

---

## Installation

``
### 1. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
python.exe -m pip install --upgrade pip
pip install pytest
```

### 3. Install Playwright Browsers
```bash
pip install playwright
playwright install
pip install requests playwright pytest pytest-html pytest-asyncio
```

---

## Running Tests

### Run All Tests (UI + API)
```bash
pytest -v
```

### Run UI Tests Only
```bash
pytest tests/ -v
```

### Run API Tests Only
```bash
pytest api/ -v
```

### Run Tests by Marker
```bash
# Run smoke tests
pytest -v -m smoke

# Run critical tests
pytest -v -m critical

# Run UI tests only
pytest -v -m ui

# Run API tests only
pytest -v -m api
```

### Run with HTML Report
```bash
pytest -v --html=reports/test-report.html --self-contained-html
```

### Run Specific Test File
```bash
pytest tests/test_login.py -v
pytest api/test_pet_api.py -v
```

### Run Specific Test Class
```bash
pytest tests/test_checkout.py::TestCheckout -v
```

### Run Specific Test
```bash
pytest tests/test_login.py::TestLogin::test_valid_user_login -v
```

### Run in Headed Mode (See Browser)
```bash
# Modify conftest.py: change headless=True to headless=False
pytest tests/ -v
```

---

## Test Coverage

### UI Tests (Part 1) - 39 Tests

| Module | Tests | Description |
|--------|-------|-------------|
| Login | 8 | Authentication, validation, logout |
| Inventory | 12 | Product display, sorting, add to cart |
| Cart | 9 | Cart operations, continue shopping |
| Checkout | 10 | E2E checkout, validation, completion |

See `flows.txt` for detailed test scenarios.

### API Tests (Part 2) - 25 Tests

| Endpoint | Tests | Description |
|----------|-------|-------------|
| POST /pet | 4 | Create pet operations |
| GET /pet/{id} | 3 | Get pet by ID |
| PUT /pet | 3 | Update pet |
| DELETE /pet/{id} | 3 | Delete pet |
| GET /pet/findByStatus | 5 | Find by status |
| POST /pet/{id} (form) | 3 | Update with form |
| Edge Cases | 4 | Boundary testing |

See `api/api-tests.md` for detailed API test documentation.

---

## Reports

### HTML Reports
```bash
# Generate HTML report
pytest -v --html=reports/test-report.html --self-contained-html
```

### Allure Reports (Optional)
```bash
# Run tests with Allure
pytest --alluredir=allure-results

# Generate report
allure serve allure-results
```

---

## Design Decisions

### Architecture
- **Page Object Model (POM)**: UI tests use POM for maintainability and reusability
- **API Client Pattern**: API tests use a dedicated client class for clean HTTP operations
- **pytest Fixtures**: Shared setup/teardown logic through fixtures

### Test Selection Rationale

**UI Tests** focus on:
- Critical user journeys (login, add to cart, checkout)
- Input validation (required fields, error messages)
- Core functionality (sorting, cart management)

**API Tests** focus on:
- CRUD operations for Pet endpoints
- Error handling (404, invalid inputs)
- Boundary conditions (special characters, unicode)

### Framework Choices
- **Playwright**: Modern, fast, auto-wait features
- **pytest**: Flexible, extensive plugin ecosystem
- **requests**: Simple, reliable HTTP library

---

## Test Credentials

For Swag Labs (https://www.saucedemo.com/):

| User Type | Username | Password |
|-----------|----------|----------|
| Standard | standard_user | secret_sauce |
| Locked Out | locked_out_user | secret_sauce |
| Problem | problem_user | secret_sauce |

---

## Troubleshooting

### Playwright Installation Issues
```bash
# If browser installation fails
playwright install chromium

# Or install with dependencies
playwright install-deps
```

### Test Failures Due to Timeout
- Increase timeout in `conftest.py`
- Check internet connection
- Verify target applications are accessible

### Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf venv  # or delete manually on Windows
python -m venv venv
# Re-activate and reinstall
```

---

## Author

**Oleg Mihov**  

