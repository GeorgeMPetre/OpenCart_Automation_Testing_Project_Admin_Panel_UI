# Test Plan — OpenCart Admin Panel Automated UI Testing

## 1. Objective

Define the scope, strategy, and execution approach for automated UI testing of the
OpenCart Admin Panel.

The goal is to ensure core administrative workflows function correctly and remain
stable through automated regression testing.

---

## 2. Scope

### In scope
- Automated UI validation of:
  - admin login
  - product management (add, edit, delete)
  - order management (view orders, update status)
- Positive and negative scenarios (where applicable)
- Regression-ready automation

### Out of scope
- Storefront (customer UI)
- API testing
- Performance and load testing
- Security testing

---

## 3. Test strategy

- Selenium WebDriver for browser automation
- PyTest as execution framework
- Page Object Model for maintainability
- Tests focus on admin behaviour, not UI implementation details
- Assertions validate:
  - successful navigation
  - visible UI elements
  - confirmation messages and alerts
  - correct data updates
- Known limitations or expected behaviours are handled explicitly

---

## 4. Test environment

- Application: OpenCart (Admin Panel)
- Version: 4.1.0.3
- Environment type: Local (XAMPP)
- Browser automation: WebDriver
- Primary browser: Chrome
- Additional browsers: Edge, Firefox
- Execution: Local machine

Note:
Results from this environment are not production-representative.

---

## 5. Entry criteria

- Admin panel is accessible
- Valid admin credentials are available
- Required test data exists (products and orders)
- Automation environment is configured

---

## 6. Exit criteria

- All planned automated tests are executed
- Failures are reviewed and documented
- Test summary is updated

---

## 7. Deliverables

- Automated test scripts
- Execution results
- HTML and Allure reports
- Screenshots
- Test summary and traceability matrix


## 8. Risks and mitigations

- UI changes may break locators and cause test failures  
  Mitigation: Use Page Object Model and reusable locators to reduce maintenance.

- Timing issues may lead to flaky tests  
  Mitigation: Apply explicit waits and proper synchronisation instead of hard delays.

- Test results may depend on existing data  
  Mitigation: Use controlled test data where possible and document assumptions.

- Local execution does not represent production behaviour  
  Mitigation: Clearly document environment limitations and focus on functional validation.

