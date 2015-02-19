from flask import Flask

class App_Flask(Flask):
    """This class is to override the origianl Flask class's run() method. Mainly
    to take in extra arguments: server and lock.
    """

    def __init__(self, *arg, **kwargs):
        super(App_Flask, self).__init__(*arg, **kwargs)
    
    def run(self, app_server, lock, *arg, **kwargs):
        self.app_server = app_server
        self.lock = lock
        super(App_Flask, self).run(*arg, **kwargs)
