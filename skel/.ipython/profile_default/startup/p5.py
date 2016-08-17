# This code can be put in any Python module, it does not require IPython
# itself to be running already.  It only creates the magics subclass but
# doesn't instantiate it yet.
import IPython
from IPython.core.magic import (Magics, magics_class, line_magic,
                                cell_magic, line_cell_magic)
from IPython.display import HTML


# The class MUST call this class decorator at creation time
@magics_class
class P5Magics(Magics):

    @cell_magic
    def p5(self, line, cell):
        if line.strip() == '':
          width, height = 720, 480
        else:
          width, height = (int(x) for x in line.split())
        prog = cell.strip().replace("'", "&quot;")
        html = """
<iframe sandbox='allow-same-origin allow-scripts allow-modals'
width='%d' height='%d'
style='border:none'
srcdoc='
    <head>
      <script language="javascript" src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/0.5.2/p5.min.js"></script>
      <script language="javascript" src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/0.5.2/addons/p5.dom.min.js"></script>
      <script language="javascript" src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/0.5.2/addons/p5.sound.min.js"></script>
        <style type="text/css" media="screen">
            body, #defaultCanvas0 {
                margin: 0px;
                padding: 0px;
            }
        </style>
    </head>
    <body>
    <script>
    WIDTH = %d;
    HEIGHT = %d;
    %s
    </script>
    </body>
' ></iframe>
"""
        return HTML(html % (width + 16, height + 16, width, height, prog))


# Coloration Javascript
js = "IPython.CodeCell.config_defaults.highlight_modes['magic_javascript'] = {'reg':[/^%%p5/]};"
IPython.core.display.display_javascript(js, raw=True)

# In order to actually use these magics, you must register them with a
# running IPython.  This code must be placed in a file that is loaded once
# IPython is up and running:
ip = get_ipython()
# You can register the class itself without instantiating it.  IPython will
# call the default constructor on it.
ip.register_magics(P5Magics)
