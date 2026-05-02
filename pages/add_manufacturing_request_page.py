import re
from playwright.sync_api import Page
import time
import random

class AddManufacturingRequestPage:
    def __init__(self, page: Page):
        self.page = page
        
        # بيانات عشوائية للاختبار
        self.client_options = ["Mega Dev"]
        self.location_options = ["Jeddah", "Riyadh"]
        self.door_types = ["Hinged Door", "Sliding Door", "Swing Door" , "Servise Door", "Panel Sandwitch"]
        self.door_options = ["Single", "Double"]
        self.directions = ["Left", "Right"]
        self.temperature_types = ["Freezer", "Chiller"]
        self.color_options = ["White", "Black", "Gray"]
        self.frame_types = ["Complete", "Latch"]
        self.accessories_options = ["MTH", "IDIF"]
        self.window_options = ["Circular", "Oval", "None"]
        self.hinges_options = ["Standard", "Heavy Duty", "Stainless"]
        self.thickness_options = ["92", "68", "121", "151", "40"]
        
        # نطاقات الأسعار والكميات
        self.min_quantity = 1
        self.max_quantity = 100
        self.min_price = 50
        self.max_price = 500
    
    def get_random_quantity(self):
        return str(random.randint(self.min_quantity, self.max_quantity))
    
    def get_random_price(self):
        return str(random.randint(self.min_price, self.max_price))
    
    def get_random_width(self):
        return str(random.randint(800, 2500))
    
    def get_random_length(self):
        return str(random.randint(1800, 3000))
    
    def get_random_thickness(self):
        return random.choice(self.thickness_options)
    
    def fill_client_and_location(self, client=None, location=None):
        """تعبئة بيانات العميل ومكان الاستلام"""
        print("🏢 جاري تعبئة بيانات العميل...")
        
        if client is None: client = random.choice(self.client_options)
        if location is None: location = random.choice(self.location_options)
        
        try:
            # 1. تفعيل Toggle "Client Exists" إذا كان موجوداً وغير مفعل
            # هذا يحاكي كود السيلينيوم الذي أرسلته
            toggle = self.page.locator("//div[contains(@class, 'cursor-pointer') and contains(@class, 'flex')]")
            if toggle.is_visible() and "justify-start" in (toggle.get_attribute("class") or ""):
                toggle.click()
                self.page.wait_for_timeout(1000)

            # 2. فتح قائمة العميل (Ant Design Selector)
            # نستخدم الكلاس ant-select-selector لأنه الأكثر استقراراً
            self.page.locator(".ant-select-selector").first.click()
            self.page.wait_for_timeout(500)
            
            # 3. اختيار العميل من القائمة المنسدلة
            self.page.get_by_text(client, exact=True).click()
            print(f"✅ تم اختيار العميل: {client}")
            
            # 4. اختيار مكان الاستلام (Radio Button)
            # نستخدم force=True لأن الـ Radio يكون مخفياً أحياناً خلف التصميم
            location_radio = self.page.locator(f"input[type='radio'][value='{location.upper()}']")
            if location_radio.count() > 0:
                location_radio.check(force=True)
            else:
                self.page.get_by_text(location, exact=True).click()
                
            print(f"✅ تم اختيار مكان الاستلام: {location}")
            
        except Exception as e:
            print(f"⚠️ خطأ في اختيار العميل: {e}")
            raise
    
    def fill_applicant_info(self, name="Automation Test", phone="01011873749", email="test@automation.com"):
        """تعبئة بيانات مقدم الطلب"""
        print("👤 جاري تعبئة بيانات مقدم الطلب...")
        
        try:
            self.page.get_by_role("textbox", name="Applicant Name").fill(name)
            self.page.get_by_role("textbox", name="Phone Number").fill(phone)
            self.page.get_by_role("textbox", name="Email").fill(email)
            print(f"✅ تم تعبئة بيانات مقدم الطلب: {name}")
        except Exception as e:
            print(f"⚠️ خطأ في تعبئة بيانات مقدم الطلب: {e}")
            raise
    
    def click_next(self):
        """الضغط على زر Next"""
        print("➡️ جاري الانتقال إلى الخطوة التالية...")
        
        try:
            self.page.get_by_role("button", name="Next").click()
            self.page.wait_for_timeout(2000)
            print("✅ تم الانتقال")
        except Exception as e:
            print(f"⚠️ خطأ: {e}")
            raise
    
    def enable_custom_request(self):
        """تفعيل طلب تخصيص"""
        print("⚙️ جاري تفعيل طلب التخصيص...")
        
        try:
            self.page.locator("div").filter(has_text="Add custom request").nth(4).click()
            self.page.wait_for_timeout(500)
            self.page.get_by_role("switch").click()
            self.page.wait_for_timeout(1000)
            print("✅ تم تفعيل طلب التخصيص")
        except Exception as e:
            print(f"⚠️ خطأ في تفعيل طلب التخصيص: {e}")
            raise
    
    def select_door_type(self, door_type=None):
        """اختيار نوع الباب"""
        if door_type is None:
            door_type = random.choice(self.door_types)
        
        print(f"🚪 جاري اختيار نوع الباب: {door_type}")
        
        try:
            self.page.locator(".ant-select-selector").first.click()
            self.page.wait_for_timeout(500)
            self.page.get_by_text(door_type).click()
            print(f"✅ تم اختيار نوع الباب: {door_type}")
        except Exception as e:
            print(f"⚠️ خطأ في اختيار نوع الباب: {e}")
            raise
        
        return door_type
    
    def fill_basic_door_info(self, quantity=None, price=None, door_option=None):
        """تعبئة المعلومات الأساسية للباب"""
        if quantity is None:
            quantity = self.get_random_quantity()
        if price is None:
            price = self.get_random_price()
        if door_option is None:
            door_option = random.choice(self.door_options)
        
        print(f"📊 جاري تعبئة المعلومات الأساسية - الكمية: {quantity}, السعر: {price}")
        
        try:
            self.page.get_by_role("spinbutton", name="Quantity").fill(quantity)
            self.page.get_by_role("spinbutton", name="Price").fill(price)
            
            self.page.get_by_text("Door Type").click()
            self.page.get_by_text(door_option).click()
            
            print(f"✅ تم تعبئة المعلومات: كمية={quantity}, سعر={price}, نوع الباب={door_option}")
        except Exception as e:
            print(f"⚠️ خطأ في تعبئة المعلومات الأساسية: {e}")
            raise
        
        return {"quantity": quantity, "price": price, "door_option": door_option}
    
    def fill_dimensions(self, width=None, length=None):
        """تعبئة الأبعاد (العرض والطول)"""
        if width is None:
            width = self.get_random_width()
        if length is None:
            length = self.get_random_length()
        
        print(f"📏 جاري تعبئة الأبعاد - العرض: {width}, الطول: {length}")
        
        try:
            self.page.get_by_role("spinbutton", name="Width").fill(width)
            self.page.get_by_role("spinbutton", name="Length").fill(length)
            print(f"✅ تم تعبئة الأبعاد: {width} x {length}")
        except Exception as e:
            print(f"⚠️ خطأ في تعبئة الأبعاد: {e}")
            raise
        
        return {"width": width, "length": length}
    
    def fill_door_specifications(self, thickness=None, direction=None, temp_type=None, material=None, frame_type=None):
        """تعبئة مواصفات الباب"""
        if thickness is None:
            thickness = self.get_random_thickness()
        if direction is None:
            direction = random.choice(self.directions)
        if temp_type is None:
            temp_type = random.choice(self.temperature_types)
        if material is None:
            material = random.choice(self.color_options)
        if frame_type is None:
            frame_type = random.choice(self.frame_types)
        
        print(f"🔧 جاري تعبئة مواصفات الباب...")
        
        try:
            # Thickness
            self.page.get_by_role("combobox", name="Thickness").click()
            self.page.wait_for_timeout(300)
            self.page.get_by_text(thickness).nth(1).click()
            
            # Direction
            self.page.get_by_text(direction).click()
            
            # Temperature Type
            self.page.get_by_text(temp_type).click()
            
            # Material
            self.page.get_by_text(material).click()
            
            # Frame Type - Select Complete
            self.page.get_by_role("radio", name=frame_type).check()
            
            print(f"✅ تم تعبئة المواصفات: سمك={thickness}, اتجاه={direction}, نوع={temp_type}, مادة={material}")
        except Exception as e:
            print(f"⚠️ خطأ في تعبئة المواصفات: {e}")
            raise
        
        return {
            "thickness": thickness,
            "direction": direction,
            "temperature_type": temp_type,
            "material": material,
            "frame_type": frame_type
        }
    
    def fill_frame_details(self, frame_thickness="2", frame_edges="3"):
        """تعبئة تفاصيل الإطار"""
        print("🖼️ جاري تعبئة تفاصيل الإطار...")
        
        try:
            self.locator("#frameThickness").fill(frame_thickness)
            self.page.get_by_role("combobox", name="Frame Edges").click()
            self.page.wait_for_timeout(300)
            self.page.get_by_text(frame_edges, exact=True).nth(1).click()
            print(f"✅ تم تعبئة تفاصيل الإطار: سمك={frame_thickness}, حواف={frame_edges}")
        except Exception as e:
            print(f"⚠️ خطأ في تعبئة تفاصيل الإطار: {e}")
            raise
    
    def fill_sheet_details(self, external_sheet="Sheet Iron ppgi", external_thickness="10", external_color="WHITE",
                          internal_sheet="Sheet Iron ppgi", internal_thickness="20", internal_color="BLACK"):
        """تعبئة تفاصيل الصفائح"""
        print("📄 جاري تعبئة تفاصيل الصفائح...")
        
        try:
            # External Sheet
            self.page.get_by_text(external_sheet).first.click()
            self.locator("#externalSheetThickness").fill(external_thickness)
            self.locator("#externalSheetColorCode").fill(external_color)
            
            # Internal Sheet
            self.page.get_by_text(internal_sheet).nth(1).click()
            self.locator("#internalSheetThickness").fill(internal_thickness)
            self.locator("#internalSheetColorCode").fill(internal_color)
            
            print(f"✅ تم تعبئة تفاصيل الصفائح")
        except Exception as e:
            print(f"⚠️ خطأ في تعبئة تفاصيل الصفائح: {e}")
            raise
    
    def fill_accessories(self, accessories_type=None, has_window=True, window_shape=None, hinges_count=2):
        """تعبئة بيانات الإكسسوارات"""
        if accessories_type is None:
            accessories_type = random.choice(self.accessories_options)
        if window_shape is None:
            window_shape = random.choice(self.window_options)
        
        print("🔧 جاري تعبئة بيانات الإكسسوارات...")
        
        try:
            # Accessories Type
            self.page.get_by_role("heading", name="Accessories").click()
            self.page.get_by_text(accessories_type).click()
            
            # Window
            if has_window:
                self.page.get_by_role("checkbox", name="Window").check()
                if window_shape != "None":
                    self.page.get_by_text(window_shape).click()
            
            # Hinges
            self.page.get_by_role("heading", name="Hinges").click()
            for _ in range(hinges_count):
                self.page.get_by_role("button", name="+").click()
            
            print(f"✅ تم تعبئة الإكسسوارات: نوع={accessories_type}, نافذة={has_window}")
        except Exception as e:
            print(f"⚠️ خطأ في تعبئة الإكسسوارات: {e}")
            raise
    
    def add_order_and_save(self):
        """إضافة الطلب وحفظه"""
        print("💾 جاري إضافة الطلب وحفظه...")
        
        try:
            self.page.get_by_text("+Add Order").click()
            self.page.wait_for_timeout(1000)
            self.page.get_by_role("button", name="Save").click()
            self.page.wait_for_timeout(3000)
            print("✅ تم حفظ الطلب")
        except Exception as e:
            print(f"⚠️ خطأ في حفظ الطلب: {e}")
            raise
    
    def confirm_order(self):
        """تأكيد الطلب"""
        print("✅ جاري تأكيد الطلب...")
        
        try:
            # انتظار ظهور الـ Modal
            self.page.wait_for_timeout(2000)
            self.page.get_by_role("button", name="Ok").click()
            self.page.wait_for_timeout(2000)
            print("✅ تم تأكيد الطلب بنجاح")
        except Exception as e:
            print(f"⚠️ خطأ في تأكيد الطلب: {e}")
            raise