import re
from playwright.sync_api import Page
import time

class ManufacturingRequestsPage:
    def __init__(self, page: Page):
        self.page = page
    
    def go_to_manufacturing_requests(self):
        """الذهاب إلى صفحة طلبات التصنيع"""
        print("📋 جاري الذهاب إلى Manufacturing Requests...")
        
        try:
            self.page.get_by_role("menuitem", name="Manufacturing Requests").click()
            self.page.wait_for_timeout(2000)
            print("✅ تم الوصول إلى صفحة طلبات التصنيع")
        except Exception as e:
            print(f"⚠️ خطأ: {e}")
            raise
    
    def click_add_request(self):
        """الضغط على زر إضافة طلب"""
        print("➕ جاري إضافة طلب تصنيع جديد...")
        
        try:
            self.page.get_by_role("button", name="plus Add a Request").click()
            self.page.wait_for_timeout(2000)
            print("✅ تم فتح نموذج إضافة الطلب")
        except Exception as e:
            print(f"⚠️ خطأ: {e}")
            raise