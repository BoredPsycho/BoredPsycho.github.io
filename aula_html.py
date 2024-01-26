#Flask -> framework pra desenvolver sites e APIs, ler a documentacao
from flask import Flask, render_template

app = Flask(__name__)

#criar a primeira pagina do site
#toda pagina tem um route e uma funcao
#route -> o caminho pra abrir dps do dominio do site(ex www.xxxx.com/(route))
#funcao -> o que voce quer exibir na pagina
#template -> template em html do site na pasta de mesmo nome
@app.route("/") #o @ e um decorator, que serve pra adicionar uma nova funcionalidade a uma funcao, no caso, poe o link da pagina a ser exibida
def homepage():
    return render_template("homepage.html")

@app.route("/contatos")
def contatos():
    return render_template("contatos.html")

@app.route("/usuarios/<nome_usuario>") #variavel entre <>
def usuarios(nome_usuario): #parametro na funcao
    return render_template("usuarios.html", nome_usuario=nome_usuario) #chama essa variavel

#colocar o site no ar
app.run(debug=True) #faz as edicoes do codigo serem adicionadas automaticamente no site