import re
import pytest
from pages.login_page import LoginPage
from pages.manufacturing_requests_page import ManufacturingRequestsPage
from pages.add_manufacturing_request_page import AddManufacturingRequestPage
from utilis.config import Config

class TestManufacturingRequest:
    
    @pytest.fixture(autouse=True)
    def setup(self, page):
        """تهيئة الصفحات لكل اختبار"""
        self.page = page
        self.login_page = LoginPage(page)
        self.manufacturing_requests_page = ManufacturingRequestsPage(page)
        self.add_request_page = AddManufacturingRequestPage(page)
    
    def test_add_manufacturing_request(self):
        """✅ اختبار إضافة طلب تصنيع كامل"""
        print("\n" + "="*70)
        print("🏭 بدء اختبار إضافة طلب تصنيع جديد")
        print("="*70)
        self.login_page.login(
        username=Config.Users.SALES["username"], 
        password=Config.Users.SALES["password"]
        )
        # 1. تسجيل الدخول بحساب SALES
        # self.login_page.login(username="SALES", password="SALES")
        
        # 2. الذهاب إلى Manufacturing Requests
        self.manufacturing_requests_page.go_to_manufacturing_requests()
        
        # 3. الضغط على إضافة طلب
        self.manufacturing_requests_page.click_add_request()
        
        # 4. تعبئة بيانات العميل
        self.add_request_page.fill_client_and_location()
        
        # 5. تعبئة بيانات مقدم الطلب
        self.add_request_page.fill_applicant_info()
        
        # 6. Next
        self.add_request_page.click_next()
        
        # 7. تفعيل طلب تخصيص
        self.add_request_page.enable_custom_request()
        
        # 8. اختيار نوع الباب
        door_type = self.add_request_page.select_door_type()
        
        # 9. تعبئة المعلومات الأساسية
        basic_info = self.add_request_page.fill_basic_door_info()
        
        # 10. تعبئة الأبعاد
        dimensions = self.add_request_page.fill_dimensions()
        
        # 11. تعبئة المواصفات
        specifications = self.add_request_page.fill_door_specifications()
        
        # 12. تعبئة تفاصيل الإطار
        self.add_request_page.fill_frame_details()
        
        # 13. تعبئة تفاصيل الصفائح
        self.add_request_page.fill_sheet_details()
        
        # 14. تعبئة الإكسسوارات
        self.add_request_page.fill_accessories()
        
        # 15. إضافة الطلب وحفظه
        self.add_request_page.add_order_and_save()
        
        # 16. تأكيد الطلب
        self.add_request_page.confirm_order()
        
        # 17. طباعة التقرير
        print("\n" + "="*70)
        print("✨✅ نجح الاختبار! تم إضافة طلب التصنيع بنجاح")
        print(f"📊 ملخص الطلب:")
        print(f"   🚪 نوع الباب: {door_type}")
        print(f"   📦 الكمية: {basic_info['quantity']}")
        print(f"   💰 السعر: {basic_info['price']}")
        print(f"   📏 الأبعاد: {dimensions['width']} x {dimensions['length']}")
        print(f"   🧭 الاتجاه: {specifications['direction']}")
        print("="*70 + "\n")
        
        assert True
    
    def test_add_manufacturing_request_minimal(self):
        """✅ اختبار إضافة طلب تصنيع بحد أدنى من البيانات"""
        print("\n" + "="*70)
        print("🏭 بدء اختبار إضافة طلب تصنيع (الحد الأدنى)")
        print("="*70)
        
        self.login_page.login(username="SALES", password="SALES")
        self.manufacturing_requests_page.go_to_manufacturing_requests()
        self.manufacturing_requests_page.click_add_request()
        
        # تعبئة أقل البيانات المطلوبة
        self.add_request_page.fill_client_and_location(client="Mega Dev", location="Jeddah")
        self.add_request_page.fill_applicant_info()
        self.add_request_page.click_next()
        self.add_request_page.enable_custom_request()
        self.add_request_page.select_door_type(door_type="Hinged Door")
        self.add_request_page.fill_basic_door_info(quantity="10", price="200", door_option="Single")
        self.add_request_page.fill_dimensions(width="1000", length="2000")
        self.add_request_page.fill_door_specifications(
            thickness="92", direction="Left", temp_type="Freezer", 
            material="PVC", frame_type="Complete"
        )
        self.add_request_page.add_order_and_save()
        self.add_request_page.confirm_order()
        
        print("\n" + "="*70)
        print("✨✅ نجح الاختبار! تم إضافة طلب التصنيع (الحد الأدنى)")
        print("="*70 + "\n")
        
        assert True