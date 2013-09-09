"""regexmagic provides a cell magic for the IPython Notebook called
%%regex that runs regular expressions against lines of text without
the clutter of re.search(...) calls.  The output is colorized to show
the span of each match.

Usage:

%%regex a+b
this text has no matches
this line has one match: aaab
about to match some more: aab

Note: IPython presently interprets {x} to mean 'expand variable x', so
      regular expressions like '\d{4}' must be written as '\d{{4}}'.
      We're working on it..."""

# This file is copyright 2013 by Matt Davis and Greg Wilson and
# covered by the license at
# https://github.com/gvwilson/regexmagic/blob/master/LICENSE

import re
from IPython.core.magic import Magics, magics_class, cell_magic
from IPython.display import display, HTML

MATCH_TEMPL = '<font color="{0}"><u>{1}</u></font>'
PATTERN_TEMPL = '<font color="green"><strong>{0}</strong></font>\n'


@magics_class
class RegexMagic(Magics):
    '''Provide the 'regex' calling point for the magic, and keep track of
    alternating colors while matching.'''

    this_color, next_color = 'red', 'blue'

    @cell_magic
    def regex(self, pattern, text):
        pattern_str = PATTERN_TEMPL.format(pattern)
        result_str = [self.handle_line(pattern, line) for line in text.split('\n')]
        display(HTML(pattern_str + '\n'.join(result_str)))

    def handle_line(self, pattern, line):
        result = []
        m = re.search(pattern, line)
        while m:
            result.append(line[:m.start()])
            result.append(MATCH_TEMPL.format(self.this_color, line[m.start():m.end()]))
            self.this_color, self.next_color = self.next_color, self.this_color
            line = line[m.end():]
            m = re.search(pattern, line)
        result.append(line)
        return '<br/>{0}'.format(''.join(result))


def load_ipython_extension(ipython):
    ipython.register_magics(RegexMagic)
