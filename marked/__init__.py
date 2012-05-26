# -*- coding: utf-8 -*-
from flask import Flask, render_template                                              

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.teardown_request
def remove_db_session(exception):
   db_session.remove()

import marked.views

from marked.ext.api.metaweblog import metaweblog
app.register_blueprint(metaweblog, url_prefix='/api')

from marked.ext.api.rest import rest
app.register_blueprint(rest, url_prefix='/api')

import marked.ext.filters
if app.debug == True:
    import marked.admin

from marked.database import db_session