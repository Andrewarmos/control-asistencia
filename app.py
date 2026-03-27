from flask import Flask, request, jsonify, send_file
from datetime import datetime
import pandas as pd

app = Flask(__name__)

# Base de datos temporal (en memoria)
registros = []

# Página principal
@app.route("/")
def inicio():
    return """
    <h2>Control de Asistencia</h2>

    <form action="/registro" method="post">
        Código: <input type="text" name="codigo"><br><br>

        Ubicación:
        <select name="ubicacion">
            <option value="Redfern">Edificio Redfern</option>
            <option value="Mascot">Edificio Mascot</option>
            <option value="Otro">Otro</option>
        </select><br><br>

        Tipo:
        <select name="tipo">
            <option value="entrada">Entrada</option>
            <option value="salida">Salida</option>
        </select><br><br>

        <button type="submit">Registrar</button>
    </form>

    <br>
    <a href="/registros">Ver registros</a><br>
    <a href="/exportar">Descargar Excel</a>
    """

# Registrar entrada/salida
@app.route("/registro", methods=["POST"])
def registrar():
    codigo = request.form["codigo"]
    ubicacion = request.form["ubicacion"]
    tipo = request.form["tipo"]
    hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    nuevo = {
        "codigo": codigo,
        "ubicacion": ubicacion,
        "tipo": tipo,
        "hora": hora
    }

    registros.append(nuevo)

    return "Registro guardado ✔<br><a href='/'>Volver</a>"

# Ver registros
@app.route("/registros")
def ver_registros():
    return jsonify(registros)

# Exportar a Excel
@app.route("/exportar")
def exportar():
    df = pd.DataFrame(registros)

    archivo = "registros.xlsx"
    df.to_excel(archivo, index=False)

    return send_file(archivo, as_attachment=True)

# IMPORTANTE para Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)