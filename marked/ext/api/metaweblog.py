# -*- coding: utf-8 -*-
"""
http://xmlrpc.scripting.com/metaWeblogApi.html
This is the metaWeblog API to marked
"""
from flask import Blueprint, url_for
from flaskext.xmlrpc import XMLRPCHandler, Fault
from marked.models import BlogPage, StaticPage, Category

# TODO: NO sqlalchemy outside of models
from sqlalchemy.exc import IntegrityError

metaweblog = Blueprint('metaweblog', __name__)

handler = XMLRPCHandler('api')
handler.connect(metaweblog, '/xml/rpc')

mwl  = handler.namespace('metaWeblog')
blogger     = handler.namespace('blogger')

@mwl.register
def newPost(blog_id, username, password, struct, publish):
    """docstring for newPost"""
    print '---\nrunning metaWeblog.newPost'
    if blog_id == 'Static':
        page = StaticPage(title=struct['title'], content=struct['description'], draft=not publish)
        page.slug = struct['link']
    else:
        page = BlogPage(title=struct['title'], content=struct['description'], draft=not publish)
    
    if 'categories' in struct:
        page.categories = [Category.get_by_name(cat) for cat in struct['categories']]
    else:
        page.categories = []
    
    try:
        page.save()
    except IntegrityError:
        raise Fault("DBase Error", "Title not unique")
    else:
        return page.slug

@mwl.register
def editPost(post_id, username, password, struct, publish):
    """docstring for editPost"""
    print '---\nrunning metaWeblog.editPost'
    page = BlogPage.get_by_slug(post_id)
    page.title      = struct['title']
    page.content    = struct['description']
    page.draft      = not publish
    if 'categories' in struct:
        page.categories = [Category.get_by_name(cat) for cat in struct['categories']]
    else:
        page.categories = []
    try:
        page.save()
    except IntegrityError:
        raise Fault("DBase Error", "Title not unique")
    else:
        return True

@mwl.register
def getPost(post_id, username, password):
    """docstring for getPost"""
    print '---\nrunning metaWeblog.getPost'
    return page_to_struct(BlogPage.get_by_slug(post_id))

@mwl.register
def getCategories(blog_id, username, password):
    """docstring for getCategories"""
    print '---\nrunning metaWeblog.getCategories'
    return [cat.name for cat in Category.get_all()]

@mwl.register
def getRecentPosts(blog_id, username, password, numberOfPosts):
    """docstring for getRecentPosts"""
    print '---\nrunning metaWeblog.getRecentPosts'
    if blog_id == 'Static':
        return [page_to_struct(page) for page in StaticPage.get_all(numberOfPosts)]
    else:
        return [page_to_struct(page) for page in BlogPage.get_all(numberOfPosts)]

@mwl.register
def newMediaObject():
    """docstring for newMediaObject"""
    print '---\nrunning metaWeblog.newMediaObject'
    raise Fault("Not Implemented Here", "Media Uploading is not supported here.")

def page_to_struct(page):
    """docstring for page_to_struct"""
    print '---\nrunning metaWeblog.page_to_struct'
    struct                  = {}
    struct['title']         = page.title
    struct['link']          = page.slug #url_for('page', slug=page.slug)
    struct['postid']        = page.slug
    struct['description']   = page.content
    struct['dateCreated']   = page.created_at
    struct['categories']    = [cat.name for cat in page.categories]
    struct['userid']        = 1
    return struct

@blogger.register
def deletePost(appKey, post_id, username, password, publish):
    """docstring for deletePost"""
    page = BlogPage.get_by_slug(post_id)
    try:
        page.delete()
    except IntegrityError:
        raise Fault("DBase Error", "No success...")
    else:
        return True

@blogger.register
def getUserInfo(appKey, username, password):
    """docstring for getUserInfo"""
    raise Fault("Not Implemented Here", "This is not supported here.")

@blogger.register
def getUsersBlogs():
    """docstring for getUsersBlogs"""
    raise Fault("Not Implemented Here", "This is not supported here.")

