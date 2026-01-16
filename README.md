# OpenCart Automation Testing Project (Admin Panel, UI)

This repository contains an automation testing project focused on the OpenCart Admin Panel. I built this framework to automate the most important back-office workflows and to show how I design UI automation that is clear, maintainable, and useful for real teams.

The main goal was to validate that administrators can manage products and orders without issues. Instead of automating everything, I focused on the areas that matter most in daily admin work: logging in, managing products, viewing orders, and updating order statuses.

The automation is written using Selenium WebDriver with PyTest and follows the Page Object Model. Each admin page has its own page class, which keeps locators and actions separate from test logic. This makes the tests easier to read and simpler to maintain when the UI changes.

I also implemented custom soft assertions so each test can verify multiple things in a single run. This helps catch more issues at once and produces more informative test results. Screenshots are captured automatically to support debugging and reporting.

I automated five admin panel test cases covering product management and order management. All tests passed successfully during execution, which confirmed that the tested admin workflows are stable for the current OpenCart setup.

The framework supports running tests across multiple browsers, including Chrome, Edge, and Firefox. Test execution generates a self-contained HTML report, and Allure reports can also be produced for a more visual overview of the results. Screenshots from test execution are stored in the reports folder.

The project structure is simple and intentional. Test cases live in the tests folder, page objects are stored in the pages folder, shared helpers such as the soft assertion utility are in utils, and browser setup is handled through PyTest fixtures in conftest.py.

The project runs on Python 3.12 with PyTest and Selenium WebDriver against OpenCart version 4.1.0.3 running locally on XAMPP. Parallel execution and reruns are supported, although the focus here is correctness and clarity rather than speed.

To run the tests, install the dependencies from requirements.txt and execute pytest with the desired options. You can run the full admin suite, a single test module, generate an HTML report, or launch an Allure report. Browser selection is controlled through a command-line argument.

This project reflects how I approach admin-side automation: automate critical workflows, keep the framework clean, and make test results easy to understand and trust.

Author: George Petre
GitHub: [https://github.com/GeorgeMPetre](https://github.com/GeorgeMPetre)
Portfolio: [https://georgempetre.github.io](https://georgempetre.github.io)
