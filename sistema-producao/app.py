from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "troque-essa-chave-por-outra"

def get_db():
    return sqlite3.connect("banco.db")

@app.route("/")
def home():
    return redirect(url_for("login_page"))

@app.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    try:
        dados = request.get_json(silent=True) or {}
        username = str(dados.get("username", "")).strip()
        senha = str(dados.get("senha", "")).strip()

        if not username or not senha:
            return jsonify({"status": "erro", "mensagem": "Preencha usuário e senha"}), 400

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM usuarios WHERE username = ? AND senha = ?",
            (username, senha)
        )
        user = cursor.fetchone()
        conn.close()

        if user:
            session["user_id"] = user[0]
            session["username"] = username
            return jsonify({"status": "ok"})

        return jsonify({"status": "erro", "mensagem": "Usuário ou senha inválidos"}), 401
    except Exception as e:
        print("ERRO LOGIN:", e)
        return jsonify({"status": "erro", "mensagem": "Erro interno no login"}), 500

@app.route("/dashboard")
def dashboard():
    if not session.get("user_id"):
        return redirect(url_for("login_page"))
    return render_template("index.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))

@app.route("/api/producao", methods=["GET"])
def listar_producao():
    if not session.get("user_id"):
        return jsonify({"status": "erro", "mensagem": "Não autorizado"}), 401

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, maquina, quantidade, data FROM producao ORDER BY id DESC")
    dados = cursor.fetchall()
    conn.close()

    return jsonify(dados)

@app.route("/api/producao", methods=["POST"])
def adicionar_producao():
    if not session.get("user_id"):
        return jsonify({"status": "erro", "mensagem": "Não autorizado"}), 401

    try:
        dados = request.get_json(silent=True) or {}
        maquina = str(dados.get("maquina", "")).strip()
        quantidade = int(dados.get("quantidade", 0))
        data = str(dados.get("data", "")).strip()

        if not maquina or not data:
            return jsonify({"status": "erro", "mensagem": "Dados incompletos"}), 400

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO producao (maquina, quantidade, data) VALUES (?, ?, ?)",
            (maquina, quantidade, data)
        )
        conn.commit()
        conn.close()

        return jsonify({"status": "ok"})
    except ValueError:
        return jsonify({"status": "erro", "mensagem": "Quantidade inválida"}), 400
    except Exception as e:
        print("ERRO POST PRODUCAO:", e)
        return jsonify({"status": "erro", "mensagem": "Erro interno"}), 500

@app.route("/api/producao/<int:registro_id>", methods=["DELETE"])
def deletar_producao(registro_id):
    if not session.get("user_id"):
        return jsonify({"status": "erro", "mensagem": "Não autorizado"}), 401

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM producao WHERE id = ?", (registro_id,))
        conn.commit()
        conn.close()

        return jsonify({"status": "ok"})
    except Exception as e:
        print("ERRO DELETE PRODUCAO:", e)
        return jsonify({"status": "erro", "mensagem": "Erro interno"}), 500

if __name__ == "__main__":
    app.run(debug=True)


































    