import pytest
import re
import time
import random
import json
from datetime import datetime
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
    
    def test_add_standard_product_3_times(self):
        """🔄 تشغيل الاختبار 3 مرات متتالية - Standard Product"""
        print("\n" + "="*70)
        print("🔄 Starting Standard Product Tests 3 times")
        print("="*70)
        
        results = []
        failures = []
        
        for run in range(1, 4):
            print(f"\n{'='*50}")
            print(f"📌 start number {run} من 3")
            print(f"{'='*50}")
            
            try:
                # سجل وقت البدء
                start_time = time.time()
                
                # 1. تسجيل الدخول
                self.login_page.login()
                
                # 2. الذهاب للمنتجات النهائية
                self.final_products_page.go_to_final_products()
                
                # 3. الضغط على اضافة منتج
                self.final_products_page.click_add_product()
                
                # بيانات فريدة للمنتج
                timestamp = int(time.time())
                product_name_ar = f"تيست ستاندرد رن{run} {timestamp}"
                product_name_en = f"Standard Test Run{run} {timestamp}"
                product_code = f"STDR{run}{timestamp}"
                
                print(f"📝 product {run}: {product_name_ar} - {product_code}")
                
                # 4. رفع صورة
                self.add_product_page.upload_image("test_data/product_image.jpeg")
                
                # 5. تعبئة البيانات الأساسية
                self.add_product_page.fill_basic_info(
                    name_ar=product_name_ar,
                    name_en=product_name_en,
                    code=product_code,
                    price=str(150 + (run * 10)),
                    quantity=str(100 + (run * 5)),
                    min_quantity=str(10 + run)
                )
                
                # 6. اختيار نوع STANDARD
                self.add_product_page.select_product_type("Standard")
                
                # 7. تعبئة خيارات STANDARD - اختيار عشوائي
                selected_options = self.add_product_page.fill_standard_options()
                
                # 8. تعبئة الملاحظات
                self.add_product_page.fill_notes(f"تشغيل رقم {run} - تم بواسطة الاختبار الاوتوماتيكي")
                
                # 9. حفظ المنتج
                self.add_product_page.save_product()
                
                # 10. البحث عن المنتج
                self.page.wait_for_timeout(3000)
                self.final_products_page.search_for_product(product_name_ar)
                
                # 11. التحقق
                assert self.final_products_page.verify_product_exists(product_name_ar), \
                    f"المنتج {product_name_ar} لم يتم العثور عليه"
                
                # حساب الوقت المستغرق
                duration = time.time() - start_time
                
                # تسجيل النتيجة
                results.append({
                    "run": run,
                    "status": "PASSED",
                    "name": product_name_ar,
                    "code": product_code,
                    "duration": round(duration, 2),
                    "options": selected_options
                })
                
                print(f"\n✅ التشغيل {run}: PASSED (في {round(duration, 2)} ثانية)")
                
            except Exception as e:
                # تسجيل الفشل
                duration = time.time() - start_time if 'start_time' in locals() else 0
                failures.append({
                    "run": run,
                    "status": "FAILED",
                    "error": str(e),
                    "duration": round(duration, 2)
                })
                
                print(f"\n❌ التشغيل {run}: FAILED - {str(e)}")
                # خد سكرين شوت للخطأ
                self.page.screenshot(path=f"failure_run_{run}.png")
                print(f"📸 save screenshot: failure_run_{run}.png")
                
                # استمر في التشغيلات التالية حتى لو فشلت واحدة
                continue
        
        # طباعة التقرير النهائي
        print("\n" + "="*70)
        print("📊 التقرير النهائي - تشغيل 3 مرات")
        print("="*70)
        
        print(f"\n✅ الناجح: {len(results)} من 3")
        print(f"❌ الفاشل: {len(failures)} من 3")
        
        # تفاصيل الناجحين
        if results:
            print("\n📋 تفاصيل التشغيلات الناجحة:")
            for r in results:
                print(f"\n   التشغيل {r['run']}:")
                print(f"      الاسم: {r['name']}")
                print(f"      الكود: {r['code']}")
                print(f"      الوقت: {r['duration']} ثانية")
                print(f"      الطول: {r['options']['length']}")
                print(f"      العرض: {r['options']['width']}")
                print(f"      الاكسسوار: {r['options']['accessories_type']}")
        
        # تفاصيل الفاشلين
        if failures:
            print("\n❌ تفاصيل التشغيلات الفاشلة:")
            for f in failures:
                print(f"\n   التشغيل {f['run']}:")
                print(f"      الخطأ: {f['error']}")
                print(f"      الوقت: {f['duration']} ثانية")
        
        print("\n" + "="*70)
        
        # إذا فشلت كل التشغيلات، يفشل الاختبار
        if len(results) == 0:
            assert False, "❌ جميع التشغيلات الثلاثة فشلت!"
        else:
            print(f"\n✨ نجح {len(results)} من أصل 3 تشغيلات")
            assert True
    
    def test_add_standard_product_with_report(self):
        """📝 اختبار اضافة منتج Standard مع تقرير مفصل"""
        print("\n" + "="*60)
        print("📝 بدء اختبار اضافة منتج قياسي (STANDARD) - مع تقرير")
        print("="*60)
        
        # تسجيل وقت البدء
        test_start_time = datetime.now()
        
        try:
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
            
            print(f"📝 المنتج: {product_name_ar} - {product_code}")
            
            # 4. رفع صورة
            self.add_product_page.upload_image("test_data/product_image.jpeg")
            
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
            
            # 7. تعبئة خيارات STANDARD - اختيار عشوائي
            selected_options = self.add_product_page.fill_standard_options()
            
            # 8. تعبئة الملاحظات
            self.add_product_page.fill_notes("تم اضافة المنتج عن طريق اختبار اوتوماتيكي")
            
            # 9. حفظ المنتج
            self.add_product_page.save_product()
            
            # 10. البحث عن المنتج
            self.page.wait_for_timeout(3000)
            self.final_products_page.search_for_product(product_name_ar)
            
            # 11. التحقق
            assert self.final_products_page.verify_product_exists(product_name_ar), \
                f"المنتج {product_name_ar} لم يتم العثور عليه"
            
            # حساب الوقت المستغرق
            test_duration = (datetime.now() - test_start_time).total_seconds()
            
            # طباعة التقرير
            print("\n" + "="*60)
            print("📊 تقرير الاختبار")
            print("="*60)
            print(f"✅ الحالة: PASSED")
            print(f"⏱️ الوقت المستغرق: {round(test_duration, 2)} ثانية")
            print(f"📝 الاسم: {product_name_ar}")
            print(f"🔢 الكود: {product_code}")
            print(f"🎲 القيم العشوائية:")
            print(f"   📏 الطول: {selected_options['length']}")
            print(f"   📐 العرض: {selected_options['width']}")
            print(f"   🔢 عدد الحواف: {selected_options['frame_edges']}")
            print(f"   🧭 الاتجاه: {selected_options['direction']}")
            print(f"   🌡️ النوع: {selected_options['temperature_type']}")
            print(f"   🔧 الاكسسوار: {selected_options['accessories_type']}")
            print("="*60 + "\n")
            
        except Exception as e:
            test_duration = (datetime.now() - test_start_time).total_seconds()
            print("\n" + "="*60)
            print("📊 تقرير الاختبار - فشل!")
            print("="*60)
            print(f"❌ الحالة: FAILED")
            print(f"⏱️ الوقت المستغرق: {round(test_duration, 2)} ثانية")
            print(f"❌ سبب الفشل: {str(e)}")
            print("="*60 + "\n")
            
            self.page.screenshot(path=f"failure_{int(time.time())}.png")
            raise e
    
    def test_add_imported_product(self):
        """✅ اختبار اضافة منتج نوع Imported"""
        print("\n" + "="*60)
        print("🚀 بدء اختبار اضافة منتج مستورد (IMPORTED)")
        print("="*60)
        
        test_start_time = datetime.now()
        
        try:
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
            
            # 4. رفع صورة
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
            
            # 9. انتظر زيادة
            self.page.wait_for_timeout(5000)
            
            # 10. البحث عن المنتج
            self.final_products_page.search_for_product(product_name_ar)
            
            # 11. التحقق
            assert self.final_products_page.verify_product_exists(product_name_ar), \
                f"المنتج المستورد {product_name_ar} لم يتم العثور عليه"
            
            test_duration = (datetime.now() - test_start_time).total_seconds()
            
            print("\n" + "="*60)
            print("📊 تقرير الاختبار - منتج مستورد")
            print("="*60)
            print(f"✅ الحالة: PASSED")
            print(f"⏱️ الوقت المستغرق: {round(test_duration, 2)} ثانية")
            print(f"📝 الاسم: {product_name_ar}")
            print(f"🔢 الكود: {product_code}")
            print("="*60 + "\n")
            
        except Exception as e:
            test_duration = (datetime.now() - test_start_time).total_seconds()
            print("\n" + "="*60)
            print("📊 تقرير الاختبار - فشل!")
            print("="*60)
            print(f"❌ الحالة: FAILED")
            print(f"⏱️ الوقت المستغرق: {round(test_duration, 2)} ثانية")
            print(f"❌ سبب الفشل: {str(e)}")
            print("="*60 + "\n")
            
            self.page.screenshot(path=f"failure_imported_{int(time.time())}.png")
            raise e
        
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(self, item, call):
        outcome = yield
        report = outcome.get_result()
        if hasattr(self, 'test_data'):
            report.test_data = json.dumps(self.test_data, ensure_ascii=False)