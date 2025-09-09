# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### 🚀 Features

#### Authentication & User Management
- **feat(base_page)**: add user authorization check method to base page
- **feat(login_page)**: implement user registration method in login page
- **feat(product_page)**: add explicit wait for success messages in product page

#### Navigation & Basket
- **feat(navigation)**: implement basket page access from header
- **feat(basket)**: add basket page with empty basket assertions
- **feat**: add go_to_basket_from_header method with debugging decorators and explicit waiting

#### Internationalization
- **feat(i18n)**: add multilingual support for basket empty state messages including en, ru, fi translations
- **feat**: add automatic language detection with fallback to English

#### Infrastructure
- **feat(config)**: major infrastructure improvements including:
  - Automatic headed mode detection for marked tests
  - Comprehensive URL fixtures with language support
  - Problematic URLs testing fixtures
  - Enhanced test configuration
- **feat**: implement known issues tracking system with automated regression tests
- **feat**: add problematic URLs registry with severity categorization

### 🐛 Fixes

- **fix(locators)**: implement explicit waiting for login link detection
- **fix**: enhance basket empty detection reliability in headless mode

### 🔧 Refactor

#### Architecture
- **refactor(architecture)**: move basket method to base page for reuse
- **refactor(architecture)**: move login methods to base page for reuse
- **refactor(urls)**: update PRODUCT_PAGE_URL

#### Locators
- **refactor(locators)**: import BASKET_LINK_IN_HEADER from BasePageLocators
- **refactor(locators)**: move basket header locator to BasePageLocators
- **refactor(locators)**: add registration link locator
- **refactor(locators)**: relocate LOGIN_LINK from MainPageLocators to BasePageLocators
- **refactor**: improve URL localization with better language code handling

#### Tests
- **refactor**: consolidate login tests into TestLoginFromMainPage class
- **refactor**: consolidate locators for better maintainability

### 📚 Documentation

- **docs(page-objects)**: comprehensive documentation update with type hints and docstrings
- **docs(all-modules)**: add comprehensive documentation update with type hints and docstrings
- **docs**: add detailed docstrings for login methods
- **docs(changelog)**: add changelog file
- **docs**: update changelog

### ✅ Tests

#### Test Infrastructure
- **test(user_registration)**: add auto-registration fixture for product page tests
- **test(TestUserAddToBasketFromProductPage)**: add parametrized tests for user basket functionality
- **test(main-page)**: create TestLoginFromMainPage class for login link checks
- **test(basket)**: enhance empty basket message check to verify element has content
- **test(basket)**: verify empty basket when opened from product page
- **test(basket)**: add empty basket test from main page
- **test(tests)**: add login tests for product page
- **test(ui)**: Add empty basket verification test requiring headed mode
- **test(ui)**: Add headed test for empty basket verification
- **test(config)**: add headed marker to distinguish UI tests requiring visual browser

#### Test Cases
- **test**: Add test_guest_should_see_login_link_on_product_page
- **test**: Add test_guest_can_go_to_login_page_from_product_page
- **test**: Add TestProductPage tests test_guest_can_add_product_to_basket

### 🏗️ Chore

- **Chore**: move all tests to 'tests' folder. Modify folders to python packages. Prepare documentation.
- Add login_guest marker for related tests
- Enhance base page with robust element checking and alert handling
- Implement robust message absence and disappearance validations
- Add negative test cases with expected failures
- Refactor code style and add test URLs
- Add utility methods to base page
- Add product page tests with basket functionality
- Add go_to_login_page() method and navigation test
- Add LoginPage class with authentication form checks and tests
- Add login link test with parametrize and page object pattern
- Configure pytest markers for test suite organization
- Add project structure with requirements and main page test
- [fix] Add main_page_url as parameter in test_guest_can_go_to_login_page

## [1.0.0] - 2024-01-15

### Initial Release

- Initial project setup and structure
- Base Page Object model implementation
- Core test infrastructure
- Basic test cases setup

---

*This CHANGELOG was automatically generated based on git history*