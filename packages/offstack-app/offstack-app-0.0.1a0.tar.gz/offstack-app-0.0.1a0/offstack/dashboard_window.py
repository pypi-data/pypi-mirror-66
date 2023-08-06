
from .managers import oAuthManager, DriverManager
from offstack.logger import logger
from .utils import (
    check_access_token,
    request_access_token,
    get_user_credentials,
    request_favorites,
    get_questions,
    display_favorite_question
)

from .constants import(
    CLIENT_ID,
    CLIENT_SECRET,
    REDIRECT_URI,
    SCOPE,
    USERDATA,
    CURRDIR,
    VERSION
)

def display_dashboard(interface, OAuth2Session, Firefox, opts, queue, Gtk):
    interface.add_from_file(CURRDIR+"/resources/dashboard_window.glade")
    dashboard_window = interface.get_object("DashboardWindow")
    dashboard_version_label = interface.get_object("dashboard_version_label")
    interface.connect_signals(DashboardHandlers(interface, OAuth2Session, Firefox, opts, queue))
    dashboard_window.connect("destroy", Gtk.main_quit)
    
    dashboard_version_label.set_text("v.{}".format(VERSION))
    dashboard_window.show()

class DashboardHandlers():
    def __init__(self, interface, OAuth2Session, Firefox, browser_opts, queue):
        self.interface = interface
        self.OAuth2Session = OAuth2Session
        self.Firefox = Firefox
        self.browser_opts = browser_opts
        self.queue = queue
        self.question_textview = self.interface.get_object("question_textview")
        self.answers_textview = self.interface.get_object("answers_textview")
        populate_on_load(self.interface, self.OAuth2Session, self.Firefox, self.browser_opts, self.queue)

    def search_entry_key_release_event(self, entry, event):
        """Event handler, to filter servers after each key release"""
        user_filter_by = entry.get_text()
        server_tree_store = self.interface.get_object("QuestionsListStore")
        tree_view_object = self.interface.get_object("QuestionsTreeView")

        # Creates a new filter from a ListStore/TreeStore
        n_filter = server_tree_store.filter_new()

        # set_visible_func:
        # first_param: filter function
        # seconde_param: input to filter by
        n_filter.set_visible_func(column_filter, data=[self.interface, user_filter_by])
        
        # Apply the filter model to a TreeView
        tree_view_object.set_model(n_filter)

        # Updates the ListStore model
        n_filter.refilter()

    def QuestionsTreeView_cursor_changed(self, listview):
        # Get the selected server
        (model, pathlist) = listview.get_selection().get_selected_rows()

        for path in pathlist :
            tree_iter = model.get_iter(path)
            # the second param of get_value() specifies the column number, starting at 0
            question_id = model.get_value(tree_iter, 0)
            load_content(question_id, self.question_textview, self.answers_textview)
            
def column_filter(model, iterator, data=None):
    """Filter by columns and returns the corresponding rows"""
    interface = data[0]
    data = data[1].lower()
    treeview = interface.get_object("QuestionsTreeView")

    cols = treeview.get_n_columns()
    tags = model.get_value(iterator, 4).split(";")
    tags = [tag.strip().lower() for tag in tags]

    question_title = model.get_value(iterator, 1).lower()
    
    try:
        if data[0] == ":":
            keys = data[1:].split()
            keys = [key.lower() for key in keys]

            if any(tag.startswith(tuple(keys)) for tag in tags):
                return True

    except IndexError:
        if any(tag.startswith(data) for tag in tags) or data in question_title:
            return True

def load_content(question_id, question_textview, answers_textview):
    question, resp_count, answers = display_favorite_question(question_id)

    question_buffer = question_textview.get_buffer()
    question_buffer.set_text(question)

    answers_buffer = answers_textview.get_buffer()
    answers_buffer.set_text(answers)

def cache_favorites(interface, OAuth2Session, Firefox, browser_opts, queue):
    logger.debug("Creating oAuth Session")
    oauth_manager = oAuthManager(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, OAuth2Session, SCOPE)
    oauth_manager.create_session()
    if not check_access_token():
        browser = Firefox(options=browser_opts)

        driver = DriverManager(CLIENT_ID, CLIENT_SECRET, browser)

        user_data = get_user_credentials()

        resp = request_access_token(driver, oauth_manager, user_data)
        if not resp:
            print("Unable to get the access token.")
            return
    
    if request_favorites(oauth_manager):
        return get_questions()
    else:
        return False

def populate_on_load(interface, OAuth2Session, Firefox, browser_opts, queue):
    questions_list = get_questions()
    questions_list_store = interface.get_object("QuestionsListStore")
    
    if not questions_list:
        questions_list = cache_favorites(interface, OAuth2Session, Firefox, browser_opts, queue)
    print("Should be displayed")
    questions_list_store.clear()
    for question in questions_list:
        tags = '; '.join(question["tags"])
        questions_list_store.append([question["question_id"], question["title"], "Yes" if question["score"] else "No", str(question["score"]), tags])