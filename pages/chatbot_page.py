from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class ChatbotPage(BasePage):
    # Locators
    CHAT_INPUT = (By.CSS_SELECTOR, ".chat-input")
    SEND_BTN = (By.CSS_SELECTOR, ".send-btn")
    CHAT_MESSAGES = (By.CSS_SELECTOR, ".chat-message")
    ERROR_MSG = (By.CSS_SELECTOR, ".error-message")
    
    def send_message(self, message):
        self.type_text(self.CHAT_INPUT, message)
        self.click(self.SEND_BTN)
    
    def get_last_response(self):
        messages = self.find_elements(self.CHAT_MESSAGES)
        return messages[-1].text if messages else ""