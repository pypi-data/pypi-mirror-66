import os
from queue import Queue

from requests_oauthlib import OAuth2Session
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
opts = Options()
opts.headless = True
opts.add_argument('--no-sandbox')
assert opts.headless  # Operating in headless mode

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import  Gtk, Gdk, GObject

from .logger import logger
from .constants import CONFIG_DIR, USERDATA, CURRDIR
from .utils import check_user_credentials

from .login_window import display_login
from .dialog_window import DialogHandlers
from .dashboard_window import display_dashboard

def init():
    queue = Queue()
    interface = Gtk.Builder()

    # Apply CSS
    style_provider = Gtk.CssProvider()
    style_provider.load_from_path(CURRDIR+"/resources/main.css")

    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        style_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

    interface.add_from_file(CURRDIR+"/resources/dialog_window.glade")
    interface.connect_signals(DialogHandlers(interface, queue))
    
    # dial = interface.get_object("MessageDialog")

    # dial.show()

    if not check_user_credentials(): 
        display_login(interface, OAuth2Session, Firefox, opts, queue, Gtk)
    else:
        display_dashboard(interface, OAuth2Session, Firefox, opts, queue, Gtk)

    Gtk.main()