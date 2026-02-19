class LoginLocators:
    # ========================
    # Elements
    # ========================
    usernameElement="input[formcontrolname='username']"
    passwordElement="input[formcontrolname='password']"
    loginbuttonElement=".login-button.sat-primary-btn"
    logoutIconElement=".side-tab-logout-icon"
    logoutElement="//div[contains(@class,'side-tab-title') and contains(text(),'Logout')]"
    satsangLogoElement="//div[@class='title-img']"

    # ========================
    # Static Content
    # ========================
    loginHeadingText="//span[@class='login-title-text' and contains(text(),'Login to Satsang Philanthrophy')]"
    usernameText="//span[@class='input-level-text' and contains(text(),'Username *')]"
    passwordText="//span[@class='input-level-text' and contains(text(),'Password *')]"