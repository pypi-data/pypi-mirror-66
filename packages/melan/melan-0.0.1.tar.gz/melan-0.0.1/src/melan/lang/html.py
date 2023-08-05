
import re

# ------------------------------------------------------------------------

def stag(name,arg):
    arg = [ ' %s="%s"' % (k,v) for k,v in arg.items() ]
    return '<%s%s>' % (name,''.join(arg))

def xtag(name,arg):
    arg = [ ' %s="%s"' % (k,v) for k,v in arg.items() ]
    return '<%s%s/>' % (name,''.join(arg))

def btag(name,arg,body):
    arg = [ ' %s="%s"' % (k,v) for k,v in arg.items() ]
    return '<%s%s>\n%s\n</%s>' % (name,''.join(arg), body, name)

def tag(name,arg,body):
    arg = [ ' %s="%s"' % (k,v) for k,v in arg.items() ]
    return '<%s%s>%s</%s>' % (name,''.join(arg),body,name)

# ------------------------------------------------------------------------

def _make_head(cpl):
    out = []
    if 'head.title' in cpl:
        out.append(tag('title',{},cpl['head.title']))
    if 'head.base' in cpl:
        out.append(stag('base',cpl['head.base']))
    for t in cpl.lst('head.meta'): out.append(stag('meta',t))
    for t in cpl.lst('head.link'): out.append(stag('link',t))
    for t in cpl.lst('head.style'): out.append(t)
    for t in cpl.lst('head.script'): out.append(t)

    return btag( 'head', cpl.arg('head'), '\t' + '\n\t'.join(out) )

def _clean(txt):
    return re.sub('\n+','\n',txt)

def wrap(cpl,body):
    return '\n'.join([
        '<!doctype html>',
        btag( 'html', cpl['html'], 
            '\n'.join([
                _make_head(cpl),
                btag( 'body', cpl.arg('body'), _clean(body) )
            ])
        )
    ])

# ------------------------------------------------------------------------

def title(cpl,body,**kw): cpl['head.title'] = body
def base(cpl,body,**kw): cpl['head.base'] = dict(kw)

def meta(cpl,body,**kw): cpl['head.meta'].append(dict(kw))
def link(cpl,body,**kw): cpl['head.link'].append(dict(kw))

def style(cpl,body='',file=None,**kw): 
    if file: body = cpl.readfile(file)
    cpl['head.style'].append(tag( 'style', kw, body ))

def script(cpl,body='',file=None,**kw):
    if file: body = cpl.readfile(file)
    cpl['head.script'].append(tag( 'script', kw, body ))

# ------------------------------------------------------------------------

def h1(body,**kw): return tag('h1',kw,body)
def h2(body,**kw): return tag('h2',kw,body)
def h3(body,**kw): return tag('h3',kw,body)
def h4(body,**kw): return tag('h4',kw,body)

def par(body,**kw): return tag('p',kw,body)
def url(body,**kw): return tag('a',kw,body)
def img(body,**kw): return stag('img',kw)
def nl(body,**kw): return stag('br',kw)

def b(body,**kw): return tag('b',kw,body)
def i(body,**kw): return tag('i',kw,body)
def u(body,**kw): return tag('u',kw,body)
def s(body,**kw): return tag('s',kw,body)
def m(body,**kw): return tag('math',kw,body)

# ------------------------------------------------------------------------

export = {
    'var': {
        'html': {'lang':'en'},
        'head.meta': [
            {'charset': 'utf-8'}
        ]
    },
    'pre': {
        'title': title, 'base': base,
        'meta': meta, 'link': link,
        'style': style, 'script': script
    },
    'doc': {
        'h1': h1, 'h2': h2, 'h3': h3, 'h4': h4,
        'par': par, 'url': url, 'img': img, 'nl': nl,
        'b': b, 'i': i, 'u': u, 's': s, 'm': m
    },
    'wrap': wrap
}
