from app import app
from threading import Semaphore
from resources.server import Server

if __name__ == '__main__':
    app_server = Server()
    lock = Semaphore()
    app.run(app_server, lock, debug=True)
