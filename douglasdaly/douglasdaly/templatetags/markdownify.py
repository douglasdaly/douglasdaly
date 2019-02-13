# -*- coding: utf-8 -*-
"""
markdownify.py

    Code for markdown/pygments - based on code from www.IgnoredByDinosaurs.com

"""
#
#   Imports
#
import re
from django import template

import mistune
from mistune_contrib import math
from pygments import highlight
from pygments.util import ClassNotFound
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter

from assets.utils import AssetRenderer


#
#   Classes
#

class CustomRenderer(math.MathRendererMixin, AssetRenderer):
    """
    Custom Renderer class for Markdown content
    """

    def math(self, text):
        """Render math for MathJax"""
        return '\\(%s\\)' % text

    def block_code(self, code, lang=None):
        """Render code blocks using pygments"""
        if not lang:
            return '\n<div class="highlight"><pre><code>' + \
                   '%s</code></pre></div>\n' % mistune.escape(code)

        try:
            lexer = get_lexer_by_name(lang, stripall=True)
            formatter = HtmlFormatter(linenos="inline")
            return highlight(code, lexer, formatter)
        except ClassNotFound:
            return self.block_code(code)

    def table(self, header, body):
        """Render table utilizing bootstrap tables"""
        ret = (
            '<table class="table table-sm table-hover table-bordered '
            'table-striped">\n'
            '<thead class="thead-dark bg-primary">%s</thead>\n'
            '<tbody>\n%s</tbody>\n</table>\n'
        ) % (header, body)
        return '<div class="table-responsive">%s</div>' % ret

    def table_row(self, content, **flags):
        """Render table rows with some customization"""
        ret = '<tr'

        klass = flags.get('class', None)

        if klass:
            ret += ' class="%s"' % klass

        ret += '>%s</tr>\n' % content

        return ret

    def table_cell(self, content, **flags):
        """Render table cells with some customization"""
        if flags['header'] or flags.get('row_header', False):
            tag = 'th'
            scope = 'col'
        else:
            tag = 'td'
            scope = None

        if flags.get('row_header', False):
            scope = 'row'
            klass = None
        else:
            klass = flags.get('class', None)

        align = flags['align']

        ret = '<%s' % tag
        if klass:
            ret += ' class="%s"' % klass
        if scope:
            ret += ' scope="%s"' % scope
        if align:
            ret += ' style="text-align:%s"' % align
        ret += '>%s</%s>' % (content, tag)

        return ret


class CustomBlockGrammar(mistune.BlockGrammar):
    """
    Block grammar for customized tables
    """
    table = re.compile(
        r'^ *\|(.+)\n *\|( *[#-:]+[-| :]*)\n((?: *\|.*(?:\n|$))*)\n*'
    )


class CustomBlockLexer(math.MathBlockMixin, mistune.BlockLexer):
    """
    Block Lexer for MathJax support
    """
    grammar_class = CustomBlockGrammar

    def __init__(self, *args, **kwargs):
        super(CustomBlockLexer, self).__init__(*args, **kwargs)
        self.enable_math()

    def parse_table(self, m):
        """Override parse table function for added functionality"""
        item = self._process_table(m)

        cells = re.sub(r'(?: *\| *)?\n$', '', m.group(3))
        cells = cells.split('\n')
        for i, v in enumerate(cells):
            v = re.sub(r'^ *\| *| *\| *$', '', v)
            cells[i] = re.split(r' *(?<!\\)\| *', v)

        item['cells'], item['cell_properties'] = self._process_cells(cells)
        self.tokens.append(item)

    def parse_nptable(self, m):
        """Override parse table function for added functionality"""
        item = self._process_table(m)

        cells = re.sub(r'\n$', '', m.group(3))
        cells = cells.split('\n')
        for i, v in enumerate(cells):
            cells[i] = re.split(r' *(?<!\\)\| *', v)

        item['cells'], item['cell_properties'] = self._process_cells(cells)
        self.tokens.append(item)

    def _process_table(self, m):
        """Override process table to collect additional information"""
        header = re.sub(r'^ *| *\| *$', '', m.group(1))
        header = re.split(r' *\| *', header)
        align = re.sub(r' *|\| *$', '', m.group(2))
        align = re.split(r' *\| *', align)
        row_headers = list()

        for i, v in enumerate(align):
            (v, cnt) = re.subn(r'#', '', v)
            row_headers.append(True if cnt > 0 else False)

            if re.search(r'^ *-+: *$', v):
                align[i] = 'right'
            elif re.search(r'^ *:-+: *$', v):
                align[i] = 'center'
            elif re.search(r'^ *:-+ *$', v):
                align[i] = 'left'
            else:
                align[i] = None

        item = {
            'type': 'table',
            'header': header,
            'align': align,
            'row_headers': row_headers,
        }
        return item

    def _process_cells(self, cells):
        """Override process cells to collect additional information"""
        cell_flags = list()
        for i, line in enumerate(cells):
            cell_flags.append(list())
            for c, cell in enumerate(line):
                # Get any cell properties
                cell, t_cflags = self.__preprocess_cell_props(cell)
                cell_flags[i].append(t_cflags)

                # de-escape any pipe inside the cell here
                cells[i][c] = re.sub('\\\\\|', '|', cell)

        return cells, cell_flags

    @staticmethod
    def __preprocess_cell_props(cell):
        """Helper function to pre-process cell information for properties"""
        prop_res = [
            ('class', (re.compile(r'^ *@class="(.+)" *'), [1], ' ')),
        ]

        ret = cell
        ret_props = None
        for (k, (p, grps, repl)) in prop_res:
            t_match = p.match(cell)
            if t_match:
                if ret_props is None:
                    ret_props = dict()
                ret_props[k] = t_match.group(*grps)
                ret = re.sub(p, repl, ret)

        return ret, ret_props


