import ast
from flask import Flask, render_template, Response, request
from slugify import slugify

from pyp5js import commands
from pyp5js.config import SKETCHBOOK_DIR
from pyp5js.exceptions import PythonSketchDoesNotExist, SketchDirAlreadyExistException
from pyp5js.fs import SketchFiles


app = Flask(__name__)
SUPPORTED_IMAGE_FILE_SUFFIXES = (".gif", ".jpg", ".png")


@app.route("/")
def sketches_list_view():
    sketches = []
    for sketch_dir in (p for p in SKETCHBOOK_DIR.iterdir() if p.is_dir()):
        name = sketch_dir.name
        sketch_files = SketchFiles(name)
        if sketch_files.has_all_files:
            sketches.append({
                'name': name,
                'url': f'/sketch/{name}'
            })

    sketches = sorted(sketches, key=lambda s: s['name'])
    return render_template('index.html', sketches=sketches, sketches_dir=SKETCHBOOK_DIR.resolve())


@app.route("/new-sketch/", methods=['GET', 'POST'])
def add_new_sketch_view():
    template = 'new_sketch_form.html'
    context = {'sketches_dir': SKETCHBOOK_DIR.resolve()}

    if request.method == 'POST':
        sketch_name = slugify(request.form.get(
            'sketch_name', '').strip(), separator='_')
        if not sketch_name:
            context['error'] = "You have to input a sketch name to proceed."
        else:
            try:
                files = commands.new_sketch(sketch_name)
                template = 'new_sketch_success.html'
                context.update({
                    'files': files,
                    'sketch_url': f'/sketch/{sketch_name}/',
                })
            except SketchDirAlreadyExistException:
                path = SKETCHBOOK_DIR.joinpath(sketch_name)
                context['error'] = f"The sketch {path} already exists."

    return render_template(template, **context)


@app.route('/sketch/<string:sketch_name>/', defaults={'static_path': ''}, methods=['GET', 'POST'])
@app.route('/sketch/<string:sketch_name>/<path:static_path>')
def render_sketch_view(sketch_name, static_path):
    sketch_files = SketchFiles(sketch_name)

    error = ''
    if static_path:
        return _serve_static(sketch_files, static_path)

    elif request.method == 'POST':
        py_code = request.form.get('py_code', '')
        if not py_code.strip():
            error = 'You have to input the Python code.'
        elif 'def setup():' not in py_code:
            error = 'You have to define a setup function.'
        elif 'def draw():' not in py_code:
            error = 'You have to define a draw function.'
        else:
            try:
                ast.parse(py_code, sketch_files.sketch_py.name)
                sketch_files.sketch_py.write_text(py_code)
            except SyntaxError as exc:
                error = f'SyntaxError: {exc}'

    if not error:
        try:
            commands.transcrypt_sketch(sketch_name)
        except PythonSketchDoesNotExist:
            return f"There's no sketch in {sketch_files.sketch_dir.resolve()}", 404

    context = {
        'p5_js_url': sketch_files.urls.p5_js_url,
        'sketch_js_url': sketch_files.urls.sketch_js_url,
        'sketch_name': sketch_files.sketch_name,
        'py_code': sketch_files.sketch_py.read_text(),
        'error': error,
    }
    return render_template('view_sketch.html', **context)


def _serve_static(sketch_files, static_path):
    content_file = sketch_files.sketch_dir.joinpath(static_path).resolve()
    if not str(content_file).startswith(str(sketch_files.sketch_dir.resolve())):
        # User tried something not allowed (as "/root/something" or "../xxx")
        return '', 403
    elif not content_file.exists():
        return '', 404

    mode = 'r'
    encoding = 'utf-8'
    file_suffix = content_file.suffix.lower()
    if file_suffix in SUPPORTED_IMAGE_FILE_SUFFIXES:
        encoding = None
        mode = 'rb'

    with content_file.open(encoding=encoding, mode=mode) as fd:
        response = Response(fd.read())

    if file_suffix == '.js':
        # To avoid MIME type errors
        # More can be found here: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options  # noqa
        response.headers['Content-Type'] = 'application/javascript'
    elif file_suffix in SUPPORTED_IMAGE_FILE_SUFFIXES:
        response.headers['Content-Type'] = 'image/' + file_suffix[1:]
        response.headers['Content-Disposition'] = f'attachment; filename={content_file.name.lower()}'

    return response
