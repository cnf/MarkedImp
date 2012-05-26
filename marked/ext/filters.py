# -*- coding: utf-8 -*-
from marked import app

@app.template_filter('datetimeformat')
def datetimeformat(value, format='%A, %d of %B %Y %H:%M'):
    return value.strftime(format)
