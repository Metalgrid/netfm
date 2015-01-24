import os
import sys
import magic
from pygments import highlight
from pygments import lexers
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound
from flask import Flask, session, render_template, request, Response, jsonify

app = Flask("netfm")
app.secret_key = "ONH&YFF^WRV"


@app.route('/', defaults={'pathstr': '.'})
@app.route('/<path:pathstr>/', methods=['GET', 'POST'])
def path(pathstr):
    if 'topdir' not in session:
        session['topdir'] = os.path.realpath(os.curdir)
    os.chdir(session.get('topdir'))
    app.logger.debug(session)
    path = pathstr.split('/')
    if '' in path:
        path.remove('')
    if not os.path.exists(pathstr):
        return "No such file or directory!", 404
    for entry in path:
        if entry == ".":
            path.remove(".")
            continue
        if os.path.isdir(entry):
            os.chdir(entry)
            session['cwd'] = entry
        else:
            size = os.stat(entry).st_size
            if size > 5*1024*1024:
                return "Error: File too large for preview"
            with open(entry, 'r') as f:
                content = f.read()
                try:
                    doc = highlight(
                        content,
                        lexers.get_lexer_for_filename(entry, stripall=True),
                        HtmlFormatter(linenos=True)
                        )
                except ClassNotFound:
                    return Response(
                        content,
                        mimetype=magic.from_file(entry, mime=True)
                        )
                return render_template(
                    'edit.html',
                    doc=doc,
                    style=HtmlFormatter().get_style_defs('.highlight')
                    )
    return render_template(
        "index.html",
        breadcrumbs=path,
        dirlist=os.listdir("."),
        isdir=lambda e: os.path.isdir(e)
        )


def server():
    app.run(host="0.0.0.0", port=8080, debug=True)

if __name__ == "__main__":
    server()
