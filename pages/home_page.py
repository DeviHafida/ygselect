from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage

class HomePage(BasePage):
    
    # LOCATOR YANG BENAR (berdasarkan debug)
    SEARCH_INPUT = (By.NAME, "keyword")  # name=keyword
    SEARCH_BTN = (By.CLASS_NAME, "search_cont")  # class=search_cont
    CART_ICON = (By.CLASS_NAME, "ico_cart")  # class=ico_cart
    MENU_LOGIN = (By.LINK_TEXT, "LOGIN")
    MENU_JOIN = (By.LINK_TEXT, "JOIN")
    MENU_ARTIST = (By.LINK_TEXT, "ARTIST")
    MENU_CATEGORY = (By.LINK_TEXT, "CATEGORY")
    MENU_EVENT = (By.XPATH, "//a[contains(text(), 'EVENT')]")
    MENU_NEWS = (By.XPATH, "//a[contains(text(), 'NEWS')]")
    MENU_STORY = (By.XPATH, "//a[contains(text(), 'STORY')]")
    LANGUAGE_DROPDOWN = (By.XPATH, "//select[contains(@id, 'lang')]")
    
    def open_homepage(self):
        self.open("https://en.ygselect.com/index.html")
    
    def click_logo(self):
        try:
            logo = (By.XPATH, "//h1/a | //div[@class='logo']/a")
            self.click(logo)
        except:
            pass
    
    def click_join_us(self):
        self.click(self.MENU_JOIN)
    
    def click_login(self):
        self.click(self.MENU_LOGIN)
    
    def search_product(self, keyword):
        self.type_text(self.SEARCH_INPUT, keyword)
        # Submit dengan Enter
        search_input = self.find_element(self.SEARCH_INPUT)
        search_input.submit()
    
    def select_language(self, language_code):
        lang_dropdown = self.find_element(self.LANGUAGE_DROPDOWN)
        select = Select(lang_dropdown)
        select.select_by_value(language_code)
    
    def click_cart(self):
        self.click(self.CART_ICON)
    
    def click_bot(self):
        try:
            bot = (By.XPATH, "//*[contains(@class, 'bot')]")
            self.click(bot)
        except:
            pass
    
    def click_menu_artist(self):
        self.click(self.MENU_ARTIST)
    
    def click_menu_category(self):
        self.click(self.MENU_CATEGORY)
    
    def click_menu_event(self):
        self.click(self.MENU_EVENT)
    
    def click_menu_news(self):
        self.click(self.MENU_NEWS)
    
    def click_menu_story(self):
        self.click(self.MENU_STORY)
    
    def click_all_products(self):
        try:
            all_products = (By.XPATH, "//a[contains(text(), '전체상품')]")
            self.click(all_products)
        except:
            pass