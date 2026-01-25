# OpenCart Automation Testing Project – Admin Panel UI

This repository contains an automated UI testing project for the OpenCart Admin Panel.
The project automates end-to-end validation of critical administrative workflows
using Selenium WebDriver and PyTest.

The framework is built using the Page Object Model (POM) pattern and includes
soft assertions, screenshots, and HTML reporting to provide clear and
traceable test results.

---

## Project purpose

The goal of this project is to:

- Automate core OpenCart Admin Panel functionality
- Validate product and order management workflows
- Ensure admin actions update system data correctly
- Provide reliable regression coverage
- Demonstrate a structured automation framework suitable for real projects

This project complements the manual admin panel testing by providing repeatable,
fast, and maintainable automated coverage.

---

## System under test

- Application: OpenCart
- Area: Admin Panel (Back Office)
- Version: 4.1.0.3
- Environment: Local (XAMPP)
- OS: Windows 11
- Browsers: Chrome, Firefox, Edge
- User role: Admin

---

## Automation scope

### In scope
- Admin login and dashboard access
- Product management:
  - add new product
  - edit existing product
  - delete product
- Order management:
  - view customer order details
  - update order status to "Shipped"

### Out of scope
- Storefront (customer UI)
- API testing
- Performance and load testing
- Security testing
- Admin configuration and reports (future scope)

---

## Test approach

- UI automation using Selenium WebDriver
- PyTest as the test framework
- Page Object Model for clean separation of logic
- Custom SoftAssert utility to capture multiple validations per test
- Screenshots captured for executed steps
- HTML and Allure reports generated for execution evidence

---

## Repository structure

├── tests/                 
├── pages/                 
├── utils/                 
├── reports/               
├── conftest.py            
├── pytest.ini
├── requirements.txt
├── README.md
├── TEST_PLAN.md
├── TEST_ROADMAP.md
├── TRACEABILITY.md
├── TEST_SUMMARY.md

How to run tests
Install dependencies:
pip install -r requirements.txt

Run all admin panel tests:
pytest tests/admin --html=report.html --self-contained-html

Run a specific module:
pytest tests/test_01_admin_product_management.py

Run with a specific browser:
pytest --browser=edge --html=report.html --self-contained-html

Generate Allure report:
pytest --alluredir=allure-results
allure serve allure-results

Author
George Petre
Portfolio: https://georgempetre.github.io
