from playwright.sync_api import Page
import time

class DeleteProductPage:
    def __init__(self, page: Page):
        self.page = page
    
    def delete_first_product(self):
        """حذف أول منتج في القائمة - باستخدام selectors من codegen"""
        print("🗑️ جاري حذف أول منتج...")
        
        try:
            # انتظر تحميل الجدول
            self.page.wait_for_timeout(3000)
            
            # من الـ codegen: page.get_by_role("button", name="delete").nth(1).click()
            # نستخدم نفس الـ selector
            delete_button = self.page.get_by_role("button", name="delete")
            
            if delete_button.count() > 0:
                # نضغط على أول زر delete
                delete_button.first.click()
                print("✅ تم الضغط على زر الحذف")
            else:
                print("❌ لم يتم العثور على زر حذف")
                return False
            
            # انتظار نافذة التأكيد
            self.page.wait_for_timeout(1500)
            
            # من الـ codegen: page.get_by_role("button", name="Accept").click()
            accept_button = self.page.get_by_role("button", name="Accept")
            if accept_button.is_visible():
                accept_button.click()
                print("✅ تم تأكيد الحذف")
                self.page.wait_for_selector("text=Accept", state="hidden")
                
                self.page.wait_for_load_state("networkidle")
                return True
            else:
                print("❌ لم يتم العثور على زر التأكيد")
                return False
                
        except Exception as e:
            print(f"⚠️ خطأ: {e}")
            self.page.screenshot(path="delete_error.png")
            return False