import redis
from flask import Flask, request, render_template
from rq import Queue
from rq.exceptions import NoSuchJobError
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from worker import download_images_task
from db import init_db, get_db


app = Flask(__name__, static_url_path="/static", static_folder="static")
app.config['DATABASE'] = "demo.sqlite"


with app.app_context():
    init_db()

task_queue = Queue(
    "default",
    connection=redis.from_url('redis://127.0.0.1:6379'),
    default_timeout=3600,
    is_async=True,
)


def save_story(text, keywords):
    keywords_query = "INSERT INTO keyword(story_id, text) VALUES(?, ?)"
    text_query = "INSERT INTO story(text) VALUES(?)"
    cursor = get_db().execute(text_query, (text, ))
    story_id = cursor.lastrowid
    print("SID", story_id)
    get_db().executemany(keywords_query, ((story_id, keyword) for keyword in keywords))
    get_db().commit()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html",)
    elif request.method == 'POST':
        job = task_queue.enqueue(download_images_task, (request.form['text']))
        return redirect(f"/result/{job.id}", code=302)


@app.route('/result/<task_id>', methods=['GET'])
def result(task_id):
    try:
        job = task_queue.fetch_job(task_id)
        if job.is_finished:
            text, keywords, images = job.result
            save_story(text, keywords)
            return render_template("index.html", images=images, text=text)
        else:
            return render_template("index.html", processing=True), 202
    except (NoSuchJobError, AttributeError):
        abort(404)


if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=True)
