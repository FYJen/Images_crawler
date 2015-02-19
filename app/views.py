from flask import request
from flask import jsonify

import config
from app import app
from app import db
from dbmodel import models
from lib import status as custom_status
from resources.worker import Worker

@app.route('/', methods=['POST'])
def post_jobs():
    urls = request.files['inputs'].read().split()

    # Create job entry.
    job = models.Job()
    db.session.add(job)
    db.session.commit()

    app.app_server.populate_queue(urls, job.id, 1)

    queue = app.app_server.get_queue()
    for i in range(config.NUM_WORKER):
        t = Worker(queue, app.lock)
        t.daemon = True
        t.start()

    result = custom_status.HTTPOk(result='job_id: %s' % job.id)

    return jsonify(result.toDict())

@app.route('/status/<int:_id>', methods=['GET'])
def show_status(_id):
    job = models.Job.query.get(_id)

    if job:
        return_dict = {
            'completed': job.completed,
            'in_process': job.in_process
        }

        result = custom_status.HTTPOk(result=return_dict)
    else:
        return_str = 'No status found for the given job_id %d' % _id
        result = custom_status.ResourceNotFound(result=return_str)

    return jsonify(result.toDict())

@app.route('/result/<int:_id>', methods=['GET'])
def get_results(_id):
    job = models.Job.query.get(_id)
    if job:
        urls = [str(result.img_url) for result in job.results.all()]
        urls = list(set(urls)) # Remove duplicate.
        return_dict = {
            'count': len(urls),
            'img_links': urls
        }

        result = custom_status.HTTPOk(result=return_dict)
    else:
        return_str = 'No result found for the given job_id %d' % _id
        result = custom_status.ResourceNotFound(result=return_str)

    return jsonify(result.toDict())
