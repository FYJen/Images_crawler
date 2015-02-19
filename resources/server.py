import config
from Queue import Queue

class Server(object):

    def __init__(self):
        self.queue = Queue(config.QUEUE_SIZE)

    def get_queue(self):
        return self.queue

    def populate_queue(self, url_list, job_id, level):
        for url in url_list:
            item = {
                'url': url,
                'job_id': job_id,
                'level': level,
                'parent_url': url
            }
            self.queue.put(item)
