import sys
import re
from IPython.core.magic import register_cell_magic
from IPython.display import HTML, display

def load_ipython_extension(ipython):
    pass

def unload_ipython_extension(ipython):
    pass

# Highlight colors alternate globally.
this, next = None, None

@register_cell_magic
def regex(pattern, cell):
    '''Match the pattern against every line in the cell and format results.'''
    global this, next
    this, next = "red", "blue"
    result = '<font color="green"><strong>%s</strong></font>\n' % pattern + \
             '\n'.join([handle(pattern, x) for x in cell.split('\n')])
    return HTML(result)

def handle(pattern, line):
    '''Find successive matches, marking the text of each in color.'''
    global this, next
    result = []
    m = re.search(pattern, line)
    while m:
        result.append(line[:m.start()])
        result.append('<font color="%s"><u>' % this)
        result.append(line[m.start():m.end()])
        result.append('</u></font>')
        this, next = next, this
        line = line[m.end():]
        m = re.search(pattern, line)
    result.append(line)
    return '<br/>%s' % ''.join(result)
