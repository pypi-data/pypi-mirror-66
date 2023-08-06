import re

from markdown.extensions import Extension
from markdown.postprocessors import Postprocessor


COMMENT_RE = r'''
(                                # Whole comment block
\((?P<comment>(                  # A comment containing
    (?<=\\)[()]                  #   Any escaped paren
    |                            #   or
    [^()]                        #   Any non-paren
)+                               #   one or more
)                                # End of comment
(\ \(                            # Whole attribution block
(?P<attribution>                 # An attribution of e.g: a name containing
    [^()]+?                      #   one or more non-parens non-greedy
)                                # End attribution name
(                                # Either
\ (?P<date>                      # A date containing
\d\d\d\d-\d\d-\d\d)              #   YYYY-MM-DD)
)?                               # End either
\))?                             # End of attribution (optional)
\))?                             # End of comment (optional)
'''

TYPE_MAP = {
    '+': 'addition',
    '-': 'deletion',
    '~': 'substitution',
    '?': 'selected',
    '!': 'comment',
    'c': 'comment',
    'a': 'attribution',
    'd': 'date',
}



class EditingExtension(Extension):

    def __init__(self, **kwargs):
        self.config = {
            'type_map': [
                TYPE_MAP,
                'dict mapping edit type to css class ("c", "a", and "d" entries'
                ' map to comment, attribution, and date segments)'],
        }
        super(EditingExtension, self).__init__(**kwargs)

    def extendMarkdown(self, md):
        type_map = self.getConfig('type_map')
        single_item_postprocessor = SingleItemPostprocessor(type_map, md)
        md.postprocessors.register(single_item_postprocessor, 'singleitemedit', 20)
        dual_item_postprocessor = DualItemPostprocessor(type_map, md)
        md.postprocessors.register(dual_item_postprocessor, 'dualitemedit', 20)


class SingleItemPostprocessor(Postprocessor):
    RE = re.compile(r'''
    (?P<type>[-+?!])\{  # An item
    (?P<contents> (     # containing
        (?<=\\)\}       #   Any escaped close brace
        |               #   or
        [^}]            #   Any non-brace
    )+)                 #   One or more
    \}?                  # End of item
    ''' + COMMENT_RE, re.MULTILINE | re.VERBOSE)
    
    def __init__(self, type_map, *args, **kwargs):
        self.type_map = type_map
        super(SingleItemPostprocessor, self).__init__(*args, **kwargs)

    def run(self, html):
        return re.sub(self.RE, self._convert_item, html)

    def _convert_item(self, match):
        tag = 'mark'
        if match.group('type') == '+':
            tag = 'ins'
        if match.group('type') == '-':
            tag = 'del'
        if match.group('type') == '!':
            tag = 'q'
        return '<{tag} class="{type}">{content}{comment}</{tag}>'.format(
            tag=tag,
            type=self.type_map[match.group('type')],
            content=match.group('contents'),
            comment=_build_comment(match, self.type_map))


class DualItemPostprocessor(Postprocessor):
    RE = re.compile(r'''
    (?P<type>~)\{              # A substitution (deletion first)
    (?P<deletion> (  # deletion containing
        (?<=\\)\}    #   Any escaped close brace
        |            #   or
        [^}]         #   Any non-brace
    )+)              #   One or more
    \}               # End of deletion
    \{               # (then substitution)
    (?P<addition> (  # addition containing
        (?<=\\)\}    #   Any escaped close brace
        |            #   or
        [^}]         #   Any non-brace
    )+)              #   One or more
    \}               # End of deletion
    ''' + COMMENT_RE, re.MULTILINE | re.VERBOSE)
    
    def __init__(self, type_map, *args, **kwargs):
        self.type_map = type_map
        super(DualItemPostprocessor, self).__init__(*args, **kwargs)

    def run(self, html):
        return re.sub(self.RE, self._convert_item, html)

    def _convert_item(self, match):
        return '<span class="{}">{}{}</span>'.format(
            self.type_map['~'],
            '<del>{}</del><ins>{}</ins>'.format(
                match.group('deletion'),
                match.group('addition')),
            _build_comment(match, self.type_map))


def makeExtension(**kwargs):
    return EditingExtension(**kwargs)


def _build_comment(match, type_map):
    if match.group('type') != '!' and match.group('comment') is not None:
        attribution = ''
        date = ''
        if match.group('attribution') is not None:
            attribution = '<span class="{}">{}</span>'.format(
                type_map['a'],
                match.group('attribution'))
        if match.group('date') is not None:
            date = '<span class="{}">{}</span>'.format(
                type_map['d'],
                match.group('date'))
        return '<q class="{}">{}{}{}</q>'.format(
            type_map['c'],
            match.group('comment').strip(),
            attribution.strip(),
            date.strip())
    else:
        return ''
