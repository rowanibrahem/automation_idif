from playwright.sync_api import Page, expect

class EditProductPage:
    def __init__(self, page: Page):
        self.page = page
        # الـ Selectors من الـ codegen بتاعك
        self.edit_button = page.get_by_role("button", name="edit").first
        self.quantity_input = page.get_by_role("textbox", name="Quantity", exact=True)
        self.name_en_input = page.get_by_role("textbox", name="Product Name in English*")
        self.save_button = page.get_by_role("button", name="Save")

    def edit_first_product(self, new_name, new_qty):
        print(f"📝 جاري تعديل المنتج إلى: {new_name}")
        
        # الضغط على زر التعديل
        self.edit_button.click()
        
        # تعديل الاسم (English Name)
        self.name_en_input.click()
        self.name_en_input.fill(new_name)
        
        # تعديل الكمية
        self.quantity_input.click()
        self.quantity_input.fill(str(new_qty))
        
        # حفظ التغييرات
        self.save_button.click()
        print("✅ تم الضغط على حفظ")

        self.save_button.wait_for(state="hidden", timeout=10000)