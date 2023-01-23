from flask import Flask
from flask import Flask, render_template, redirect, request, session, jsonify, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://master:ekka@localhost:5432/ekkadb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'thisismykey'
db = SQLAlchemy(app)


@app.route("/form")
def form():
    if request.method == 'POST':
        firstname = request.form.get('firstanme')
        email = request.form.get('email')
        return redirect(url_for('details'))
    return render_template('form.html')


@app.route("/details")
def details():
    return render_template('details.html')


if __name__ == '__main__':
    app.run(port=7000, debug=True)