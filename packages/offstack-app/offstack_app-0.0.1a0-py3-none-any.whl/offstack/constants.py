import os
import getpass

try:
    USER = os.environ["SUDO_USER"]
except KeyError:
    USER = getpass.getuser()

CURRDIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_DIR = os.path.join(os.path.expanduser("~{0}".format(USER)), ".offstack")
FAVORITES = os.path.join(CONFIG_DIR, "favorites.json")
USERDATA = os.path.join(CONFIG_DIR, ".userdata")

VERSION = "0.0.1-alpha"
CLIENT_ID = '17218'
CLIENT_SECRET = 'vrkGpneBMkEkA7E*mVCynw(('
REDIRECT_URI = 'https://stackexchange.com/oauth/login_success'
SCOPE = ['no_expiry'] 
BASE_API = "https://api.stackexchange.com/2.2/"