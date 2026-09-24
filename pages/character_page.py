from config import BASE_URL

class CharacterPage:
    def __init__(self, page):
        self.page = page
    
    def open(self):
        self.page.goto(f"{BASE_URL}/character")
    
    def coin(self):
        return self.page.locator("#coin")
    
    def get_coin(self):
        return int(self.page.locator("#coin").text_content())
    
    def battle(self):
        self.page.get_by_role("button", name="Battle").click()
        
    def battle_result(self):
        return self.page.get_by_text("Battle Won", exact=False)
    
    def result(self):
        return self.page.locator("#battle-result")