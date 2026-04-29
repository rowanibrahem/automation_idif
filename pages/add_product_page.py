from playwright.sync_api import Page
import re
import os
import random

class AddProductPage:
    def __init__(self, page: Page):
        self.page = page
        self.length_options = ["1800", "1900", "2000", "2500", "3000"]
        self.width_options = ["800", "900", "1000", "2000", "2500"]
        self.frame_edges_options = ["3", "4"]
        self.direction_options = ["Left", "Right"]
        self.temperature_options = ["Freezer", "Chiller"]
        self.accessories_options = ["MTH", "IDIF"]
    
    def get_random_length(self):
        return random.choice(self.length_options)
    
    def get_random_width(self):
        return random.choice(self.width_options)
    
    def get_random_frame_edges(self):
        return random.choice(self.frame_edges_options)
    
    def get_random_direction(self):
        return random.choice(self.direction_options)
    
    def get_random_temperature(self):
        return random.choice(self.temperature_options)
    
    def get_random_accessories(self):
        return random.choice(self.accessories_options)
    
    def upload_image(self, image_path):
        """رفع صورة المنتج - الطريقة الصحيحة"""
        print(f"🖼️ Go to upload image: {image_path}")
        
        # المسار المطلق للصورة
        full_path = r"C:\Users\rowan\automation_project\test_data\product_image.jpeg"
        
        # تأكد من وجود الصورة
        if os.path.exists(full_path):
            print(f"✅ Found image: {full_path}")
            image_path = full_path
        else:
            print(f"❌ Image not found in: {full_path}")
            print("📌 Please make sure the image exists in the folder")
            return False
        
        try:
            # الطريقة الصحيحة: استخدم JavaScript لإظهار input file
            self.page.evaluate("""
                () => {
                    const fileInput = document.querySelector('input[type="file"]');
                    if (fileInput) {
                        fileInput.style.display = 'block';
                        fileInput.style.opacity = '1';
                        fileInput.style.visibility = 'visible';
                    }
                }
            """)
            
            # انتظر ظهور input file
            self.page.wait_for_selector("input[type='file']", timeout=5000)
            
            # ارفع الصورة
            self.page.set_input_files("input[type='file']", image_path)
            self.page.wait_for_timeout(2000)
            
            # انتظر ظهور معاينة الصورة
            self.page.wait_for_timeout(2000)
            print("✅ image uploaded successfully")
            return True
            
        except Exception as e:
            print(f"⚠️ Error uploading image: {e}")
            
            # جرب طريقة تانية: عن طريق الـ div
            try:
                # اضغط على زر رفع الصورة
                upload_button = self.page.locator("div:has-text('Drag and drop an image')").first
                upload_button.click()
                self.page.wait_for_timeout(1000)
                
                # ارفع الصورة
                self.page.set_input_files("input[type='file']", image_path)
                self.page.wait_for_timeout(2000)
                print("✅ image uploaded successfully (method 2)")
                return True
            except Exception as e2:
                print(f"❌ Failed to upload image: {e2}")
                return False
    
    def fill_basic_info(self, name_ar, name_en, code, price, quantity, min_quantity):
        """تعبئة البيانات الأساسية"""
        print("📝 Go to fill basic info...")
        
        # الاسم بالعربي
        self.page.get_by_role("textbox", name="Product Name in Arabic*").fill(name_ar)
        
        # الاسم بالإنجليزي
        self.page.get_by_role("textbox", name="Product Name in English*").fill(name_en)
        
        # كود المنتج
        self.page.get_by_role("textbox", name="Product Code*").fill(code)
        
        # السعر
        self.page.get_by_role("spinbutton", name="Price (SAR)*").fill(price)
        
        # الكمية
        self.page.get_by_role("textbox", name="Quantity", exact=True).fill(quantity)
        
        # الحد الأدنى للكمية
        self.page.get_by_role("textbox", name="Minimum Quantity").fill(min_quantity)
        
        print("✅ Go to fill basic info...")
    
    def select_product_type(self, product_type):
        """اختيار نوع المنتج (Standard أو Imported)"""
        print(f"📌 Go to select product type: {product_type}")
        
        # فتح القائمة المنسدلة
        self.page.get_by_role("combobox", name="Product type*").click()
        self.page.wait_for_timeout(500)
        
        # اختيار النوع
        if product_type.upper() == "STANDARD":
            self.page.get_by_text("Standard", exact=True).click()
        else:
            self.page.get_by_title("Imported").click()
        
        self.page.wait_for_timeout(1000)
        print(f"✅ Go to select product type: {product_type}")
    
    def fill_standard_options(self, length=None, width=None, frame_edges=None, direction=None, temperature_type=None, accessories_type=None):
        """تعديل لاختيار الخيارات بشكل أكثر استقراراً"""
        
        # اختيار قيم عشوائية إذا لم تُحدد
        if length is None: length = self.get_random_length()
        if width is None: width = self.get_random_width()
        if frame_edges is None: frame_edges = self.get_random_frame_edges()
        if direction is None: direction = self.get_random_direction()
        if temperature_type is None: temperature_type = self.get_random_temperature()
        if accessories_type is None: accessories_type = self.get_random_accessories()
        # ... بقية التعيينات العشوائية كما هي ...

        print("⚙️ Go to fill standard options...")

        # 1. اختيار الطول - تحديث المحدد ليكون أكثر دقة
        # نضغط أولاً على حقل القائمة المنسدلة الخاص بالطول
        self.page.locator("div").filter(has_text=re.compile(r"^length$")).nth(1).click()
        dropdown_container = self.page.locator(".ant-select-dropdown:not(.ant-select-dropdown-hidden)")

        # اختاري القيمة من داخل الحاوية دي فوراً
        dropdown_container.get_by_title(length, exact=True).click()

        # 2. اختيار العرض بنفس الطريقة المستقرة
        self.page.locator("div").filter(has_text=re.compile(r"^width$")).nth(1).click()
        dropdown_container = self.page.locator(".ant-select-dropdown:not(.ant-select-dropdown-hidden)")

        # اختاري القيمة من داخل الحاوية دي فوراً
        dropdown_container.get_by_title(width, exact=True).click()

        
        # عدد الحواف
        print(f"📌 محاولة اختيار عدد الحواف: {frame_edges}")
        try:
            self.page.locator("div").filter(has_text=re.compile(r"^Number of Frame Edges$")).nth(1).click()

            self.page.wait_for_timeout(500)
        
            self.page.get_by_title(str(frame_edges), exact=True).click()
            print(f"✅ عدد الحواف: {frame_edges}")
        except Exception as e:
            print(f"⚠️ failed to select Number of Frame Edges: {e}")
            self.page.locator(f"div.ant-select-item-option-content:has-text('{frame_edges}')").first.click()
            self.page.wait_for_timeout(500)
        
        
        # الاتجاه
        self.page.get_by_text(direction, exact=True).click()
        self.page.wait_for_timeout(500)
        
        # النوع (Freezer/Cooler/etc)
        self.page.get_by_text(temperature_type, exact=True).click()
        self.page.wait_for_timeout(500)
        
        # Accessories Type
        print(f"   - اختيار Accessories Type: {accessories_type}")
        
        try:
            accessories_label = self.page.locator("text=Accessories Type").first
            accessories_label.click()
            self.page.wait_for_timeout(500)
            self.page.get_by_text(accessories_type, exact=True).click()
            print(f"✅ select Accessories Type: {accessories_type}")
        except:
            try:
                self.page.click("div:has-text('Accessories Type')")
                self.page.wait_for_timeout(500)
                self.page.click(f"div[title='{accessories_type}']")
                print(f"✅ select Accessories Type: {accessories_type}")
            except:
                try:
                    self.page.get_by_role("combobox", name="Accessories Type").click()
                    self.page.wait_for_timeout(500)
                    self.page.get_by_role("option", name=accessories_type).click()
                    print(f"✅ select Accessories Type: {accessories_type}")
                except Exception as e:
                    print(f"⚠️ failed to select Accessories Type: {e}")
        
        self.page.wait_for_timeout(500)
        print("✅ Go to fill additional options...")

        # رجع القيم اللي اتعملها
        return {
            "length": length,
            "width": width,
            "frame_edges": frame_edges,
            "direction": direction,
            "temperature_type": temperature_type,
            "accessories_type": accessories_type
        }
    
    def fill_notes(self, notes):
        """تعبئة الملاحظات"""
        print("📝 Go to fill notes...")
        
        # حقل الملاحظات باستخدام quill editor
        self.page.locator(".ql-editor").click()
        self.page.locator(".ql-editor").fill(notes)
        
        print("✅ Notes filled successfully")
    
    def save_product(self):
        """حفظ المنتج والعودة للصفحة الرئيسية"""
        print("💾 Go to save product...")
        
        # حفظ المنتج
        self.page.get_by_role("button", name="Save").click()
        
        # انتظر ظهور رسالة نجاح
        self.page.wait_for_timeout(5000)
        
        # خد سكرين شوت بعد الحفظ
        self.page.screenshot(path="after_save.png")
        
        # نتأكد اننا رجعنا لصفحة المنتجات النهائية
        try:
            self.page.wait_for_selector("text=Final Products", timeout=10000)
            print("✅ Go to save product... Product saved and returned to final products page")
        except:
            print("⚠️ Go to return to final products page")
            self.page.goto("https://idif.ebdaa-business.com/finalProducts")
            self.page.wait_for_timeout(3000)