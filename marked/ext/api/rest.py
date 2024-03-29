# -*- coding: utf-8 -*-
"""
This is the REST API to marked
http://flask.pocoo.org/snippets/45/ Handling Accept Headers
"""
from flask import Blueprint, jsonify, request, Response
from marked.models import Page, Post

rest = Blueprint('rest', __name__)

@rest.route('/rest')
def index():
    """docstring for index"""
    # TODO: Return xml/json describing the API?
    return 'GOOD!'

@rest.route('/rest/auth')
def auth():
    """docstring for auth"""
    return jsonify( token='E053C9A4-03A3-4B68-A119-8BF30FDA5094')

@rest.route('/rest/test', methods=['GET', 'POST', 'PUT', 'DELETE'])
def test():
    """docstring for test"""
    # TODO: return the sessions auth string
    auth = request.authorization
    if not auth:
        return Response(
            'Could not verify your access level for that URL.\n'
            'You have to login with proper credentials', 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'})
    else:
        print auth.username, " ", auth.password
        return jsonify(authstring="authstring", 
                username=auth.username,
                password=auth.password)

@rest.route('/rest/page/<path:slug>', methods=['GET'])
def page_get(slug):
    """docstring for page_get"""
    post = StaticPage.get_by_slug(slug)
    return jsonify(
            id = post.slug,
            date = str(post.published_at),
            content = post.content)

@rest.route('/rest/post/<slug>', methods=['GET'])
def post_get(slug):
    """docstring for post_get"""
    post = BlogPage.get_by_slug(slug)
    return jsonify(
            id = post.slug,
            date = str(post.published_at),
            content = post.content)

# @rest.route('/category')