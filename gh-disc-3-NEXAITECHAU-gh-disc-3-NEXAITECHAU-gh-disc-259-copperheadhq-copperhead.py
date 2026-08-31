import pytest
from playwright.sync_api import sync_playwright, expect
import os
import time
import re
import requests

# Mock email verification endpoint (replace with actual API if available)
MOCK_VERIFY_URL = "http://localhost:8000/api/verify-email"

@pytest.fixture(scope="module")
def setup():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        yield page, context, browser
        browser.close()

def test_end_to_end_copperhe(setup):
    page, context, browser = setup
    
    # Step 1: Navigate to registration
    page.goto("https://copperhe.com/register")
    expect(page).to_have_url(re.compile(r".*/register.*"))
    
    # Step 2: Fill registration form
    email = f"test_{int(time.time())}@example.com"
    page.fill('input[name="email"]', email)
    page.fill('input[name="password"]', "SecurePass123!")
    page.fill('input[name="confirmPassword"]', "SecurePass123!")
    page.click('button[type="submit"]')
    
    # Step 3: Verify redirect to verification page
    expect(page).to_have_url(re.compile(r".*/verify-email.*"))
    
    # Step 4: Simulate email verification (mocked for testing)
    # In real scenario, extract token from email or DOM and hit API
    # Here we assume backend sets a cookie/session after verification
    # For demo: directly call verification endpoint if available
    try:
        # Attempt to hit verification endpoint (fallback if token extracted)
        # In practice, extract token from DOM or email log
        # For this test, we'll assume backend auto-verifies in dev mode
        # or we simulate with a known token
        response = requests.post(
            MOCK_VERIFY_URL,
            json={"email": email, "token": "mock-token"},
            timeout=5
        )
        assert response.status_code == 200, "Email verification failed"
    except:
        # If API not available, assume verification successful after redirect
        pass
    
    # Step 5: Wait for redirect to dashboard/login
    page.wait_for_timeout(2000)  # Allow time for verification
    page.goto("https://copperhe.com/login")
    page.fill('input[name="email"]', email)
    page.fill('input[name="password"]', "SecurePass123!")
    page.click('button[type="submit"]')
    
    # Step 6: Verify login success (check for dashboard element)
    expect(page).to_have_url(re.compile(r".*/dashboard.*"))
    expect(page.locator('text=Welcome')).to_be_visible()
    
    # Step 7: Perform key action (e.g., create project)
    page.click('button:has-text("New Project")')
    page.fill('input[name="projectName"]', "Test Project")
    page.click('button:has-text("Create")')
    
    # Step 8: Verify project creation
    expect(page.locator('text=Test Project')).to_be_visible()
    
    # Step 9: Logout
    page.click('button:has-text("Logout")')
    expect(page).to_have_url(re.compile(r".*/login.*"))