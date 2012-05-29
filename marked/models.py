# -*- coding: utf-8 -*-
from sqlalchemy import Column, Table, Integer, String, DateTime, Text, Boolean, Enum, ForeignKey                                                                            
# from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from marked.database import Base, db_session
from sqlalchemy.orm import deferred, defer, undefer, relationship

from datetime import datetime
from markdown import markdown
from unicodedata import normalize

import re

association_table = Table('page_category_assoc', Base.metadata,
    Column('entry_id', Integer, ForeignKey('entries.entry_id')),
    Column('category_id', Integer, ForeignKey('categories.category_id'))
)

class Entry(Base):
    """docstring for User"""
    __tablename__       = 'entries'
    entry_id            = Column(Integer, primary_key=True)
    _type               = Column('type', Enum('Page', 'Post'), default='Post')
    title               = Column(String, unique=True)
    _slug               = Column('slug', String, unique=True, nullable=False)
    published_at        = Column(DateTime, default=datetime.now)
    created_at          = Column(DateTime, default=datetime.now)
    updated_at          = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    content             = deferred(Column(Text()))
    _html               = Column('html', Text)
    draft               = Column(Boolean, default=False)
    categories          = relationship("Category", 
                            secondary=association_table)
                            # backref="pages")
    
    def __init__(self, title, content, draft):
            # super(Entry, self).__init__()
            self.title      = title
            self.content    = content
            self.draft      = draft
    
    def __repr__(self):
        """docstring for __repr__"""
        return "Entry<%s>" % self._slug
    
    @classmethod
    def get_by_slug(cls, slug):
        """docstring for get_by_slug"""
        return cls.query.filter_by(_slug=slug, _type=cls._my_type).first()
    
    @classmethod
    def get_by_id(cls, page_id):
        """docstring for get_by_id"""
        return cls.query.get(page_id)
    
    @classmethod
    def get_all(cls, limit=None, offset=0):
        """docstring for get_all"""
        # TODO: Don't fetch ALL date (no need for html and mdfield)
        if limit:
            return cls.query.options(defer('_html')).filter_by(_type=cls._my_type).offset(offset).limit(limit)
        else:
            return cls.query.options(defer('_html')).filter_by(_type=cls._my_type)
    
    def save(self):
        """docstring for save"""
        self._slug = self.slug
        self._html = markdown(self.content)
        db_session.add(self)
        db_session.commit()
    
    def delete(self):
        """docstring for delete"""
        db_session.delete(self)
        db_session.commit()
    
    @hybrid_property
    def html(self):
        return self._html if self._html else markdown(self.content)
    
    @hybrid_property
    def slug(self):
        return unicode(self._slug) if self._slug else self.slugify(unicode(self.title))
    
    @classmethod
    def slugify(cls, text, delim=u'-'):
        """Generates an slightly worse ASCII-only slug."""
        _punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.:]+')
        result = []
        for word in _punct_re.split(text.lower()):
            word = normalize('NFKD', word).encode('ascii', 'ignore')
            if word:
                result.append(word)
        return unicode(delim.join(result))

class Post(Entry):
    """docstring for Post"""
    _my_type           = 'Post'
    def __init__(self, title, content, draft):
        super(Post, self).__init__(title, content, draft)
        self._type      = self._my_type

class Page(Entry):
    """docstring for Page"""
    _my_type           = 'Page'
    def __init__(self, title, content, draft):
        super(Page, self).__init__(title, content, draft)
        self._type      = self._my_type
    
    @hybrid_property
    def slug(self):
        """docstring for slug"""
        return super(Page, self).slug
    
    @slug.setter
    def slug(self, slug):
        """docstring for slug"""
        # TODO: Validate the slug
        self._slug = slug
    
    def _validate_url(self, url):
        """docstring for _validate_url"""
        return url

class Category(Base):
    """docstring for Category"""
    __tablename__       = 'categories'
    category_id         = Column(Integer, primary_key=True)
    name                = Column(String(50), unique=True, nullable=False)
    
    def __repr__(self):
        """docstring for __repr__"""
        return "Categories<%s>" % self.name
    
    @classmethod
    def get_by_name(cls, name):
        """docstring for get_by_name"""
        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def get_all(cls, limit=None, offset=0):
        """docstring for get_all"""
        if limit:
            return cls.query.offset(offset).limit(limit)
        else:
            return cls.query.all()

class Redirect(Base):
    """docstring for Redirect"""
    __tablename__       = 'redirects'
    redirect_id         = Column(Integer, primary_key=True)
    _type               = Column('type', Enum('Static', 'Blog'), default='Blog')
    from_slug           = Column(String, unique=True, nullable=False)
    to_slug             = Column(String, unique=True, nullable=False)
    
    def __init__(self, from_slug, to_slug, page_type):
        # super(Redirect, self).__init__()
        self.from_slug  = from_slug
        self.to_slug    = to_slug
        self._type      = page_type

class BaseUser(object):
    """docstring for BaseUser"""
    def __init__(self, arg):
        super(BaseUser, self).__init__()
        self.arg = arg

class User(BaseUser):
    """docstring for User"""
    def __init__(self, arg):
        super(User, self).__init__()
        self.arg = arg
        
        



