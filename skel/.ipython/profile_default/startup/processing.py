# This code can be put in any Python module, it does not require IPython
# itself to be running already.  It only creates the magics subclass but
# doesn't instantiate it yet.
import IPython
from IPython.core.magic import (Magics, magics_class, line_magic,
                                cell_magic, line_cell_magic)
from IPython.display import HTML


# The class MUST call this class decorator at creation time
@magics_class
class ProcessingMagics(Magics):

    @cell_magic
    def processing(self, line, cell):
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
        <script type="text/javascript" src="/lib/js/jquery.min.js"></script>
        <script type="text/javascript" src="/lib/js/skulpt.min.js"></script>
        <script type="text/javascript" src="/lib/js/skulpt-stdlib.js"></script>
        <script type="text/javascript" src="/lib/js/processing.min.js"></script>
        <style type="text/css" media="screen">
            body, #skulpt_canvas {
                margin: 0px;
                padding: 0px;
            }
        </style>
    </head>
    <body onload="skulpt()">
        <script type="text/javascript">
            function outf(text) {
               var mypre = document.getElementById(Sk.pre);
               mypre.innerHTML = mypre.innerHTML + text;
            }

            function builtinRead(x)
            {
                if (Sk.builtinFiles === undefined || Sk.builtinFiles["files"][x] === undefined)
                    throw "File not found: " + x;
                return Sk.builtinFiles["files"][x];
            }

            function skulpt() {
               var prog = document.getElementById("skulpt_prog").innerText;
               Sk.canvas = "skulpt_canvas";
               var can = document.getElementById(Sk.canvas);
               can.style.display = "block";
               Sk.pre = "skulpt_output";
               Sk.configure({output:outf,
                        read: builtinRead
                          });
               var myPromise = Sk.misceval.asyncToPromise(function() {
                  return Sk.importMainWithBody("<stdin>",false,prog,true);
               });
               myPromise.then(function() {}, function(err) {alert(err.toString())});
            }
        </script>
        <pre id="skulpt_prog" hidden>
from processing import *
width, height = %d, %d
%s
run()
        </pre>
        <canvas id="skulpt_canvas"></canvas>
        <pre id="skulpt_output"></pre>
    </body>
'></iframe>"""
        return HTML(html % (width + 16, height + 16, width, height, prog))


# In order to actually use these magics, you must register them with a
# running IPython.  This code must be placed in a file that is loaded once
# IPython is up and running:
ip = get_ipython()
# You can register the class itself without instantiating it.  IPython will
# call the default constructor on it.
ip.register_magics(ProcessingMagics)
