import time

class Config:
    BASE_URL = "https://idif.ebdaa-business.com"
    
    # حسابات مختلفة
    class Users:
        JEDDAH = {"username": "JEDDAH", "password": "JEDDAH"}
        SALES = {"username": "SALES", "password": "SALES"}
        RIYADH = {"username": "RIYADH", "password": "RIYADH"}
        PRODUCTION = {"username": "PRODUCTION", "password": "PRODUCTION"}
        PURCHASES = {"username": "PURCHASES", "password": "PURCHASES"}
    
    # بيانات المنتج
    @staticmethod
    def get_product_code():
        return f"AUTO{int(time.time())}"
    
    @staticmethod
    def get_product_name():
        return f"منتج اوتوماتيك {int(time.time())}"
    
    @staticmethod
    def get_manufacturing_code():
        return f"MAN{int(time.time())}"