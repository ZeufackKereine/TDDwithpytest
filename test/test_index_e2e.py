import unittest
from selenium import webdriver
from selenium.webdriver.edge.service import Service
import multiprocessing
from app import app  # Import your Flask app
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def run_flask():
    app.run(port=5000)

class E2ETests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Start Flask server in a separate process
        cls.flask_process = multiprocessing.Process(target=run_flask)
        cls.flask_process.start()
        time.sleep(4)  # Give the server a second to ensure it's running
        
        # Setup Selenium WebDriver
        service = Service(r'C:\Users\HP\Downloads\edgedriver_win64\msedgedriver.exe')
        cls.driver = webdriver.Edge(service=service)

    @classmethod
    def tearDownClass(cls):
     time.sleep(30)  # Keep the browser open for 30 seconds
     cls.driver.quit()
     cls.flask_process.terminate()
     cls.flask_process.join()
    
    def test_browser_title_contains_app_name(self):
        self.driver.get('http://localhost:5000')
        self.assertIn('Named Entity', self.driver.title)

    def test_page_heading_is_named_entity_finder(self):
        heading = self._find("app-title").text
        self.assertEqual('Named Entity Finder', heading)

    def test_page_has_input_for_text(self):
        input_element = self._find('input-text')
        self.assertIsNotNone(input_element)

    def test_page_has_button_for_submitting_text(self):
        submit_button = self._find('find-button')
        self.assertIsNotNone(submit_button)

    def test_page_has_ner_table(self):
        input_element = self._find('input-text')
        submit_button = self._find('find-button')
        input_element.send_keys('France and Germany share a border in Europe')
        submit_button.click()
        table = self._find('ner-table')
        self.assertIsNotNone(table)

    def _find(self, id):
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, id))
            )
        except Exception as e:
            self.driver.save_screenshot(f"error_{id}.png")
            raise e  # Raise the caught exception explicitly

    def prompt_user(self):
        input("Press Enter to close the browser...")

if __name__ == '__main__':
    unittest.main()

    # Add this line if you want the prompt to appear after all tests are done
    E2ETests.prompt_user(E2ETests)