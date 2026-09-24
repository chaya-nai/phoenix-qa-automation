from config import BASE_URL

class ShopPage():
    def __init__(self, page):
        self.page = page
    
    def open(self):
        self.page.goto(f"{BASE_URL}/shop")
    
    def coin(self):
        return self.page.locator("#coin")
    
    def get_coin(self):
        return int(self.page.locator("#coin").text_content())
    
    def shop_item(self, item_name):
        return self.page.locator(".shop-item").filter(has_text=item_name)
    
    def buy(self, item_name):
        self.shop_item(item_name).get_by_role("button", name="Buy").click()
        
    def result(self):
        return self.page.locator("#purchase-result")
    
    def item_price(self, item_name):
        return self.shop_item(item_name).locator(".item-price")
    
    def get_price(self, item_name):
        return int(self.item_price(item_name).text_content())