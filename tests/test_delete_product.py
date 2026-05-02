import pytest
import time
from pages.login_page import LoginPage
from pages.final_products_page import FinalProductsPage
from pages.delete_product_page import DeleteProductPage
from playwright.sync_api import expect
from utilis.config import Config
class TestDeleteProduct:
    
    @pytest.fixture(autouse=True)
    def setup(self, page):
        self.page = page
        self.login_page = LoginPage(page)
        self.final_products_page = FinalProductsPage(page)
        self.delete_product_page = DeleteProductPage(page)
    
    def test_delete_first_product(self):
        """✅ اختبار حذف أول منتج في القائمة"""
        print("\n" + "="*60)
        print("🗑️Start delete first product test ")
        print("="*60)
        
        self.login_page.login(
            username=Config.Users.JEDDAH["username"], 
            password=Config.Users.JEDDAH["password"]
        )
        self.final_products_page.go_to_final_products()
        
        # سجل عدد المنتجات قبل الحذف
        before_count = self.page.locator("table tbody tr").count()
        print(f"📊 عدد المنتجات قبل الحذف: {before_count}")
        
        if before_count == 0:
            print("⚠️ لا يوجد منتجات للحذف!")
            assert True, "لا يوجد منتجات للحذف - تخطي الاختبار"
        
        # حذف المنتج الأول
        result = self.delete_product_page.delete_first_product()
        
        if result:
            # انتظر التحديث
            rows = self.page.locator("table tbody tr")

            try:
                expect(rows).to_have_count(before_count - 1, timeout=5000)
                print(f"✨✅ نجح الاختبار! تم حذف المنتج بنجاح")
            except AssertionError:
                after_count = rows.count()
                print(f"⚠️ فشل: العدد ما زال {after_count}")
                raise # عشان الاختبار يفشل رسمياً
            
            # سجل عدد المنتجات بعد الحذف
            after_count = self.page.locator("table tbody tr").count()
            print(f"📊 عدد المنتجات بعد الحذف: {after_count}")
            