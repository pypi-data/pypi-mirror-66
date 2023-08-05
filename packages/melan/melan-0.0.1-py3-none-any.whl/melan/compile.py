
from .parse import Parser
from importlib import import_module
from warnings import warn
from os import getcwd
import os.path as op
import json
import nxp

# ------------------------------------------------------------------------

class ScopeError(Exception): 
    def __init__(self,name,msg='Bad Scope'):
        self.message = '%s: "%s"' % (msg,name)

class TagError(Exception): 
    def __init__(self,tag,msg='Bad tag'):
        self.message = '%s: "%s"' % (msg,tag)

class LengthError(Exception):
    def __init__(self,obj,msg='Bad length'):
        self.message = '%s: %d' % (msg,len(obj))

# ------------------------------------------------------------------------

class Compiler:
    """
    Compiler object holds:
        commands to be interpreted
        variables to be substituted
        path used to find files
    """
    def __init__( self ):
        self._pre = dict()
        self._doc = dict()
        self._var = dict() 
        self._wrap = None
        self._path = [ getcwd() ]
        self._indoc = False
        self.load('melan.lang.default')

    def __str__(self):
        out = [ 'MeLan Compiler' ]
        out.append( '+ Path:\n\t' + ' ; '.join(self._path[1:]) )
        out.append( '+ Variables (%d):\n\t%s' % (len(self._var),self._var) )
        out.append( '+ Preamble (%d):\n\t%s' % (len(self._pre),', '.join(list(self._pre.keys()))) )
        out.append( '+ Document (%d):\n\t%s' % (len(self._doc),', '.join(list(self._doc.keys()))) )
        return '\n'.join(out)

    # ----------  =====  ----------
    # process

    def process(self,buffer,first=(0,0),last=None):
        return nxp.process( Parser, self._cb_elem, buffer, first, last )

    def procfile(self,infile,r2l=False):
        infile = self.pathFind(infile)
        return nxp.procfile( Parser, self._cb_elem, infile, r2l )

    def proctxt(self,text,r2l=False):
        return nxp.proctxt( Parser, self._cb_elem, text, r2l )

    # ----------  =====  ----------
    # path

    def _chkdir(self,p):
        assert op.isdir(p), FileNotFoundError('Not a folder: "%s"', p)

    def pathAppend(self,p):
        self._chkdir(p)
        self._path.append(p)
        return self
    def pathPrepend(self,p):
        self._chkdir(p)
        self._path.insert(0,p)
        return self
    def pathFind(self,f):
        for p in self._path:
            q = op.join(p,f)
            if op.exists(q):
                return q
        raise FileNotFoundError(f)

    def readfile(self,f):
        with open(self.pathFind(f)) as fh:
            return fh.read()

    # ----------  =====  ----------
    # variables

    def _mkvar(self,var):
        if isinstance(var,dict): # return as is
            return var 
        elif isinstance(var,str):
            assert op.isfile(var), FileNotFoundError(var)
            assert var.endswith('.json'), ValueError('Not a JSON file.')
            with open(var) as fh:
                return json.load(fh)
        else:
            raise TypeError('Unexpected var type: %s' % type(var))

    def varSet(self,var): 
        self._var = self._mkvar(var)
        return self
    def varAdd(self,var,prefix=''): 
        var = self._mkvar(var)
        for name,val in var.items():
            name = prefix+name
            if name in self._var:
                warn( 'Variable overwrite: "%s"' % name, RuntimeWarning )
            self._var[name] = val
        return self
    def varFilt(self,prefix):
        return { k.lstrip(prefix): v for k,v in self._var.items() if k.startswith(prefix) }

    def lst(self,key): return self._var.setdefault(key,[])
    def arg(self,key): return self._var.setdefault(key,{})
    def num(self,key): return self._var.setdefault(key,0)
    def get(self,key,default=None): return self._var.setdefault(key,default)

    def __getitem__(self,key): 
        return self._var[key]
    def __setitem__(self,key,val): 
        self._var[key] = val
    def __contains__(self,key):
        return key in self._var

    # ----------  =====  ----------
    # commands

    def _chkcmd(self,cmd):
        assert isinstance(cmd,dict), \
            TypeError('Expected dict, but got "%s" instead.' % type(cmd))
        assert all([ callable(f) for f in cmd.values() ]), \
            TypeError('Command values should be callable.')

    def docSet(self,cmd):
        self._chkcmd(cmd)
        self._doc = cmd
        return self
    def docAdd(self,cmd,prefix=''):
        self._chkcmd(cmd)
        for name,fun in cmd.items():
            name = prefix+name
            if name in self._doc:
                warn( 'Command override (doc): "%s"' % name, RuntimeWarning )
            self._doc[name] = fun
        return self

    def preSet(self,cmd):
        self._chkcmd(cmd)
        self._pre = cmd
        return self
    def preAdd(self,cmd,prefix=''):
        self._chkcmd(cmd)
        for name,fun in cmd.items():
            name = prefix+name
            if name in self._pre:
                warn( 'Command override (pre): "%s"' % name, RuntimeWarning )
            self._pre[name] = fun
        return self

    # ----------  =====  ----------
    # import from file

    def load(self,fpath,prefix='',package=None):

        # remove .py extension
        if fpath.endswith('.py') and op.isfile(fpath):
            fpath = fpath.rstrip('.py')

        # import module and look for "export"
        x = import_module(fpath,package)
        try:
            x = x.export 
        except:
            raise RuntimeError('Module should define variable "export".')

        # add commands and variables
        if 'pre' in x: self.preAdd(x['pre'],prefix)
        if 'doc' in x: self.docAdd(x['doc'],prefix)
        if 'var' in x: self.varAdd(x['var'])
        if 'wrap' in x: 
            if self._wrap is not None:
                 warn( 'Wrapper override', RuntimeWarning )
            self._wrap = x['wrap']

        return self

    def wrap(self,text):
        if self._wrap:
            return self._wrap(self,text)
        else:
            return text

    # ----------  =====  ----------
    # processing callback

    def _cb_elem(self,tsf,elm):
        if isinstance(elm,nxp.RMatch):
            beg,end = elm.beg, elm.end
            tag = elm.tag 

            if tag == 'rep':
                tsf.append( beg, end, ''.join(elm.text) )
            elif tag == 'var':
                tsf.append( beg, end, self[elm[0].data[1]] )
            else:
                raise TagError(tag,'Unknown tag')
        elif elm.name == 'command':
            self._cb_cmd(tsf,elm)
        elif elm.name == 'document':
            self._cb_doc(tsf,elm)
        else:
            raise ScopeError(elm.name,'Unexpected scope')

    def _cb_doc(self,tsf,elm):
        assert not self._indoc, RuntimeError('[bug] Nested document?')
        assert len(elm) >= 2, LengthError(elm)

        # bounds
        assert elm[0].tag=='doc' and elm[-1].tag=='/doc', ValueError('Bad first or last tag.')
        tsf.beg = elm[0].end
        tsf.end = elm[-1].beg
        
        # process
        self._indoc = True
        for sub in elm[1:-1]: self._cb_elem(tsf,sub)
        self._indoc = False
        
    def _cb_cmd(self,tsf,elm):
        assert len(elm) <= 3, LengthError(elm)

        # command name
        match = elm[0]
        assert match.tag == 'cmd', TagError(match.tag)

        name = match[0].data[1]
        beg,end = match.beg, match.end

        # body and options
        body = ''
        opt = dict()
        buf = tsf.buf

        for sub in elm[1:]:
            assert isinstance(sub,nxp.RElement), TypeError(sub)
            if sub.name == 'command.option':
                _,e,opt = self._cb_opt(buf,sub)
            else:
                _,e,body = self._cb_body(buf,sub)
            
            if e > end: end = e

        # call command
        if self._indoc:
            tsf.append( beg, end, self._doc[name](body,**opt) )
        else:
            self._pre[name](self,body,**opt)

    def _cb_opt(self,buf,elm):
        assert len(elm) >= 2, LengthError(elm,'Insufficient length')

        # bounds
        assert elm[0].tag=='arg' and elm[-1].tag=='/arg', ValueError('Bad first or last tag.')
        beg, end = elm[0].beg, elm[-1].end

        # options
        out = dict()
        for sub in elm[1:-1]:
            assert sub.name == 'command.option.name', ScopeError(sub.name)
            assert 1 <= len(sub) <= 2, LengthError(sub)
            assert sub[0].tag == 'opt', TagError(sub[0].tag)

            name = sub[0].text[0]
            if len(sub) > 1:
                out[name] = self._cb_value(buf,sub[1])
            else:
                out[name] = True 

        return beg,end,out

    def _cb_value(self,buf,elm):
        assert elm.name.startswith('command.option.'), ScopeError(elm.name)
        tag = elm[0].tag 
        if tag == 'num':
            return float(elm[0].text[0])
        elif tag == 'bool':
            return bool(elm[0].text[0])
        else:
            return self._cb_str(buf,elm)

    def _cb_str(self,buf,elm):
        assert len(elm) >= 2, LengthError(elm,'Insufficient length')
        tsf = nxp.Transform( buf, elm[0].end, elm[-1].beg )
        for sub in elm[1:-1]: self._cb_elem(tsf,sub)
        return str(tsf)

    def _cb_body(self,buf,elm):
        assert len(elm) >= 2, LengthError(elm,'Insufficient length')
        beg = elm[0].beg 
        end = elm[-1].end
        tsf = nxp.Transform( buf, elm[0].end, elm[-1].beg )
        if elm.name in {'command.body','command.pre'}:
            for sub in elm[1:-1]: self._cb_elem(tsf,sub)
        return beg,end,str(tsf)

# ------------------------------------------------------------------------

def compile( infile, r2l=False, output=None, show=False ):
    
    # compile document
    cpl = Compiler()
    out = cpl.procfile(infile,r2l)
    txt = cpl.wrap(str(out))

    # print to console
    if show: print(txt)

    # write to file
    if output:
        with open(output,'w') as fh:
            fh.write(txt)

    return cpl,out
    