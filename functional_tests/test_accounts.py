from .base import FunctionalTest


class AccountsTest(FunctionalTest):

    def test_sign_up(self):
        self.browser.get(self.server_url)
        self.browser.find_element_by_link_text('Sign up').click()
        form = self.browser.find_element_by_id('signup-form')
        form.find_element_by_name('username').send_keys('test_user')
        form.find_element_by_name('email').send_keys('test@gmail.com')
        form.find_element_by_name('password').send_keys('test_password')
        form.find_element_by_name('confirm_password').send_keys('test_password')
        form.find_element_by_id('signup-submit').click()
        self.assertTrue('accounts/register/success' in self.browser.current_url)

    def test_login(self):
        self.browser.get(self.server_url)
        self.browser.find_element_by_name('username').send_keys('test_user')
        self.browser.find_element_by_name('password').send_keys('test_password')
        self.browser.find_element_by_id('login-submit').click()
        self.assertEqual(self.browser.current_url, self.server_url + '/')