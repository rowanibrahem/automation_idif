import pytest
import re
import time
from pages.login_page import LoginPage
from pages.final_products_page import FinalProductsPage
from pages.add_product_page import AddProductPage

class TestFinalProducts:
    
    @pytest.fixture(autouse=True)
    def setup(self, page):
        """تهيئة الصفحات لكل اختبار"""
        self.page = page
        self.login_page = LoginPage(page)
        self.final_products_page = FinalProductsPage(page)
        self.add_product_page = AddProductPage(page)
    
    def test_add_standard_product(self):
        """✅ اختبار اضافة منتج نوع Standard"""
        print("\n" + "="*60)
        print("🚀 بدء اختبار اضافة منتج قياسي (STANDARD)")
        print("="*60)
        
        # 1. تسجيل الدخول
        self.login_page.login()
        
        # 2. الذهاب للمنتجات النهائية
        self.final_products_page.go_to_final_products()
        
        # 3. الضغط على اضافة منتج
        self.final_products_page.click_add_product()
        
        # بيانات فريدة للمنتج
        timestamp = int(time.time())
        product_name_ar = f"تيست ستاندرد {timestamp}"
        product_name_en = f"Standard Test {timestamp}"
        product_code = f"STD{timestamp}"
        
        # 4. رفع صورة
        image_uploaded = self.add_product_page.upload_image("test_data/product_image.jpeg")
        if not image_uploaded:
         print("⚠️ لم يتم رفع الصورة، سنكمل الاختبار بدونها")
         
        # 5. تعبئة البيانات الأساسية
        self.add_product_page.fill_basic_info(
            name_ar=product_name_ar,
            name_en=product_name_en,
            code=product_code,
            price="150",
            quantity="100",
            min_quantity="10"
        )
        
        # 6. اختيار نوع STANDARD
        self.add_product_page.select_product_type("Standard")
        
        # 7. تعبئة خيارات STANDARD
        self.add_product_page.fill_standard_options(
            length="1800",
            width="800",
            frame_edges="3",
            direction="Left",
            temperature_type="Freezer",
            accessories_type="MTH"
        )
        
        # 8. تعبئة الملاحظات
        self.add_product_page.fill_notes("تم اضافة المنتج عن طريق اختبار اوتوماتيكي (Standard)")
        
        # 9. حفظ المنتج
        self.add_product_page.save_product()
        self.page.screenshot(path="after_save.png")
        print("📸 تم اخذ سكرين شوت بعد الحفظ")
        
        # 10. البحث عن المنتج والتأكد من اضافته
        self.page.wait_for_timeout(5000)
        self.final_products_page.search_for_product(product_name_ar)
        
        # 11. التحقق من وجود المنتج
        try:
            assert self.final_products_page.verify_product_exists(product_name_ar), \
                f"❌ المنتج {product_name_ar} لم يظهر في القائمة بعد الاضافة"
        except AssertionError as e:
            self.page.screenshot(path=f"failure_{product_code}.png")
            print(f"📸 تم حفظ سكرين شوت للخطأ: failure_{product_code}.png")
            raise e
        
        print("\n" + "="*60)
        print(f"✨✅ نجح الاختبار! المنتج القياسي تمت اضافته بنجاح")
        print(f"📝 الاسم: {product_name_ar}")
        print(f"🔢 الكود: {product_code}")
        print("="*60 + "\n")
    
    def test_add_imported_product(self):
        """✅ اختبار اضافة منتج نوع Imported"""
        print("\n" + "="*60)
        print("🚀 بدء اختبار اضافة منتج مستورد (IMPORTED)")
        print("="*60)
        
        # 1. تسجيل الدخول
        self.login_page.login()
        
        # 2. الذهاب للمنتجات النهائية
        self.final_products_page.go_to_final_products()
        
        # 3. الضغط على اضافة منتج
        self.final_products_page.click_add_product()
        
        # بيانات فريدة للمنتج
        timestamp = int(time.time())
        product_name_ar = f"تيست استيراد {timestamp}"
        product_name_en = f"Imported Test {timestamp}"
        product_code = f"IMP{timestamp}"
        
        print(f"📝 هنضيف المنتج: {product_name_ar} - {product_code}")
        
        # 4. رفع صورة (هنتخطى)
        self.add_product_page.upload_image("test_data/product_image.jpeg")
        
        # 5. تعبئة البيانات الأساسية
        self.add_product_page.fill_basic_info(
            name_ar=product_name_ar,
            name_en=product_name_en,
            code=product_code,
            price="300",
            quantity="50",
            min_quantity="5"
        )
        
        # 6. اختيار نوع IMPORTED
        self.add_product_page.select_product_type("Imported")
        
        # 7. تعبئة الملاحظات
        self.add_product_page.fill_notes("منتج مستورد - تمت الاضافة عن طريق اختبار اوتوماتيكي")
        
        # 8. حفظ المنتج
        self.add_product_page.save_product()
        
        # 9. انتظر زيادة عشان الصفحة تتحمل
        self.page.wait_for_timeout(5000)
        
        # 10. البحث عن المنتج
        self.final_products_page.search_for_product(product_name_ar)
        
        # 11. التحقق من وجود المنتج
        assert self.final_products_page.verify_product_exists(product_name_ar), \
            f"المنتج المستورد {product_name_ar} لم يتم العثور عليه"
        
        print("\n" + "="*60)
        print(f"✨✅ نجح الاختبار! المنتج المستورد تمت اضافته بنجاح")
        print(f"📝 الاسم: {product_name_ar}")
        print(f"🔢 الكود: {product_code}")
        print("="*60 + "\n")