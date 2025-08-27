from flask import Flask, render_template, request, flash, redirect, url_for
from js_flask import javascript
from python_flask import python
from ts_flask import typescript
import secrets
import os

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            return redirect(url_for('index'))
        code = file.read().decode('utf-8')

        filename = file.filename
        extension = filename.split('.')[-1].lower()

        if extension == "js":
            result = javascript(code)
        elif extension == 'py':
            result = python(code)
        elif extension == 'ts':
            result = typescript(code)
        else:
            flash("unsupported file! currently only .js, .ts and .py files are supported")
            return redirect(url_for('index'))

    return render_template('index.html', result=result)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
