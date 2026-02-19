from pages import LoginPage

def test_valid_login(page):
    login_page = LoginPage(page)

    login_page.navigate_baseurl()
    login_page.verify_static_content()
    login_page.enter_username()
    login_page.enter_password()
    login_page.click_login()

    login_page.verify_sucess_login()
    login_page.click_logout_button()
    login_page.verify_static_content()
