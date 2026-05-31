from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ProductPage(BasePage):

    ADD_TO_CART_BTN = (
        By.XPATH,
        "//button[contains(.,'Add to Cart')] | //a[contains(.,'Add to Cart')] | //button[contains(@class,'cart')]"
    )

    QUANTITY_INPUT = (
        By.XPATH,
        "//input[@type='number'] | //input[contains(@name,'qty')]"
    )

    PRODUCT_TITLE = (
        By.XPATH,
        "//h2 | //h3 | //div[contains(@class,'title')]"
    )

    PRODUCT_PRICE = (
        By.XPATH,
        "//*[contains(@class,'price')]"
    )

    WISHLIST_BTN = (
        By.XPATH,
        "//*[contains(@class,'wish')] | //*[contains(@class,'like')]"
    )

    def click_add_to_cart(self):
        self.click(self.ADD_TO_CART_BTN)

    def set_quantity(self, quantity):
        qty = self.find_element(self.QUANTITY_INPUT)
        qty.clear()
        qty.send_keys(str(quantity))

    def click_wishlist(self):
        self.click(self.WISHLIST_BTN)

    def get_product_title(self):
        return self.get_text(self.PRODUCT_TITLE)

    def get_product_price(self):
        return self.get_text(self.PRODUCT_PRICE)