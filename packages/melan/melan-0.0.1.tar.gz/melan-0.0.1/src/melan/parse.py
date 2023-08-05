
from nxp import Num, Bool, FileBuffer, ListBuffer, make_parser

# ------------------------------------------------------------------------

# for body blocks
def _saveIndent(c,x,m):
    x.set('indent',c.line.indent)
def _checkIndent(c,x):
    return c.line.indent == x.get('indent',1)

# language definition using NXP
_variable = [ r'\$\{(\w[\w:\.]*)\}', ('tag','var') ]
_command = [ r'\\(\w[\w:]*)', ('open','command'), ('call',_saveIndent),('tag','cmd') ]
_comment = [ r'#.*$', ('rep','') ]
_bslash = [ r'\\\\', ('rep','\\') ]
_hash = [ r'\\#', ('rep','#') ]

Language = {
    'main': [
        _comment,
        _command,
        [ r'^\s*@begin\s*$', ('open','document'), ('tag','doc') ],
        [ r'@\{begin\}', ('open','document'), ('tag','doc') ]
    ],
    'document': [
        _hash,
        _comment,
        _variable,
        _bslash,
        _command,
        [ r'^\s*@end\s*$', ('tag','/doc'), 'close' ],
        [ r'@\{end\}', ('tag','/doc'), 'close' ]
    ],
    'command': {
        'main': [
            [ r'\[', ('open','command.option'), ('tag','arg') ],
            [ r'\{', ('open','command.body'), ('tag','body') ],
            [ r'\|', ('open','command.pre'), ('tag','pre') ],
            [ r'<\s*$', ('open','command.block'), ('tag','blk') ],
            [ None, 'close' ]
        ],
        'option': {
            'main': [
                [ r'\s+' ], # consume spaces
                [ r'\]', ('tag','/arg'), 'close' ],
                [ r'\w+', ('open','command.option.name'), ('tag','opt') ]
            ],
            'name': [
                [ r'\s+' ], # consume spaces
                [ r',', 'close' ], # equivalence: foo, <=> foo=True,
                [ r'=', ('open','command.option.value') ],
                [ r'\]', 'close', ('tag','/arg'), 'close' ]
            ],
            'value': [
                [ r'"', ('swap','command.option.dq_string'), ('tag','str') ],
                [ r"'", ('swap','command.option.sq_string'), ('tag','str') ],
                [ Num(), ('tag','num'), ('close',2) ],
                [ Bool(), ('tag','bool'), ('close',2) ]
            ],
            'dq_string': [
                [ r'$', ('err','No linebreaks allowed in strings.') ],
                _variable,
                [ r'\\"' ],
                [ r'"', ('tag','/str'), ('close',2) ]
            ],
            'sq_string': [
                [ r'$', ('err','No linebreaks allowed in strings.') ],
                [ r"\\'" ],
                [ r"'", ('tag','/str'), ('close',2) ]
            ]
        },
        'body': [
            _variable,
            [ r'\\\{', ('rep','{') ],
            [ r'\\\}', ('rep','}') ],
            _bslash,
            _hash,
            _comment,
            _command,
            [ r'\}', ('tag','/body'), ('close',2) ]
        ],
        'pre': [
            [ r'\\\|', ('rep','|') ],
            [ r'\|', ('tag','/pre'), ('close',2) ]
        ],
        'block': [
            [ r'^\s*/>', ('chk',_checkIndent), ('tag','/blk'), ('close',2) ]
        ]
    }
}

# ------------------------------------------------------------------------

Parser = make_parser({
    'lang': Language,
    'strict': [
        'main',
        'command.option.name',
        'command.option.value'
    ]
})

def parsefile( fpath, r2l=False ):
    return Parser.clone().parse( FileBuffer(fpath,r2l).cursor() )

def parselines( lines, r2l=False ):
    return Parser.clone().parse( ListBuffer(lines,r2l).cursor() )

def parsebuffer( buf ):
    return Parser.clone().parse( buf.cursor() )

def parse( text, r2l=False ):
    return parselines( text.splitlines(True), r2l )
