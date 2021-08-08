from Modules import Commits, Log

import time
import hashlib
from flask import Flask, render_template, url_for, send_from_directory, request

app = Flask('Portfolio')
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route("/")
def home():
    Log.LogVisit(request)
    return render_template(
            "index.html",
            Events=Commits.GetCommits()
        )


@app.route('/favicon.ico')
@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
