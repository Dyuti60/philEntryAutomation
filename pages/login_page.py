from core import ActionManager, WaitManager, KeyboardManager, MouseManager
from assertions import UIAssert
from locators import LoginLocators
from utils.logger import Logger
from config.settings import settings

class LoginPage:
    
    def __init__(self, page):
        self.page=page
        self.action = ActionManager(page)
        self.wait = WaitManager(page)
        self.keyboard = KeyboardManager(page)
        self.assert_ui = UIAssert(page)
        self.mouse = MouseManager(page)

    # Navigate And Click

    def navigate_baseurl(self):
        self.action.goto("/login")
        self.wait.for_network_idle()
        return self
    
    def enter_username(self):
        print("DEBUG USERNAME:", repr(settings.USERNAME))
        self.action.type(LoginLocators.usernameElement,settings.USERNAME)
        return self

    def enter_password(self):
        self.action.type(LoginLocators.passwordElement,settings.PASSWORD)
        return self
    
    def click_login(self):
        self.action.click(LoginLocators.loginbuttonElement)
        return self

    def login_by_username_and_password(self,username:str, password:str):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login
        return self

    def verify_static_content(self):
        self.assert_ui.element_visible(LoginLocators.loginHeadingText)
        self.assert_ui.element_visible(LoginLocators.usernameText)
        self.assert_ui.element_visible(LoginLocators.passwordText)
        self.assert_ui.element_visible(LoginLocators.loginbuttonElement)
        return self


    def verify_sucess_login(self):
        self.mouse.hover(LoginLocators.satsangLogoElement)
        self.wait.wait_for_timeout(200)
        return self

    def click_logout_button(self):
        self.action.click(LoginLocators.logoutElement)
        return self


