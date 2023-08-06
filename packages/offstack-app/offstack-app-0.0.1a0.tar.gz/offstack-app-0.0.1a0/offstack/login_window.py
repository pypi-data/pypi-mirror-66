import time
import concurrent.futures
from threading import Thread

from .dashboard_window import display_dashboard
from .managers import oAuthManager, DriverManager
from .utils import request_access_token, check_user_credentials
from .logger import logger
from .constants import (
    CLIENT_ID,
    CLIENT_SECRET,
    REDIRECT_URI,
    SCOPE,
    VERSION,
    USERDATA,
    CURRDIR,

)

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import  GObject as obj

def display_login(interface, OAuth2Session, Firefox, opts, queue, Gtk):
    interface.add_from_file(CURRDIR+"/resources/login_window.glade")
    login_window = interface.get_object("LoginWindow")
    login_version_label = interface.get_object("login_version_label")
    interface.connect_signals(LoginHandlers(interface, OAuth2Session, Firefox, opts, queue, Gtk))
    login_window.connect("destroy", Gtk.main_quit)

    login_version_label.set_text("v.{}".format(VERSION))
    login_window.show()

class LoginHandlers:
    def __init__(self, interface, OAuth2Session, Firefox, browser_opts, queue, Gtk):
        self.interface = interface
        self.OAuth2Session = OAuth2Session
        self.Firefox = Firefox
        self.browser_opts = browser_opts
        self.queue = queue
        self.gtk = Gtk

    def login_button_clicked(self, button):
        email = self.interface.get_object('login_username_entry').get_text().strip()
        password = self.interface.get_object('password_username_entry').get_text().strip()

        message_dialog = self.interface.get_object("MessageDialog")
        dialog_header = self.interface.get_object("dialog_header")
        primary_text_title = self.interface.get_object("primary_text_title")
        message_dialog_spinner = self.interface.get_object("message_dialog_spinner")

        dialog_header.set_text("Intializing profile")  
        primary_text_title.set_text("Saving credentials and getting access token...")  
        message_dialog_spinner.show()

        message_dialog.show()

        if not len(email) == 0 and not len(password) == 0:          
            thread = Thread(target=save_access_token, args=[self.interface, self.Firefox, self.browser_opts, self.OAuth2Session, email, password, self.queue, self.gtk])
            thread.daemon = True
            thread.start()
        else:
            print("some of the fields were left empty")

    def need_help_login_label_clicked(self, label, link):
        popover = self.interface.get_object("need_help_popover_menu")
        popover.show()

def save_access_token(interface, Firefox, browser_opts, OAuth2Session, email, password, queue, gtk): 
    with concurrent.futures.ThreadPoolExecutor() as executor:
        params_dict = {
            "email": email,
            "password": password
        }
        future = executor.submit(create_user_file, email, password)
        return_value = future.result()

        if not return_value:
            print("Could not save to file")
            return

        browser = Firefox(options=browser_opts)
        oauth_manager = oAuthManager(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, OAuth2Session, SCOPE)
        oauth_manager.create_session()
        driver = DriverManager(CLIENT_ID, CLIENT_SECRET, browser)
        user_data = email, password
        response = request_access_token(driver, oauth_manager, user_data)
        queue.put({"create_user": {"response":response}})
        if response:
            obj.idle_add(display_dashboard, interface, OAuth2Session, Firefox, browser_opts, queue, gtk)
            login_window = interface.get_object("LoginWindow")
            login_window.hide()

def create_user_file(email, password):
    try:
        with open(USERDATA, 'w') as f:
            f.write("{0}\n{1}".format(email, password))
            print()
            print("User data saved to file!")
            logger.debug("User data saved to file!")
            return True
    except:
        return False
