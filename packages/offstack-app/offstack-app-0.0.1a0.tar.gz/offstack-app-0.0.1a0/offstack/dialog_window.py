from threading import Thread

class DialogHandlers():
    def __init__(self, interface, queue):
        self.interface = interface
        self.queue = queue

        thread = Thread(target=listener, args=[self.interface, self.queue])
        thread.daemon = True
        thread.start()

    def close_dialog_button_clicked(self, button):
        self.interface.get_object("MessageDialog").hide()

    def MessageDialog_delete_event(self, window, event):
        """On Delete handler is used to hide the dialog and so that it successfully renders next time it is called

        -Returns:Boolean
        - It needs to return True, otherwise the content will not re-render after closing the window
        """
        if window.get_property("visible") is True:
            window.hide()
            return True

def listener(interface, queue):
    dialog_header = interface.get_object("dialog_header")
    primary_text_title = interface.get_object("primary_text_title")
    message_dialog_spinner = interface.get_object("message_dialog_spinner")
    while True:
        item = queue.get()
        if item["create_user"]:
            if not item["create_user"]["response"]:
                dialog_header.set_text("Error")
                primary_text_title.set_text("Unable to extract token! (It could be related to incorrect credentials)")
                message_dialog_spinner.hide()
            else:
                dialog_header.set_text("Setup is complete!")
                primary_text_title.hide()
                message_dialog_spinner.hide()
                