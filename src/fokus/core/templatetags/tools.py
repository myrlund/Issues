# -*- coding: utf8 -*-

from django import template
from django.template import loader, Node, TemplateSyntaxError, Variable
from django.template.context import Context
from django.template.defaultfilters import slugify as _slugify, stringfilter

import re

register = template.Library()

def slugify(value):
    for s, r in ASCII:
        value = value.replace(s, r)
    return _slugify(value)
slugify.is_safe = True
slugify = stringfilter(slugify)

@register.filter
def verbose_name(instance, field_name):
    return instance._meta.get_field(field_name).verbose_name

@register.filter
def smart_trim(text, length=70):
    trim_keep = ['.', '!', '?']
    trim_discard = [' ', ',']
    trim = trim_keep + trim_discard
    
    # Start at length and search backwards
    if len(text) <= length:
        return text
    else:
        i = []
        for symbol in trim:
            i.append((text.rfind(symbol, 0, length), symbol))
        i = max(i)
        i, symbol = i
        
        if symbol in trim_keep:
            i += 1
        return text[0:i]
        
        print "MAX in '%s': %d - en '%s'" % (text, i[0], i[1])

@register.filter
def verbosejoin(list, default='-'):
    l = len(list)
    if l == 0:
        return default
    elif l == 1:
        return list[0]
    else:
        str = u"%s og %s" % (list[-2], list[-1])
        
        if l > 2:
            for i in range(l-2):
                str = u"%s, %s" % (list[i], str)
        return str

class TagNode(Node):
    type = Variable('""')
    closed = Variable('""')
    
    def __init__(self, tag, nodelist, title, closed=False, type=None):
        self.tag = tag
        self.title = Variable(title)
        if type:
            self.type = Variable(type)
        if closed:
            self.closed = Variable(closed)
        self.nodelist = nodelist
        
    def render(self, context):
        inner = self.nodelist.render(context)
        t = loader.get_template('issues/core/%s.html' % self.tag)
        if self.closed:
            self.closed = self.closed.resolve(context)
        context = Context({
            'title': self.title.resolve(context),
            'closed': self.closed,
            'type': self.type.resolve(context),
            'inner': inner,
        })
        return t.render(context)

def tag(tag, parser, token):
    nodelist = parser.parse(('end%s' % tag,))
    parser.delete_first_token()
    
    c = token.split_contents()[1:]
    
    title = None
    type = None
    closed = False
    
    try:
        title = c.pop(0)
        if tag == 'article':
            type = c.pop(0)
        closed = c.pop(0)
        
    except IndexError:
        if not title:
            raise TemplateSyntaxError, "%s tag needs title" % tag
    
    return TagNode(tag, nodelist, title=title, type=type, closed=closed)

@register.tag
def section(parser, token):
    return tag('section', parser, token)

@register.tag
def article(parser, token):
    return tag('article', parser, token)

def split_token(token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise TemplateSyntaxError, "%r tag requires arguments." % token.contents.split()[0]
    
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise TemplateSyntaxError, "%r tag had invalid arguments." % tag_name
    
    return m.groups()

ASCII = (
    (u'æ', 'ae'),
    (u'Æ', 'AE'),
    (u'ø', 'o'),
    (u'Ø', 'O'),
    (u'å', 'a'),
    (u'Å', 'A'),
)
