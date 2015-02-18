from app import app

@app.route('/', methods=['POST'])
def post_jobs():
    return 'post jobs'
    pass

@app.route('/status/<int:id>', methods=['GET'])
def show_status(id):
    return 'show status'
    pass

@app.route('/result/<int:id>', methods=['GET'])
def get_results(id):
    return 'get results'
    pass