class CustomInlineGrammar(mistune.InlineGrammar):
    """
    Inline grammar
    """
    emphasis = re.compile(
        r'^\*((?:\*\*|[^\*])+?)\*(?!\*)'  # *word*
    )

    double_emphasis = re.compile(
        r'^\*{2}([\s\S]+?)\*{2}(?!\*)'  # **word**
    )

    link = re.compile(
        r'^!?\[('
        r'(?:\[[^^\]]*\]|[^\[\]]|\](?=[^\[]*\]))*'
        r')\]\('
        r'''\s*(<)?([\s\S]*?)(?(2)>)(?:\s+['"]([\s\S]*?)['"])?\s*'''
        r'\)'
        r'(?:\s*(?:\{:\s*)(.*)(?:\s*\}))?'
    )


class CustomInlineLexer(math.MathInlineMixin, mistune.InlineLexer):
    """
    Inline Lexer for MathJax support and disabled underscores
    """
    grammar_class = CustomInlineGrammar

    def __init__(self, *args, **kwargs):
        super(CustomInlineLexer, self).__init__(*args, **kwargs)

        self.enable_math()
        self.rules.math = re.compile(r'^\\\((.+?)\\\)')

    def output_emphasis(self, m):
        """Override emphasis rules for MathJax integration"""
        text = m.group(1)
        text = self.output(text)
        return self.renderer.emphasis(text)

    def output_double_emphasis(self, m):
        """Override double-emphasis rules for MathJax integration"""
        text = m.group(1)
        text = self.output(text)
        return self.renderer.double_emphasis(text)

    def _process_link(self, m, link, title=None):
        """Override for attributes"""
        line = m.group(0)
        text = m.group(1)
        attrib = m.group(5) or None

        if line[0] == '!':
            return self.renderer.image(link, title, text, attribute=attrib)

        self._in_link = True
        text = self.output(text)
        self._in_link = False
        return self.renderer.link(link, title, text)


class CustomMarkdown(mistune.Markdown):
    """
    Custom Markdown class
    """

    def output_table(self):
        """Override output table for added functionality"""
        aligns = self.token['align']
        aligns_length = len(aligns)
        row_headers = self.token['row_headers']
        cell_properties = self.token['cell_properties']
        cell = self.renderer.placeholder()

        # header part
        header = self.renderer.placeholder()
        for i, value in enumerate(self.token['header']):
            align = aligns[i] if i < aligns_length else None
            flags = {'header': True, 'align': align}
            cell += self.renderer.table_cell(self.inline(value), **flags)

        header += self.renderer.table_row(cell)

        # body part
        body = self.renderer.placeholder()
        for i, row in enumerate(self.token['cells']):
            cell = self.renderer.placeholder()
            row_props = None
            for j, value in enumerate(row):
                align = aligns[j] if j < aligns_length else None
                row_header = row_headers[j] if j < aligns_length else None
                flags = {
                    'header': False, 'align': align, 'row_header': row_header
                }
                t_cprops = cell_properties[i][j]
                if t_cprops:
                    if not row_header:
                        flags = {**flags, **t_cprops}
                    else:
                        row_props = t_cprops

                cell += self.renderer.table_cell(self.inline(value), **flags)

            body += self.renderer.table_row(cell,
                                            **(row_props if row_props else {}))

        return self.renderer.table(header, body)


#
#   Filter Setup
#

register = template.Library()

md = CustomMarkdown(renderer=CustomRenderer(), inline=CustomInlineLexer,
                    block=CustomBlockLexer)


@register.filter
def markdown(value):
    return md(value)
