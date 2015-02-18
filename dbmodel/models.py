from app import db

class Job(db.Model):
    __tablename__ = 'job'
    id = db.Column(db.Integer, primary_key=True)
    completed = db.Column(db.Integer, default=0)
    in_process = db.Column(db.Integer, default=0)
    results = db.relationship('Result', backref='results', lazy='dynamic')

    def __repr__(self):
        return '<Job %r>' % (self.id)

class Result(db.Model):
    __tablename__ = 'result'
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    img_url = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Result %r: job-%r>' % (self.id, self.job_id)
