# ============================================================================
# FILE: ultisnips.py
# AUTHOR: Qiming Zhao <chemzqm@gmail.com>
# License: MIT license
# ============================================================================
# pylint: disable=E0401,C0411
import os
from ..kind.file import Kind as File
from .base import Base
from operator import itemgetter

class Source(Base):

    def __init__(self, vim):
        super().__init__(vim)
        self.name = 'ultisnips'
        self.matchers = ['matcher_regexp']
        self.kind = Kind(vim)

    def on_init(self, context):
        pos = self.vim.call('getpos', '.')
        col = pos[2] - 1 if pos[2] > 1 else 0
        line = self.vim.current.buffer[pos[1] - 1]
        ch = line[col] if len(line) else ''
        if len(ch) == 0 or ch == ' ':
            context['__command'] = ''
        else:
            context['__command'] = 'diw'

    def highlight(self):
        self.vim.command(r'highlight default link deniteSource__UltisnipsPath Comment')
        self.vim.command(r'highlight default link deniteSource__UltisnipsTrigger Identifier')
        self.vim.command(r'highlight default link deniteSource__UltisnipsDescription Statement')

    def define_syntax(self):
        self.vim.command('syntax case ignore')
        self.vim.command(r'syntax match deniteSource__UltisnipsHeader /^.*$/ '
                         r'containedin=' + self.syntax_name)
        self.vim.command(r'syntax match deniteSource__UltisnipsPath /\v^\s.{-}\ze\s/ contained '
                         r'containedin=deniteSource__UltisnipsHeader')
        self.vim.command(r'syntax match deniteSource__UltisnipsTrigger /\%14c.*\%38c/ contained '
                         r'containedin=deniteSource__UltisnipsHeader')
        self.vim.command(r'syntax match deniteSource__UltisnipsDescription /\%39c.*$/ contained '
                         r'containedin=deniteSource__UltisnipsHeader')

    def gather_candidates(self, context):
        args = dict(enumerate(context['args']))
        is_all = str(args.get(0, '')) == 'all'
        if is_all:
            items = self.vim.call('UltiSnips#SnippetsInCurrentScope', 1)
        else:
            items = self.vim.call('UltiSnips#SnippetsInCurrentScope', 0)

        items = sorted(items, key=itemgetter('priority', 'filepath'), reverse=True)
        candidates = []
        for item in items:
            locs = item['location'].split(':')
            base = os.path.basename(locs[0])
            fname = os.path.splitext(base)[0]
            candidates.append({
                'word': '%s %s' % (item['key'], item['description']),
                'abbr': '%-12s%-20s     %s' % (fname, item['key'], item['description']),
                'action__path': locs[0],
                'action__line': locs[1],
                'action__col': 0,
                'source__command': context['__command'],
                'source__trigger': item['key'],
                })
        return candidates

class Kind(File):
    """
    Kind of ultisnips source
    """
    def __init__(self, vim):
        super().__init__(vim)

        self.default_action = 'expand'
        self.name = 'ultisnips'
        self.sorters = []

    def action_expand(self, context):
        """
        expand snippet
        """
        target = context['targets'][0]
        command = target['source__command']
        trigger = target['source__trigger']
        self.vim.command('normal %sa%s ' % (command, trigger))
        self.vim.call('UltiSnips#ExpandSnippet')

    def action_edit(self, context):
        """
        edit snippet
        """
        return self.action_open(context)
