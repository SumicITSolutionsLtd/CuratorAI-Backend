# Testing Guide - CuratorAI Backend

This guide explains how to run and use the test suite for the CuratorAI backend API.

## Quick Start

### Run All Tests

**Linux/Mac:**
```bash
./scripts/run_tests.sh
```

**Windows:**
```cmd
scripts\run_tests.bat
```

**Or directly with pytest:**
```bash
pytest apps/
```

### Access Test Dashboard

1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. Open your browser and navigate to:
   ```
   http://localhost:8000/test-dashboard/
   ```

3. Use the dashboard to:
   - Run all tests with one click
   - Run tests for specific modules
   - Run individual tests
   - View test results and coverage

## Test Structure

Tests are organized by app in the `apps/` directory:

```
apps/
├── accounts/
│   └── tests/
│       └── test_authentication.py
├── social/
│   └── tests/
│       └── test_social_feed.py
├── lookbooks/
│   └── tests/
│       └── test_lookbooks.py
└── ...
```

## Running Tests

### Command Line Options

**Run all tests:**
```bash
pytest apps/
```

**Run tests for a specific app:**
```bash
pytest apps/accounts/tests/
pytest apps/social/tests/
```

**Run a specific test file:**
```bash
pytest apps/accounts/tests/test_authentication.py
```

**Run a specific test:**
```bash
pytest apps/accounts/tests/test_authentication.py::TestRegistration::test_register_success
```

**Run with coverage:**
```bash
pytest apps/ --cov=apps --cov-report=html
```

**Run with verbose output:**
```bash
pytest apps/ -v
```

**Run and stop on first failure:**
```bash
pytest apps/ -x
```

## Test Coverage

Generate coverage reports:

```bash
pytest apps/ --cov=apps --cov-report=html --cov-report=term
```

Coverage reports will be generated in:
- **HTML**: `htmlcov/index.html` (open in browser)
- **Terminal**: Displayed in console
- **JSON**: `coverage.json`

## Test Dashboard Features

The test dashboard (`/test-dashboard/`) provides:

1. **Run All Tests** - Execute the entire test suite
2. **Run Module Tests** - Test specific app modules
3. **Run Individual Tests** - Test specific test files
4. **View Results** - See detailed test output
5. **Test Status** - Visual indicators for pass/fail
6. **Summary Statistics** - Pass/fail/skip counts

## Writing New Tests

### Test File Structure

```python
import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

@pytest.fixture
def api_client():
    """Create API client."""
    return APIClient()

@pytest.fixture
def user():
    """Create test user."""
    return User.objects.create_user(
        email='test@example.com',
        username='testuser',
        password='testpass123'
    )

@pytest.fixture
def authenticated_client(api_client, user):
    """Create authenticated API client."""
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return api_client

@pytest.mark.django_db
class TestMyEndpoint:
    """Test my endpoint."""
    
    def test_endpoint_success(self, authenticated_client):
        """Test successful request."""
        url = '/api/v1/my-endpoint/'
        response = authenticated_client.get(url)
        assert response.status_code == status.HTTP_200_OK
```

### Best Practices

1. **Use fixtures** for common setup (users, clients, etc.)
2. **Use descriptive test names** that explain what is being tested
3. **Test both success and failure cases**
4. **Use `@pytest.mark.django_db`** for tests that need database access
5. **Assert specific status codes** and response data
6. **Clean up test data** (Django test database is isolated by default)

## Continuous Integration

Tests can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Run tests
  run: |
    pip install -r requirements/development.txt
    pytest apps/ --cov=apps --cov-report=xml
```

## Troubleshooting

### Tests fail with database errors

Make sure migrations are up to date:
```bash
python manage.py migrate
```

### Tests fail with import errors

Make sure all dependencies are installed:
```bash
pip install -r requirements/development.txt
```

### Test dashboard not loading

1. Check that `apps.test_dashboard` is in `INSTALLED_APPS`
2. Verify the URL is included in `curator/urls.py`
3. Check server logs for errors

### Google OAuth tests failing

Google OAuth tests require valid tokens. These tests are marked with `@pytest.mark.skip` by default. To test OAuth:

1. Get a valid Google OAuth token
2. Remove the `@pytest.mark.skip` decorator
3. Update the test with a valid token

## Test Endpoints Coverage

Current test coverage includes:

- ✅ Authentication endpoints (register, login, refresh, OAuth)
- ✅ Social feed endpoints (feed, posts, likes, comments)
- ✅ Lookbooks endpoints (list, detail, create, like)
- ⚠️ Other endpoints (wardrobe, outfits, cart, notifications) - tests can be added

## Next Steps

1. Add more test coverage for remaining endpoints
2. Add integration tests for complex workflows
3. Add performance tests for high-traffic endpoints
4. Set up automated test runs in CI/CD

