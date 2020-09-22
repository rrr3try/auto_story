from time import sleep

import redis
from flask import Flask, request, jsonify, render_template
from rq import Queue
from rq.exceptions import NoSuchJobError
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from worker import download_images_task

app = Flask(__name__, static_url_path="/static", static_folder="static")
task_queue = Queue(
    "default",
    connection=redis.from_url('redis://127.0.0.1:6379'),
    default_timeout=3600,
    is_async=True,
)


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

            return jsonify(job.result)
        else:
            return jsonify({"id": task_id,
                            "status": "processing",
                            "result": f"/results/{task_id}"}), 202
    except (NoSuchJobError, AttributeError):
        abort(404)

    return render_template("index.html", stories=[{"image_url": "...", "text": "some text"},
                                                  {"image_url": "...", "text": "some text"}])


if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=True)
