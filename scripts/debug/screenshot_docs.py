#!/usr/bin/env python3
"""
Screenshot utility for documentation analysis.
"""
import sys
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def take_screenshot(url: str, output_path: str, theme: str = "auto"):
    """Take a screenshot of a documentation page.

    Args:
        url: URL to screenshot
        output_path: Path to save screenshot
        theme: Theme to use (light, dark, auto)
    """
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        print(f"Loading {url}...")
        driver.get(url)

        # Wait for page to load
        time.sleep(2)

        # Set theme if specified
        if theme in ["light", "dark"]:
            try:
                # Look for theme toggle button
                theme_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-theme-toggle]"))
                )

                current_theme = driver.execute_script(
                    "return document.documentElement.getAttribute('data-theme')"
                )

                if current_theme != theme:
                    theme_button.click()
                    time.sleep(1)

            except Exception as e:
                print(f"Could not set theme to {theme}: {e}")

        # Take screenshot
        print(f"Taking screenshot...")
        driver.save_screenshot(output_path)
        print(f"✅ Screenshot saved to {output_path}")

        # Return current theme for analysis
        current_theme = driver.execute_script(
            "return document.documentElement.getAttribute('data-theme')"
        )
        return current_theme

    finally:
        driver.quit()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python screenshot_docs.py <url> <output_path> [theme]")
        sys.exit(1)

    url = sys.argv[1]
    output_path = sys.argv[2]
    theme = sys.argv[3] if len(sys.argv) > 3 else "auto"

    # Create output directory
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    current_theme = take_screenshot(url, output_path, theme)
    print(f"Current theme: {current_theme}")
