import subprocess
import sys

def run_tests():
    """تشغيل اختبارات Playwright"""
    
    print("Start Running Tests")
    print("-" * 50)
    
    # تشغيل اختبار standard
    result = subprocess.run([
        sys.executable, "-m", "pytest", 
        "tests/test_final_products.py::test_add_standard_product", 
        "-v", "-s"
    ])
    
    if result.returncode == 0:
        print("\n✅ All tests passed successfully!")
    else:
        print("\n❌ An error occurred in the tests")
    
    return result.returncode

if __name__ == "__main__":
    sys.exit(run_tests())