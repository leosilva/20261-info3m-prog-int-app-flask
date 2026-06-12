from app import app


@app.route('/')
def hello():
    return "Página inicial"


@app.route('/sobre')
def sobre():
    return "Página sobre"

@app.route('/endereco')
def endereco():
    return "<h1>Meu endereço</h1>"