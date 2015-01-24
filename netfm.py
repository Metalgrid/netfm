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


@app.route("/__netfm_api/folder/", methods=['GET', 'POST'])
def folder_api():
    action = request.form.get('action', None)
    target = request.form.get('target', None)
    if not action or not target:
        return jsonify({'message': "Invalid action or target!"}), 500
    if action == 'new':
        try:
            os.mkdir(target)
            return jsonify({'message': "Directory %s created" % target})
        except OSError as e:
            return jsonify({'message': str(e)}), 500


def run():
    app.run(host="0.0.0.0", port=8080, debug=True)

if __name__ == "__main__":
    run()
