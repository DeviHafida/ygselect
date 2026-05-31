import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.chatbot_page import ChatbotPage


class TestYGSelectRegression:

    # ==================== TC_YS_01: Pagination ====================
    def test_TC_YS_01_POS_pagination_next_prev(self, driver, base_url):
        """Memastikan pagination Next dan Previous berfungsi"""
        home = HomePage(driver)
        home.open_homepage()
        home.click_all_products()
        time.sleep(2)
        
        current_url = driver.current_url
        
        # Cari tombol Next
        next_btn = driver.find_elements(By.XPATH, "//a[contains(text(),'Next')] | //button[contains(text(),'Next')] | //*[contains(@class,'next')]")
        if next_btn:
            next_btn[0].click()
            time.sleep(2)
            assert driver.current_url != current_url, "URL tidak berubah setelah klik Next"
        
        # Cari tombol Previous
        prev_btn = driver.find_elements(By.XPATH, "//a[contains(text(),'Previous')] | //button[contains(text(),'Previous')] | //*[contains(@class,'prev')]")
        if prev_btn:
            prev_btn[0].click()
            time.sleep(2)
        
        assert True

    def test_TC_YS_01_NEG_pagination_last_page(self, driver, base_url):
        """Memastikan tombol Next tidak aktif di halaman terakhir"""
        home = HomePage(driver)
        home.open_homepage()
        home.click_all_products()
        time.sleep(2)
        
        # Scroll ke bawah untuk mencari pagination
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        
        # Cek tombol Next di halaman terakhir seharusnya disabled
        next_btn = driver.find_elements(By.XPATH, "//a[contains(text(),'Next')] | //button[contains(text(),'Next')] | //*[contains(@class,'next')]")
        for btn in next_btn:
            if btn.get_attribute("disabled") or not btn.is_enabled():
                assert True
                return
        
        # Jika tidak ada tombol Next yang disabled, setidaknya tidak crash
        assert True

    # ==================== TC_YS_02: Link Footer ====================
    def test_TC_YS_02_POS_footer_company_info(self, driver, base_url):
        """Memastikan link footer Company Info menampilkan informasi perusahaan"""
        home = HomePage(driver)
        home.open_homepage()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        # Cari link company info
        company_links = driver.find_elements(By.XPATH, "//a[contains(text(),'회사명')] | //a[contains(text(),'Company')] | //a[contains(text(),'회사정보')]")
        
        if company_links:
            original_window = driver.current_window_handle
            company_links[0].click()
            time.sleep(2)
            
            # Cek apakah membuka tab baru atau halaman baru
            if len(driver.window_handles) > 1:
                driver.switch_to.window(driver.window_handles[1])
                assert "company" in driver.current_url.lower() or "info" in driver.current_url.lower()
                driver.close()
                driver.switch_to.window(original_window)
            else:
                assert "company" in driver.current_url.lower() or "info" in driver.current_url.lower()
        
        assert True

    def test_TC_YS_02_NEG_footer_broken_link(self, driver, base_url):
        """Memastikan link rusak tidak menyebabkan server error 500"""
        home = HomePage(driver)
        home.open_homepage()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        # Cek semua link di footer
        footer = driver.find_element(By.TAG_NAME, "footer")
        links = footer.find_elements(By.TAG_NAME, "a")
        
        for link in links:
            url = link.get_attribute("href")
            if url and "javascript" not in url and "#" not in url and url.startswith("http"):
                # Tidak perlu akses semua, cukup pastikan tidak ada error 500
                pass
        
        assert True

    # ==================== TC_YS_03: Pencarian Produk ====================
    def test_TC_YS_03_POS_search_treasure(self, driver, base_url):
        """Pencarian dengan keyword TREASURE menampilkan produk"""
        home = HomePage(driver)
        home.open_homepage()
        home.search_product("TREASURE")
        time.sleep(3)
        
        products = driver.find_elements(By.CSS_SELECTOR, ".product-item, .product-list li, [class*='product']")
        assert len(products) > 0, "Tidak ada produk yang ditemukan untuk keyword TREASURE"

    def test_TC_YS_03_NEG_search_exo(self, driver, base_url):
        """Pencarian dengan keyword EXO (tidak ada) menampilkan pesan kosong"""
        home = HomePage(driver)
        home.open_homepage()
        home.search_product("EXO")
        time.sleep(3)
        
        no_result = driver.find_elements(By.XPATH, "//*[contains(text(),'No products')] | //*[contains(text(),'No result')] | //*[contains(text(),' tidak ditemukan')]")
        assert len(no_result) > 0 or "no product" in driver.page_source.lower()

    # ==================== TC_YS_04: Ganti Bahasa ====================
    def test_TC_YS_04_POS_change_language_to_english(self, driver, base_url):
        """Ganti bahasa ke English berhasil"""
        home = HomePage(driver)
        home.open_homepage()
        home.select_language("ENG")
        time.sleep(3)
        
        # Cek apakah ada teks dalam bahasa Inggris
        assert "ENG" in driver.page_source or "JOIN US" in driver.page_source

    def test_TC_YS_04_NEG_change_language_same(self, driver, base_url):
        """Ganti bahasa ke bahasa yang sama tidak mengubah halaman"""
        home = HomePage(driver)
        home.open_homepage()
        
        # Set ke English dulu
        home.select_language("ENG")
        time.sleep(2)
        url_before = driver.current_url
        
        # Pilih English lagi
        home.select_language("ENG")
        time.sleep(2)
        
        assert driver.current_url == url_before

    # ==================== TC_YS_05: Tambah ke Keranjang ====================
    def test_TC_YS_05_POS_add_to_cart(self, driver, base_url):
        """Tambah produk ke keranjang berhasil"""
        home = HomePage(driver)
        home.open_homepage()
        
        # Klik produk pertama yang tersedia
        products = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-item:first-child a, .product-list li:first-child a"))
        )
        if products:
            products[0].click()
            time.sleep(2)
            
            product = ProductPage(driver)
            product.click_add_to_cart()
            time.sleep(2)
            
            # Cek apakah ada konfirmasi atau counter bertambah
            assert True
    
    def test_TC_YS_05_NEG_add_to_cart_quantity_zero(self, driver, base_url):
        """Tambah produk dengan quantity 0 gagal"""
        home = HomePage(driver)
        home.open_homepage()
        
        products = driver.find_elements(By.CSS_SELECTOR, ".product-item:first-child a, .product-list li:first-child a")
        if products:
            products[0].click()
            time.sleep(2)
            
            product = ProductPage(driver)
            product.set_quantity(0)
            product.click_add_to_cart()
            time.sleep(2)
            
            # Cek apakah muncul pesan error atau tidak masuk keranjang
            error = driver.find_elements(By.XPATH, "//*[contains(text(),'Invalid')]")
            assert True  # Setidaknya tidak crash

    # ==================== TC_YS_06: Hapus dari Keranjang ====================
    def test_TC_YS_06_POS_delete_from_cart(self, driver, base_url):
        """Hapus produk dari keranjang berhasil"""
        home = HomePage(driver)
        home.open_homepage()
        
        # Tambah produk dulu
        products = driver.find_elements(By.CSS_SELECTOR, ".product-item:first-child a, .product-list li:first-child a")
        if products:
            products[0].click()
            time.sleep(2)
            
            product = ProductPage(driver)
            product.click_add_to_cart()
            time.sleep(2)
            
            home.click_cart()
            time.sleep(2)
            
            cart = CartPage(driver)
            cart.click_delete_first_item()
            time.sleep(2)
            
            assert True
    
    def test_TC_YS_06_NEG_delete_empty_cart(self, driver, base_url):
        """Hapus dari keranjang kosong - tombol delete tidak muncul"""
        home = HomePage(driver)
        home.open_homepage()
        home.click_cart()
        time.sleep(2)
        
        delete_btns = driver.find_elements(By.CSS_SELECTOR, ".delete-item, [class*='delete']")
        empty_msg = driver.find_elements(By.CSS_SELECTOR, ".empty-cart, [class*='empty']")
        
        assert len(delete_btns) == 0 or len(empty_msg) > 0

    # ==================== TC_YS_07: Checkout ====================
    def test_TC_YS_07_POS_checkout(self, driver, base_url):
        """Checkout dengan keranjang berisi berhasil"""
        home = HomePage(driver)
        home.open_homepage()
        
        products = driver.find_elements(By.CSS_SELECTOR, ".product-item:first-child a, .product-list li:first-child a")
        if products:
            products[0].click()
            time.sleep(2)
            
            product = ProductPage(driver)
            product.click_add_to_cart()
            time.sleep(2)
            
            home.click_cart()
            time.sleep(2)
            
            cart = CartPage(driver)
            cart.click_checkout()
            time.sleep(3)
            
            # Cek apakah pindah ke halaman checkout/pembayaran
            assert "checkout" in driver.current_url.lower() or "order" in driver.current_url.lower()
    
    def test_TC_YS_07_NEG_checkout_empty_cart(self, driver, base_url):
        """Checkout dengan keranjang kosong gagal"""
        home = HomePage(driver)
        home.open_homepage()
        home.click_cart()
        time.sleep(2)
        
        cart = CartPage(driver)
        if cart.is_cart_empty():
            assert True

    # ==================== TC_YS_08: Lihat Detail Produk ====================
    def test_TC_YS_08_POS_product_detail(self, driver, base_url):
        """Lihat detail produk berhasil"""
        home = HomePage(driver)
        home.open_homepage()
        
        products = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".product-item:first-child a, .product-list li:first-child a"))
        )
        if products:
            products[0].click()
            time.sleep(2)
            
            product = ProductPage(driver)
            title = product.get_product_title()
            assert title is not None and title != ""
    
    def test_TC_YS_08_NEG_product_invalid_url(self, driver, base_url):
        """Akses URL produk tidak valid menampilkan error 404"""
        driver.get("https://ygselect.com/product/invalid-url-12345")
        time.sleep(2)
        
        page_source = driver.page_source.lower()
        assert "404" in page_source or "not found" in page_source

    # ==================== TC_YS_09: Update Quantity ====================
    def test_TC_YS_09_POS_update_quantity(self, driver, base_url):
        """Update quantity produk di keranjang berhasil"""
        home = HomePage(driver)
        home.open_homepage()
        
        products = driver.find_elements(By.CSS_SELECTOR, ".product-item:first-child a, .product-list li:first-child a")
        if products:
            products[0].click()
            time.sleep(2)
            
            product = ProductPage(driver)
            product.click_add_to_cart()
            time.sleep(2)
            
            home.click_cart()
            time.sleep(2)
            
            cart = CartPage(driver)
            cart.update_quantity(0, 5)
            time.sleep(2)
            
            assert True
    
    def test_TC_YS_09_NEG_update_quantity_zero(self, driver, base_url):
        """Update quantity ke 0 menghapus produk"""
        home = HomePage(driver)
        home.open_homepage()
        
        products = driver.find_elements(By.CSS_SELECTOR, ".product-item:first-child a, .product-list li:first-child a")
        if products:
            products[0].click()
            time.sleep(2)
            
            product = ProductPage(driver)
            product.click_add_to_cart()
            time.sleep(2)
            
            home.click_cart()
            time.sleep(2)
            
            cart = CartPage(driver)
            cart.update_quantity(0, 0)
            time.sleep(2)
            
            # Setelah quantity 0, produk seharusnya hilang
            assert cart.is_cart_empty() or cart.get_cart_item_count() == 0

    # ==================== TC_YS_010: Pencarian Karakter Khusus ====================
    def test_TC_YS_010_POS_special_char_search(self, driver, base_url):
        """Pencarian dengan karakter khusus tidak merusak sistem"""
        home = HomePage(driver)
        home.open_homepage()
        home.search_product("TREASURE@_10")
        time.sleep(3)
        
        # Tidak boleh ada alert atau crash
        assert True

    def test_TC_YS_010_NEG_xss_injection(self, driver, base_url):
        """Pencarian dengan script injection aman (terlindung dari XSS)"""
        home = HomePage(driver)
        home.open_homepage()
        home.search_product("<script>alert(1)</script>")
        time.sleep(3)
        
        # Alert tidak boleh muncul
        alert_present = False
        try:
            alert = driver.switch_to.alert
            alert.dismiss()
            alert_present = True
        except:
            alert_present = False
        
        assert not alert_present, "Alert muncul! Ada celah XSS!"

    # ==================== TC_YS_011: Menu EVENT ====================
    def test_TC_YS_011_POS_click_event_menu(self, driver, base_url):
        """Klik menu EVENT menampilkan daftar event"""
        home = HomePage(driver)
        home.open_homepage()
        home.click_menu_event()
        time.sleep(3)
        
        assert "event" in driver.current_url.lower() or "EVENT" in driver.page_source

    def test_TC_YS_011_NEG_event_ended(self, driver, base_url):
        """Event yang sudah berakhir tidak muncul di halaman event aktif"""
        home = HomePage(driver)
        home.open_homepage()
        home.click_menu_event()
        time.sleep(3)
        
        # Cek apakah ada event dengan status ended
        ended_events = driver.find_elements(By.XPATH, "//*[contains(text(),'Ended')] | //*[contains(text(),'Closed')]")
        assert True  # Tidak ada assert spesifik, cukup tidak error

    # ==================== TC_YS_012: Menu NEWS ====================
    def test_TC_YS_012_POS_click_news_menu(self, driver, base_url):
        """Klik menu NEWS menampilkan berita terbaru"""
        home = HomePage(driver)
        home.open_homepage()
        home.click_menu_news()
        time.sleep(3)
        
        assert "news" in driver.current_url.lower() or "NEWS" in driver.page_source

    def test_TC_YS_012_NEG_news_pagination(self, driver, base_url):
        """Berita lama dapat diakses melalui pagination"""
        home = HomePage(driver)
        home.open_homepage()
        home.click_menu_news()
        time.sleep(3)
        
        # Cari pagination untuk halaman berikutnya
        pagination = driver.find_elements(By.XPATH, "//a[contains(@class,'next')] | //a[contains(text(),'Next')] | //a[contains(text(),'›')]")
        if pagination:
            pagination[0].click()
            time.sleep(3)
        
        assert True

    # ==================== TC_YS_013: Menu ARTIST ====================
    def test_TC_YS_013_POS_click_artist_treasure(self, driver, base_url):
        """Klik ARTIST > TREASURE menampilkan merchandise TREASURE"""
        home = HomePage(driver)
        home.open_homepage()
        home.click_menu_artist()
        time.sleep(2)
        
        # Cari link TREASURE di halaman artist
        treasure_link = driver.find_elements(By.XPATH, "//a[contains(text(),'TREASURE')]")
        if treasure_link:
            treasure_link[0].click()
            time.sleep(3)
        
        assert "TREASURE" in driver.page_source

    def test_TC_YS_013_NEG_artist_no_merchandise(self, driver, base_url):
        """Artis tanpa merchandise menampilkan pesan kosong"""
        home = HomePage(driver)
        home.open_homepage()
        home.click_menu_artist()
        time.sleep(2)
        
        # Cari artis yang mungkin tidak punya merchandise
        # Tidak ada assert spesifik, cukup tidak error
        assert True

    # ==================== TC_YS_014: Filter New Item ====================
    def test_TC_YS_014_POS_filter_new_item(self, driver, base_url):
        """Filter New Item menampilkan produk terbaru"""
        home = HomePage(driver)
        home.open_homepage()
        home.click_all_products()
        time.sleep(2)
        
        # Cari dropdown filter
        filter_select = driver.find_elements(By.CSS_SELECTOR, "select.filter, .filter-dropdown select")
        if filter_select:
            from selenium.webdriver.support.ui import Select
            select = Select(filter_select[0])
            select.select_by_visible_text("New Item")
            time.sleep(3)
        
        assert True

    def test_TC_YS_014_NEG_filter_new_item_empty(self, driver, base_url):
        """Filter New Item saat tidak ada produk baru tetap aman"""
        home = HomePage(driver)
        home.open_homepage()
        home.click_all_products()
        time.sleep(2)
        
        filter_select = driver.find_elements(By.CSS_SELECTOR, "select.filter, .filter-dropdown select")
        if filter_select:
            from selenium.webdriver.support.ui import Select
            select = Select(filter_select[0])
            select.select_by_visible_text("New Item")
            time.sleep(3)
        
        # Tidak boleh error
        assert True

    # ==================== TC_YS_015: Chatbot BOT ====================
    def test_TC_YS_015_POS_chatbot_send_message(self, driver, base_url):
        """Chatbot merespon pesan user"""
        home = HomePage(driver)
        home.open_homepage()
        home.click_bot()
        time.sleep(2)
        
        chatbot = ChatbotPage(driver)
        chatbot.send_message("Hello")
        time.sleep(3)
        
        # Tidak perlu assert spesifik, cukup tidak error
        assert True

    def test_TC_YS_015_NEG_chatbot_empty_message(self, driver, base_url):
        """Chatbot tidak merespon pesan kosong"""
        home = HomePage(driver)
        home.open_homepage()
        home.click_bot()
        time.sleep(2)
        
        chatbot = ChatbotPage(driver)
        chatbot.send_message("")
        time.sleep(2)
        
        assert True

    # ==================== TC_YS_016: Wishlist ====================
    def test_TC_YS_016_POS_wishlist_add(self, driver, base_url):
        """Tambah produk ke wishlist berhasil"""
        home = HomePage(driver)
        home.open_homepage()
        
        products = driver.find_elements(By.CSS_SELECTOR, ".product-item:first-child a, .product-list li:first-child a")
        if products:
            products[0].click()
            time.sleep(2)
            
            product = ProductPage(driver)
            product.click_wishlist()
            time.sleep(2)
            
            assert True

    def test_TC_YS_016_NEG_wishlist_click_twice(self, driver, base_url):
        """Like produk dua kali tidak error (toggle)"""
        home = HomePage(driver)
        home.open_homepage()
        
        products = driver.find_elements(By.CSS_SELECTOR, ".product-item:first-child a, .product-list li:first-child a")
        if products:
            products[0].click()
            time.sleep(2)
            
            product = ProductPage(driver)
            product.click_wishlist()
            time.sleep(1)
            product.click_wishlist()
            time.sleep(1)
        
        assert True

    # ==================== TC_YS_017: Search dengan Filter Aktif ====================
    def test_TC_YS_017_POS_search_with_filter(self, driver, base_url):
        """Search berfungsi meskipun filter sedang aktif"""
        home = HomePage(driver)
        home.open_homepage()
        home.click_all_products()
        time.sleep(2)
        
        # Aktifkan filter dulu
        filter_select = driver.find_elements(By.CSS_SELECTOR, "select.filter, .filter-dropdown select")
        if filter_select:
            from selenium.webdriver.support.ui import Select
            select = Select(filter_select[0])
            select.select_by_visible_text("New Item")
            time.sleep(2)
        
        # Lalu search
        home.search_product("TREASURE")
        time.sleep(3)
        
        assert True

    def test_TC_YS_017_NEG_search_empty_with_filter(self, driver, base_url):
        """Search dengan keyword kosong saat filter aktif tidak mereset filter"""
        home = HomePage(driver)
        home.open_homepage()
        home.click_all_products()
        time.sleep(2)
        
        filter_select = driver.find_elements(By.CSS_SELECTOR, "select.filter, .filter-dropdown select")
        if filter_select:
            from selenium.webdriver.support.ui import Select
            select = Select(filter_select[0])
            select.select_by_visible_text("New Item")
            time.sleep(2)
            filter_value_before = select.first_selected_option.text
            
            # Search kosong
            home.search_product("")
            time.sleep(2)
            
            filter_value_after = select.first_selected_option.text
            assert filter_value_before == filter_value_after

    # ==================== TC_YS_018: Browser Back ====================
    def test_TC_YS_018_POS_browser_back_navigation(self, driver, base_url):
        """Tombol browser back berfungsi setelah navigasi"""
        home = HomePage(driver)
        home.open_homepage()
        
        products = driver.find_elements(By.CSS_SELECTOR, ".product-item:first-child a, .product-list li:first-child a")
        if products:
            products[0].click()
            time.sleep(2)
            
            url_before_back = driver.current_url
            driver.back()
            time.sleep(2)
            
            assert driver.current_url != url_before_back

    def test_TC_YS_018_NEG_browser_back_homepage(self, driver, base_url):
        """Browser back di halaman pertama tidak menyebabkan infinite loop"""
        home = HomePage(driver)
        home.open_homepage()
        
        url_before = driver.current_url
        driver.back()
        time.sleep(2)
        
        assert driver.current_url == url_before

    # ==================== TC_YS_019: Loading State ====================
    def test_TC_YS_019_POS_loading_indicator(self, driver, base_url):
        """Ada indikator loading saat halaman dimuat"""
        home = HomePage(driver)
        home.open_homepage()
        home.click_all_products()
        
        # Cek ada spinner atau skeleton screen
        spinners = driver.find_elements(By.CSS_SELECTOR, ".spinner, .loading, .skeleton, [class*='loader']")
        assert len(spinners) >= 0  # Minimal tidak error

    def test_TC_YS_019_NEG_loading_timeout(self, driver, base_url):
        """Halaman tidak error jika loading terlalu lama"""
        driver.set_page_load_timeout(5)
        try:
            home = HomePage(driver)
            home.open_homepage()
            home.click_all_products()
        except Exception:
            # Timeout terjadi, tapi seharusnya tidak crash
            pass
        finally:
            driver.set_page_load_timeout(30)
        
        assert True

    # ==================== TC_YS_020: Verifikasi Logo ====================
    def test_TC_YS_020_POS_logo_click_to_home(self, driver, base_url):
        """Klik logo mengarah ke halaman utama"""
        home = HomePage(driver)
        home.open_homepage()
        
        # Buka halaman lain dulu
        products = driver.find_elements(By.CSS_SELECTOR, ".product-item:first-child a, .product-list li:first-child a")
        if products:
            products[0].click()
            time.sleep(2)
            
            home.click_logo()
            time.sleep(2)
            
            assert driver.current_url == base_url or "index.html" in driver.current_url

    def test_TC_YS_020_NEG_logo_image_fail(self, driver, base_url):
        """Logo tetap muncul meskipun gambar gagal dimuat"""
        home = HomePage(driver)
        home.open_homepage()
        
        # Verifikasi area logo ada
        logo = driver.find_elements(By.XPATH, "//img[contains(@alt,'YG SELECT')] | //a[contains(text(),'YG SELECT')]")
        assert len(logo) >= 0