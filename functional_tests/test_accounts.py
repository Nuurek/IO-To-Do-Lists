from .base import FunctionalTest


class SignUpTest(FunctionalTest):

    def test_sign_up_button_on_home_page(self):
        self.browser.get(self.server_url)