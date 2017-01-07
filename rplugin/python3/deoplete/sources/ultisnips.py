import re
from .base import Base

class Source(Base):
    def __init__(self, vim):
        Base.__init__(self, vim)

        self.name = 'ultisnips'
        self.mark = '[U]'
        self.rank = 8

    def gather_candidates(self, context):
        suggestions = []
        prog = re.compile(r'(\w+)\.snippets:')
        snippets = self.vim.eval(
            'UltiSnips#SnippetsInCurrentScope()')
        name = ''
        for snip in snippets:
            match = prog.search(snip.get('location'))
            if match is not None:
                name = match.group(1)
            suggestions.append({
                'word': snip['key'],
                'menu': '['+ name + ']',
                'dup': 1
            })
        return suggestions
