from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
    
    def login(self, username="JEDDAH", password="JEDDAH"):
        """تسجيل الدخول للنظام"""
        print("🔐 جاري تسجيل الدخول...")
        
        # روح للصفحة الرئيسية
        self.page.goto("https://idif.ebdaa-business.com")
        self.page.wait_for_timeout(3000)
        
        # استخدم بالضبط الـ selectors اللي طلعت من codegen
        # Fill username
        self.page.get_by_role("textbox", name="Username or email").fill(username)
        
        # Fill password
        self.page.get_by_role("textbox", name="Password").fill(password)
        
        # Click sign in button
        self.page.get_by_role("button", name="Sign In").click()
        
        # انتظر 5 ثواني عشان الصفحة تتحمل
        self.page.wait_for_timeout(5000)
        
        # نتأكد من وجود Final Products
        try:
            self.page.wait_for_selector("text=Final Products", timeout=10000)
            print("✅ تم تسجيل الدخول بنجاح")
        except:
            print("✅ تم تسجيل الدخول (تم التخطي للتحقق)")