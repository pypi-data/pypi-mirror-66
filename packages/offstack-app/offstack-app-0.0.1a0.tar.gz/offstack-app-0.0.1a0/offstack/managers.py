import time

# Third party packages
from requests_oauthlib import OAuth2Session
from getpass import getpass, getuser
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

from offstack.logger import logger

from .constants import (
    BASE_API
)

opts = Options()
opts.headless = True
opts.add_argument('--no-sandbox')

class DriverManager:
    def __init__(self, client_id, client_secret, bot_instance):
        self.driver = bot_instance
        self.client_id = client_id
        self.client_secret = client_secret
        
    def _go_to(self, authorization_url):
        logger.debug("Driver going to: {}".format(authorization_url))
        self.driver.get(authorization_url)

    def _type(self, *args):
        logger.debug("Typing user email and password.")
        for each_input in args:
            # self.driver.type(each_input['value'], xpath=each_input['xpath'])
            field = self.driver.find_element_by_xpath(each_input['xpath'])
            field.send_keys(each_input['value'])

    def _click(self, login_button_xpath):
        logger.debug("Clicked on login button.")
        submit_button = self.driver.find_elements_by_xpath(login_button_xpath)[0]
        submit_button.click()

    def _get_current_url(self):
        logger.debug("Current URL: {}".format(self.driver.current_url))
        time.sleep(2)
        return self.driver.current_url

    def _quit(self):
        logger.debug("Driver process ended.")
        self.driver.quit()
        
class oAuthManager:
    def __init__(self, client_id, client_secret, redirect_uri, oauth_session, args_scope):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = args_scope
        self.oauth_session = oauth_session
        self.oauth = None
        self.authorization_url = ''
        self.state = ''

    def create_session(self):
        logger.debug("Created oAuth Session.")
        self.oauth = self.oauth_session(self.client_id, redirect_uri=self.redirect_uri, scope=self.scope)

    def get_authorization_state_url(self):
        vars_ = self.oauth.authorization_url('https://stackoverflow.com/oauth/dialog')
        logger.debug("Getting authorization url: {}".format(vars_[0]))
        self.authorization_url, self.state = vars_

    def extract_state_token(self, current_url):
        attempts = 3
        while not attempts == 0:
            try:
                access_token, state = current_url.split("#")[1].split("&")
                access_token = access_token.split("=")[1]
                state = state.split("=")[1]
                logger.debug("Extracted access_token: {}".format(access_token))
                logger.debug("Extracted state: {}".format(state))
                return (access_token, state)
                # attempts = 0
            except:
                attempts -= 1
                time.sleep(2)
                logger.debug("[!] Unable to extract access_token and state.")
    
    def fetch_from_api(self, access_token):
        filter = "!)5bKRrkYVUeqn(O3dIVXK4gH800i"
        url = BASE_API + "me/favorites?pagesize=100&order=desc&sort=added&site=stackoverflow&filter={0}&access_token={1}&key={2}".format(filter, access_token, self.client_secret)
        logger.debug("Fetching from API: {}".format(url))
        return self.oauth.get(url)