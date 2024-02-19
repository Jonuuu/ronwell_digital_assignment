# test_trendyol.py
import pytest
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By as by
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class TestTrendyol:

    # Case 1: Verify that all the specified fields are present on the registration page
    def test_fields_on_registration_page(self):
        # Navigate to the registration page
        driver = self.driver
        driver.implicitly_wait(10)
        self.select_country()
        driver.get(self.url + "/login")
        driver.implicitly_wait(10)

        inputs_by_tag = driver.find_elements(by.TAG_NAME, "input")

        input_elements = {}

        for input_element in inputs_by_tag:
            input_id = input_element.get_attribute("id")
            print("Each input: %s", input_id)
            if input_id and "register" in input_id or "checkbox" in input_id:
                variable_name = f"field_{input_id}"
                input_elements[variable_name] = input_element

        for variable_name, input_element in input_elements.items():
            print(f"{variable_name}: {input_element.get_attribute('id')}")
            expected_variable_name = f"field_{input_element.get_attribute('id')}"
            assert variable_name == expected_variable_name

    # Case 2: Verify that not filling the mandatory fields and clicking the submit button will lead to validation error
    def test_validation_error_on_empty_fields(self):
        driver = self.driver
        driver.implicitly_wait(10)
        self.select_country()
        driver.get(self.url + "/login")

        driver.find_element(by.CLASS_NAME, "p-button-wrapper.p-primary.p-large.p-fluid.register-button").click()
        # Check if the validation error message is displayed
        error_message = self.driver.find_element(by.CLASS_NAME, "p-typography-wrapper.p-typography-title.p-typography-semibold.p-typography-semibold.p-primary").text
        print(f"Message displayed after clicking submit button without inputing mendatory fields: {error_message}")
        assert error_message

    # Case 3: Verify that entering blank spaces on mandatory fields leads to validation error
    def test_validation_error_on_blank_spaces(self):
        driver = self.driver
        driver.implicitly_wait(10)
        self.select_country()
        driver.get(self.url + "/login")

        # Enter blank spaces on the mandatory fields
        self.driver.find_element(by.ID, "register-email-input").send_keys(" ")
        self.driver.find_element(by.ID, "register-password-input").send_keys(" ")
        # Click the submit button
        driver.find_element(by.CLASS_NAME, "p-button-wrapper.p-primary.p-large.p-fluid.register-button").click()
        error_message = self.driver.find_element(by.CLASS_NAME, "p-typography-wrapper.p-typography-bodyMedium.p-typography-regular.p-typography-regular.p-primary").text
        print(f"Message displayed after entering blanks spaces in mendatory fields: {error_message}")
        assert error_message

    # Case 4: Verify that the user can add to cart one or more products
    def test_add_to_cart(self):

        self.user_login()
        self.find_products(1)
        wait = WebDriverWait(self.driver, 20)
        if self.driver.find_element(by.CLASS_NAME, "p-onboarding-layout"):
            self.driver.find_element(by.CLASS_NAME, "p-onboarding-layout").click()
        self.driver.find_element(by.ID, "add-to-basket").click()
        wait.until(EC.visibility_of_element_located((by.CLASS_NAME, "p-button-wrapper.p-primary.p-large.success")))
        wait.until(EC.visibility_of_element_located((by.CLASS_NAME, "p-button-wrapper.p-primary.p-large.default")))

        self.find_products(2)
        self.driver.find_element(by.ID, "add-to-basket").click()
        wait.until(EC.visibility_of_element_located((by.CLASS_NAME, "p-button-wrapper.p-primary.p-large.success")))
        wait.until(EC.visibility_of_element_located((by.CLASS_NAME, "p-button-wrapper.p-primary.p-large.default")))

        self.driver.get(self.url + "/cart")
        cart = self.driver.find_element(by.CLASS_NAME, "product-card-list")
        products = cart.find_elements(by.CLASS_NAME, "product-card")

        for product in products:
            print(f"Product added to cart: {product.text}")
        assert cart

    # Case 5: Verify that users can add products to the wishlist(favorites)
    def test_add_to_wishlist(self):
        # Navigate to the home page
        self.user_login()
        self.find_products(1)
        if self.driver.find_element(by.CLASS_NAME, "p-onboarding-layout"):
            self.driver.find_element(by.CLASS_NAME, "p-onboarding-layout").click()
        self.driver.find_element(by.ID, "add-to-favorites").click()

        self.driver.get(self.url + "/account/favorites")

        wish_list = self.driver.find_element(by.CLASS_NAME, "product-cards")
        print(f"Products in the wish list: {wish_list.text}")
        assert wish_list

    # Case 7: Verify that the user can logout successfully
    def test_logout(self):
        # Navigate to the home page
        self.user_login()

        user_icon = self.driver.find_element(by.CLASS_NAME, "user")
        action_chains = ActionChains(self.driver)

        # Hover over the element
        # wait = WebDriverWait(self.driver, 20)

        action_chains.move_to_element(user_icon).perform()
        menu_wrapper = self.driver.find_element(by.CLASS_NAME, "account-menu-wrapper")
        print(menu_wrapper)
        menu_wrapper.find_element(by.CSS_SELECTOR, 'img[alt="by clicking you can log out"]').click()

        user_icon = self.driver.find_element(by.CLASS_NAME, "user")
        action_chains = ActionChains(self.driver)
        action_chains.move_to_element(user_icon).perform()
        sign_out = self.driver.find_element(by.CLASS_NAME, "login-register-wrapper")

        if sign_out:
            print("User succesfully signed out")
        assert sign_out

    # Set up the driver and the URL
    def setup_class(self):
        options = FirefoxOptions()
        options.headless = True  # Example of setting a capability
        driver_path = 'C:/Users/Jona/geckodriver/geckodriver.exe'
        self.driver = webdriver.Firefox(options=options)
        self.url = "https://www.trendyol.com/en"

    # Tear down the driver
    def teardown_class(self):
        self.driver.quit()

    def select_country(self):
        """
        Method used for selecting country
        """
        self.driver.get(self.url)
        self.driver.find_element(by.XPATH, "//div[@class='country-selection__content']//select//option[@value='GB']").click()
        self.driver.implicitly_wait(10)
        self.driver.find_element(by.CLASS_NAME, "country-actions").click()

    def user_login(self):
        """
        Method for logging in
        """
        self.driver.implicitly_wait(10)
        self.select_country()
        self.driver.find_element(by.CSS_SELECTOR,"#onetrust-reject-all-handler").click()
        self.driver.get(self.url + "/login")
        self.driver.find_element(by.ID, "login-password-input").send_keys("test123")
        self.driver.find_element(by.ID, "login-email-input").send_keys("jona@test.com")

        wait = WebDriverWait(self.driver, 5)
        wait.until(EC.element_to_be_clickable((by.CLASS_NAME, "p-button-wrapper.p-primary.p-large.p-fluid.login-button"))).click()
        wait.until(EC.invisibility_of_element_located((by.CLASS_NAME, "poseidon-loader-container")))
        print("Logged in.")

    def find_products(self, number, sub_url="/women-jean-x-g1-c120"):

        self.driver.get(self.url + sub_url) 
        self.driver.find_element(by.CSS_SELECTOR, f'[data-productorder="{number}"]').click()
