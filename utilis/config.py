class Config:
    BASE_URL = "https://idif.ebdaa-business.com"
    USERNAME = "JEDDAH"
    PASSWORD = "JEDDAH"
    
    # بيانات المنتج
    @staticmethod
    def get_product_code():
        import time
        return f"AUTO{int(time.time())}"
    
    @staticmethod
    def get_product_name():
        import time
        return f"منتج اوتوماتيك {int(time.time())}"