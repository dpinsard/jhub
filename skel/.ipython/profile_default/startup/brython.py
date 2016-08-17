# This code can be put in any Python module, it does not require IPython
# itself to be running already.  It only creates the magics subclass but
# doesn't instantiate it yet.
import IPython
from IPython.core.magic import (Magics, magics_class, line_magic,
                                cell_magic, line_cell_magic)
from IPython.display import HTML


# The class MUST call this class decorator at creation time
@magics_class
class BrythonMagics(Magics):

    @cell_magic
    def brython(self, line, cell):
        if line.strip() == '':
          width, height = 720, 480
        else:
          width, height = (int(x) for x in line.split())
        code = cell.strip().replace('\n', '\n    ')
        html = """
<iframe sandbox='allow-scripts' width='%d' height='%d'
srcdoc='
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<script src="//cdnjs.cloudflare.com/ajax/libs/p5.js/0.5.2/p5.js"></script>
<script type="text/javascript" src="//cdn.rawgit.com/brython-dev/brython/3.2.2/www/src/brython.js"></script>
<style type="text/css" media="screen">
  body {
    font: 12px/15px Calibri, Verdana;
    margin: 0px;
    background:#ddd;
    padding: 0px;
  }
#defaultCanvas0{
    position: absolute;
    margin: 0px;
    padding: 0px;
}
</style>
</head>
<body onload="brython()">
<script type="text/python">
from browser import document, window, alert
from javascript import JSConstructor

def sketch(p):
    width = %d
    height = %d
    preload = lambda : None
    setup = lambda : None
    draw = lambda : None
    mousePressed = lambda : None
    %s
    p.preload = preload
    p.setup = setup
    p.draw = draw
    p.mousePressed = mousePressed

myp5 = JSConstructor(window.p5)(sketch)
</script>
</body>
' />"""
        return HTML(html % (width + 2, height + 2, width, height, code))


# In order to actually use these magics, you must register them with a
# running IPython.  This code must be placed in a file that is loaded once
# IPython is up and running:
ip = get_ipython()
# You can register the class itself without instantiating it.  IPython will
# call the default constructor on it.
ip.register_magics(BrythonMagics)
