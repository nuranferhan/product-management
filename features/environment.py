import os
from behave import fixture
from selenium import webdriver


def before_all(context):
    """Executed once before all tests"""
    context.BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')
    
    # Setup Selenium WebDriver (optional for web UI testing)
    # context.driver = webdriver.Chrome()
    # context.driver.implicitly_wait(30)
    # context.driver.set_window_size(1200, 600)


def after_all(context):
    """Executed after all tests"""
    # Clean up WebDriver if used
    # if hasattr(context, 'driver'):
    #     context.driver.quit()
    pass