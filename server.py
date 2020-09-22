from flask import Flask, request, jsonify, render_template
from werkzeug.utils import redirect


app = Flask(__name__, static_url_path="/static", static_folder="static")


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html",)
    elif request.method == 'POST':
        print(request.form['text'])
        return redirect("/result", code=302)


@app.route('/result/<task_id>', methods=['GET'])
def result(task_id):
    return render_template("index.html", stories=[{"image_url": "...", "text": "some text"},
                                                  {"image_url": "...", "text": "some text"}])


if __name__ == '__main__':
    app.run(host="127.0.0.1", debug=True)
