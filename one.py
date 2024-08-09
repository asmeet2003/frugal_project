import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AmazonBot:
    def __init__(self):
        self.service = Service("F:/chromedriver-win64/chromedriver.exe")
        self.driver = webdriver.Chrome(service=self.service)
        self.driver.implicitly_wait(10)  # Adjusted implicit wait

    def add_to_cart(self):
        self.driver.get("https://www.amazon.in/")
        self.driver.maximize_window()

        # Search for mobile
        search_bar = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='twotabsearchtextbox']"))
        )
        search_bar.send_keys("redmi")
        search_bar.send_keys(Keys.ENTER)

        # Sort by Newest Arrivals
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@class='a-dropdown-label']"))
        ).click()
        newest_arrivals = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Newest Arrivals']"))
        )
        newest_arrivals.click()

        # Wait for the list of products to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@data-component-type='s-search-result']"))
        )

        # Click on the first product link and handle the new tab
        first_product = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@data-component-type='s-search-result'][1]//h2/a"))
        )
        first_product.click()

        # Switch to the new tab
        original_window = self.driver.current_window_handle
        WebDriverWait(self.driver, 10).until(
            EC.number_of_windows_to_be(2)
        )
        new_window = [window for window in self.driver.window_handles if window != original_window][0]
        self.driver.switch_to.window(new_window)

        # Wait for the product page to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "add-to-cart-button"))
        )

        # Click "Add to Cart" button
        try:
            add_to_cart_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "add-to-cart-button"))
            )
            add_to_cart_button.click()
            print("Added to cart successfully.")
        except Exception as e:
            print("Error adding item to cart:", e)

        # Handle any additional prompts or actions
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@aria-labelledby='attachSiNoCoverage-announce']"))
            ).click()
        except Exception as e:
            print("Error handling additional prompts:", e)

        # Navigate to the cart
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@id='nav-cart']"))
        ).click()

        # Optionally, add a final wait to ensure everything loads
        time.sleep(5)
        self.driver.quit()

if __name__ == "__main__":
    bot = AmazonBot()
    bot.add_to_cart()
