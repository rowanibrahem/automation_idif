import subprocess
import sys

def run_tests():
    """تشغيل اختبارات Playwright"""
    
    print("🚀 بدء تشغيل اختبارات الأتمتة...")
    print("-" * 50)
    
    # تشغيل اختبار standard
    result = subprocess.run([
        sys.executable, "-m", "pytest", 
        "tests/test_final_products.py::test_add_standard_product", 
        "-v", "-s"
    ])
    
    if result.returncode == 0:
        print("\n✅ جميع الاختبارات اكتملت بنجاح!")
    else:
        print("\n❌ حدث خطأ في الاختبارات")
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(run_tests())