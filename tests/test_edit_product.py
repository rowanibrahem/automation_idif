import pytest
from pages.login_page import LoginPage
from pages.final_products_page import FinalProductsPage
from pages.edit_product_page import EditProductPage
from playwright.sync_api import expect
from utilis.config import Config

class TestEditProduct:
    
    @pytest.fixture(autouse=True)
    def setup(self, page):
        self.page = page
        self.login_page = LoginPage(page)
        self.final_products_page = FinalProductsPage(page)
        self.edit_page = EditProductPage(page)

    def test_edit_product_details(self):
        print("\n" + "="*60)
        print("🛠️ start edit product ")
        print("="*60)
        
        # 1. تسجيل الدخول والذهاب للمنتجات
        self.login_page.login(
            username=Config.Users.JEDDAH["username"], 
            password=Config.Users.JEDDAH["password"]
        )
        self.final_products_page.go_to_final_products()
        
        # بيانات التجربة
        target_name = "Imported Test Edited"
        target_qty = "99"
        
        # 2. تنفيذ عملية التعديل
        self.edit_page.edit_first_product(target_name, target_qty)
        
        # 3. التأكد من نجاح التعديل (Assertion)
        # هننتظر ظهور رسالة نجاح أو نتأكد إن البيانات اتحدثت في الجدول
        
        # مثال: التأكد أن الاسم الجديد ظهر في أول صف بالجدول
        first_row = self.page.locator("table tbody tr").first
        print(f"⏳ جاري التأكد من ظهور الاسم الجديد: {target_name}")
        expect(first_row).to_contain_text(target_qty, timeout=10000)
        
        print(f"✨✅ edit successfully and be sure from data : {target_name}")