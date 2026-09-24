from config import BASE_URL

class InventoryPage:
    def __init__(self, page):
        self.page = page
        
    def open(self):
        self.page.goto(f"{BASE_URL}/inventory")
    
    def get_coin(self):
        coin = int(self.page.locator("#coin").text_content())
        return coin
    
    def get_equipped_outfit(self):
        outfit = self.page.locator("#equipped-outfit").text_content()
        return outfit
    
    def equip(self, item_name):
        item = self.page.locator(".inventory-item").filter(has_text=item_name)
        item.get_by_role("button", name="Equip").click()
        
    def coin(self):
        return self.page.locator("#coin")

    def equipped_outfit(self):
        return self.page.locator("#equipped-outfit")
    
    def item(self, item_name):
        return self.page.locator(".inventory-item").filter(has_text=item_name)
    
    def equip_result(self):
        return self.page.locator("#equip-result")
    
    