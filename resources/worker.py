import requests
import urlparse
from threading import Thread
from bs4 import BeautifulSoup

import config
from app import db
from dbmodel import models

class Worker(Thread):
    
    def __init__(self, queue, lock, *arg, **kwargs):
        super(Worker, self).__init__(*arg, **kwargs)
        self.queue = queue
        self.lock = lock
        self.image_suffix = config.IMAGE_SUFFIX
        self.levle_to_stop = config.LEVEL_TO_STOP

    def _create_new_item(self, url, job_id, level, parent_url):
        return {
            'job_id': job_id,
            'url': url,
            'level': level,
            'parent_url': parent_url
        }

    def process_item(self, item):
        url = item['url']
        parent_url = item['parent_url']
        job_id = item['job_id']
        level = item['level']

        try:
            html_text = requests.get(url).text
        except Exception:
            # Passively skip invalid URLs.
            return

        # Create a critical section while updating job status.
        self.lock.acquire()
        job = models.Job.query.get(job_id)
        job.in_process += 1
        db.session.add(job)
        db.session.commit()
        self.lock.release()

        soup = BeautifulSoup(html_text)

        for link in soup.find_all('a'):
            href = urlparse.urljoin(parent_url, link.get('href'))
            
            # Add new link if and only if our current recusive level is lower than
            # what we have defined in the config. In this case, it is 2.
            if href and level < self.levle_to_stop:
                href_parsed = urlparse.urlparse(href)
                new_parent_url = '://'.join([href_parsed.scheme, href_parsed.netloc])
                new_level = level + 1

                new_item = self._create_new_item(href, job_id, new_level, new_parent_url)
                
                # Add to queue.
                self.queue.put(new_item)

        for link in soup.find_all('img'):
            src = urlparse.urljoin(parent_url, link.get('src'))

            for ending in self.image_suffix:
                if src.endswith(ending):
                    result = models.Result(job_id=job_id, img_url=str(src))
                    db.session.add(result)

        # Update status and commit to DB.
        self.lock.acquire()
        job = models.Job.query.get(job_id)
        job.in_process -= 1
        job.completed += 1
        db.session.add(job)
        db.session.commit()
        self.lock.release()

    def run(self):
        while True:
            item = self.queue.get()
            self.process_item(item)
            self.queue.task_done()
