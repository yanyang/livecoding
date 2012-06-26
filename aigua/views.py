import os
import datetime
import requests
import json
from aigua import app
from flask import render_template, send_from_directory, redirect, session, request
from requests import post


@app.route('/', defaults={'gistId': None})
@app.route('/<gistId>')
def index(gistId):
    return render_template('index.html', vars=dict(
        gistId = gistId))


@app.route('/save-anonymously', methods=['POST'])
def save_anonymously():

    gist = {
        'description': 'created by water, a live-coding editor (http://water.gabrielflor.it)',
        'public': 'true',
        'files': {
            'water.js': {
                'content': request.form['js']
            },
            'water.css': {
                'content': request.form['css']
            }
        }
    }

    headers = {'content-type': 'application/json', 'accept': 'application/json'}
    r = requests.post('https://api.github.com/gists', data=json.dumps(gist), headers=headers)

    return json.loads(r.text)['html_url']


@app.route('/github-login')
def github_login():
    # take user to github for authentication
    return redirect('https://github.com/login/oauth/authorize?client_id=' + os.getenv('CLIENT_ID') + '&scope=gist')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/img'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


def versioning():
    return datetime.date.today().strftime('%y%m%d')
