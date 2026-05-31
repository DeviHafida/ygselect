from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):

    CART_ITEMS = (
        By.XPATH,
        "//*[contains(@class,'cart')]//*[contains(@class,'item')]"
    )

    DELETE_BTN = (
        By.XPATH,
        "//button[contains(@class,'delete')] | //a[contains(@class,'delete')]"
    )

    CHECKOUT_BTN = (
        By.XPATH,
        "//button[contains(.,'Checkout')] | //a[contains(.,'Checkout')]"
    )

    QUANTITY_INPUT = (
        By.XPATH,
        "//input[@type='number']"
    )

    def get_cart_item_count(self):
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def click_delete_first_item(self):
        buttons = self.driver.find_elements(*self.DELETE_BTN)

        if buttons:
            buttons[0].click()

    def update_quantity(self, index, quantity):
        inputs = self.driver.find_elements(*self.QUANTITY_INPUT)

        if index < len(inputs):
            inputs[index].clear()
            inputs[index].send_keys(str(quantity))

    def click_checkout(self):
        self.click(self.CHECKOUT_BTN)

    def is_cart_empty(self):
        page = self.driver.page_source.lower()

        keywords = [
            "cart is empty",
            "empty cart",
            "장바구니가 비어"
        ]

        return any(word in page for word in keywords)