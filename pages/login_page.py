from config import BASE_URL

class LoginPage:
    def __init__(self, page):
        self.page = page
    
    def open(self):
        self.page.goto(f"{BASE_URL}/login")
        
    def input_username(self, username):
        self.page.locator("#username").fill(username)
        
    def input_password(self, password):
        self.page.locator("#password").fill(password)
    
    def login(self):
        self.page.get_by_role('button', name="Login").click()
    
    def message(self, message):
        return self.page.get_by_text(message)
        