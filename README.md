OpenCart Automation Testing Project (Admin Panel, UI)


Project Overview
The OpenCart Automation Testing Project (Admin Panel) automates end-to-end validation of administrative features in the OpenCart platform using Selenium WebDriver and PyTest.
This project ensures that all critical admin workflows—such as managing products, processing orders, and updating inventory—function correctly and efficiently.
The framework is designed using the Page Object Model (POM) for maintainability, Soft Assertions for detailed validation, and HTML/Allure reports for traceable execution results.

Objectives
Automate the Admin Panel UI for OpenCart’s key modules.
Validate core administrative operations (add/edit/delete product, order management).
Integrate Soft Assertion logic to capture multiple verifications per test.
Validate functionality across multiple browsers (Chrome, Edge, Firefox).
Generate comprehensive HTML and Allure execution reports for result analysis.


Scope of Automation
Module	Description
Admin Login	Authenticate and verify successful access to the admin dashboard.
Product Management	Add, edit, and delete products using form-based input and file upload.
Order Management	Validate order visibility, filtering, and status updates.
Dashboard Overview	Confirm analytics widgets and navigation links are responsive.
Reports (Future Scope)	Automate sales and product performance report validation.


Project Deliverables
File / Folder	Description
tests/	Modular test suites for product and order management.
pages/	Page Object Model classes defining UI locators and actions.
utils/soft_assert.py	Custom Soft Assertion logic for aggregated verification.
conftest.py	Fixture and WebDriver setup for multi-browser execution.
report.html	PyTest-HTML execution report (all tests passed).
reports/screenshots/	Captured screenshots of executed UI states.


Framework Overview
Language: Python 3.12.6
Test Framework: PyTest 8.3.3
Automation Library: Selenium WebDriver
Assertion Utility: Custom SoftAssert class
Parallel Execution: pytest-xdist 3.6.1
Retries: pytest-rerunfailures 14.0
Reporting: pytest-html 4.0.2, pytest-metadata 3.1.1, Allure 2.13.5
Environment: Windows 11 | OpenCart v4.1.0.3 (Admin Panel via XAMPP)
Java Environment: JDK 21
Supported Browsers:  Chrome |  Edge |  Firefox


Test Execution Summary
Metric	Result
Total Tests	5
Passed	5
Failed	0
Skipped / Errors	0
Execution Time	00:01:20
Report Generated	report.html (pytest-html v4.0.2)


Test Details
Test ID	Description	Status
TestAdminProductManagement::test_add_new_product	Add a new product and verify confirmation message	| Passed
TestAdminProductManagement::test_edit_existing_product	Edit an existing product and validate success alert	| Passed
TestAdminProductManagement::test_delete_product	Delete a product and verify confirmation	| Passed
TestAdminOrderManagement::test_view_customer_order	View existing customer order and confirm details	| Passed
TestAdminOrderManagement::test_update_order_status_to_shipped	Update order status to Shipped and verify confirmation	| Passed


Test Evidence
HTML Report: report.html
Screenshots: Saved in reports/screenshots/ for each module execution.


Key Achievements
Successfully automated Admin Product and Order Management modules.
Achieved 100% pass rate across 5 tests in <2 minutes.
Implemented Page Object Model for reusable and maintainable design.
Generated detailed reports with logs and captured screenshots.
Implemented cross-browser automation supporting Chrome, Edge, and Firefox.

How to Run Tests
Install dependencies
pip install -r requirements.txt

Run all admin panel tests
pytest tests/admin --html=report.html --self-contained-html

Run specific module
pytest tests/test_01_admin_product_management.py

Generate Allure Report
pytest --alluredir=allure-results
allure serve allure-results

Specify a browser (chrome, edge, firefox)
pytest --browser=edge --html=report.html --self-contained-html

Author

George Petre
Sturry, CT2 0HN, UK
george.petre23@gmail.com
georgempetre.github.io

This project demonstrates a robust automation framework for the OpenCart Admin Panel UI, covering product and order workflows with full reporting, reusable design, and adherence to IEEE 829 documentation standards.
