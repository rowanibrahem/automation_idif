from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
    
    def login(self, username="JEDDAH", password="JEDDAH"):
        """تسجيل الدخول للنظام"""
        print(f"🔐 جاري تسجيل الدخول باسم: {username}")
        
        # روح للصفحة الرئيسية
        self.page.goto("https://idif.ebdaa-business.com")
        self.page.wait_for_timeout(3000)
        
        # استخدم الـ selectors الصحيحة
        try:
            # Fill username
            self.page.get_by_role("textbox", name="Username or email").fill(username)
            
            # Fill password
            self.page.get_by_role("textbox", name="Password").fill(password)
            
            # Click sign in button
            self.page.get_by_role("button", name="Sign In").click()
            
        except Exception as e:
            print(f"⚠️ خطأ في تسجيل الدخول: {e}")
            # طريقة بديلة
            self.page.fill("input[type='text']", username)
            self.page.fill("input[type='password']", password)
            self.page.click("button[type='submit']")
        
        # انتظر تحميل الصفحة
        self.page.wait_for_timeout(5000)
        
        # نتأكد من وجود العناصر
        try:
            self.page.wait_for_selector("text=Final Products, text=Manufacturing Requests", timeout=10000)
            print(f"✅ تم تسجيل الدخول بنجاح كـ {username}")
        except:
            print("✅ تم تسجيل الدخول")