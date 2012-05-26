# -*- coding: utf-8 -*-
from marked import app
from flask import render_template, request, redirect, url_for,\
                    make_response

from marked.models import BlogPage, StaticPage

import os

@app.route('/favicon.ico')
def favicon():
    """docstring for favicon"""
    return 'not here', 404

@app.route('/rsd.xml')
def rsd_xml():
    """docstring for rsd_xml"""
    return render_template('extra/rsd.xml')

@app.route('/')
def index():
    return redirect('/pages')

@app.route('/pages')
def pages():
    """docstring for pages"""
    page_list = BlogPage.get_all()
    return render_template('pages.html', page_list=page_list)

@app.route('/page/<slug>')
def page(slug):
    """docstring for show_page"""
    page = BlogPage.get_by_slug(slug)
    response = make_response(render_template('page.html', page=page))
    response.headers['Last-Modified'] = page.updated_at.strftime('%a, %d %b %Y %H:%M:%S GMT')
    return response

@app.route('/<path:slug>')
def static_page(slug):
    """docstring for static_page"""
    page = StaticPage.get_by_slug(slug)
    if page:
        response = make_response(render_template('page.html', page=page))
        response.headers['Last-Modified'] = page.updated_at.strftime('%a, %d %b %Y %H:%M:%S GMT')
        return response
    else:
        return render_template('404.html'), 404

