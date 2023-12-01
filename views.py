from flask import render_template
from models import Personas
from run import app

@app.route('/')
def index():
    usuarios = Personas.query.all()
    return render_template('index.html', usuarios=usuarios)
