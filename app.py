from flask import Flask


app = Flask(__name__)


@app.route("/")
def questao1():
    return render_template("questao1.html", name = "Clara")

@app.route("/questao2")
def questao2():
    dados = [{"nome": "Clara", "idade": 18}]
    return render_template("questao2.html", alunos = dados)



if __name__ == "__main__":
    app.run(debug=True)