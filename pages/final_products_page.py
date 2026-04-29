from playwright.sync_api import Page

class FinalProductsPage:
    def __init__(self, page: Page):
        self.page = page
    
    def go_to_final_products(self):
        """الذهاب لصفحة المنتجات النهائية"""
        print("📦 Go to final products page..")
        
        # جرب اكتر من طريقة
        try:
            self.page.get_by_text("Final Products").click()
        except:
            try:
                self.page.click("a[href*='finalProducts']")
            except:
                self.page.goto("https://idif.ebdaa-business.com/finalProducts")
        
        self.page.wait_for_timeout(3000)
        print("✅ arrive to final products page")
    
    def click_add_product(self):
        """الضغط على زر اضافة منتج"""
        print("➕ Go to add product page...")
        self.page.get_by_role("button", name="plus Add Product").click()
        self.page.wait_for_timeout(3000)
        print("✅ arrive to add product page")
    
    def search_for_product(self, product_name):
        """البحث عن منتج"""
        print(f"🔍 Searching for product: {product_name}")
        
        # انتظر تحميل الجدول
        self.page.wait_for_timeout(2000)
        
        # جرب اكتر من selector لحقل البحث
        selectors = [
            "input[placeholder*='Search']",
            "input[placeholder*='بحث']",
            "input[type='search']",
            ".ant-input"
        ]
        
        search_box = None
        for selector in selectors:
            try:
                search_box = self.page.locator(selector).first
                if search_box.is_visible():
                    break
            except:
                continue
        
        if search_box:
            search_box.click()
            search_box.fill(product_name)
            self.page.wait_for_timeout(3000)
            print(f"✅ Searching for: {product_name}")
        else:
            print("❌ No search box found")
            self.page.screenshot(path="no_search_box.png")
    
    def verify_product_exists(self, product_name):
        """التأكد من وجود المنتج في الجدول"""
        try:
            # انتظر ظهور المنتج
            self.page.wait_for_selector(f"text={product_name}", timeout=10000)
            print(f"✅ Found product: {product_name}")
            return True
        except:
            print(f"❌ Product not found: {product_name}")
            # خد سكرين شوت عشان نشوف ايه موجود
            self.page.screenshot(path="product_not_found.png")
            return False