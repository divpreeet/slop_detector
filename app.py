from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def main(name="divpreet"):
    return render_template('index.html', person=name)


@app.route('/js')
def js():
    return "<p>js</p>"