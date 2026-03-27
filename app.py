from flask import Flask, request, jsonify, send_file
from datetime import datetime
import pandas as pd

app = Flask(__name__)

# Base de datos temporal
registros = []

# Lista de empleados
empleados = [
    {"codigo": "13434", "nombre": "ANDRIW SOCHA"},
    {"codigo": "22345", "nombre": "JUAN PEREZ"},
    {"codigo": "33456", "nombre": "MARIA LOPEZ"},
    {"codigo": "44567", "nombre": "CARLOS RAMIREZ"}
]

# Página principal
@app.route("/")
def inicio():
    opciones = ""
    for emp in empleados:
        opciones += f"<option value='{emp['codigo']}'>{emp['codigo']} - {emp['nombre']}</option>"

    return f"""
    <h1>Bienvenido a ARMOS</h1>

    <form action="/registrar" method="post">
        <label>Empleado:</label><br>
        <select name="codigo">
            {opciones}
        </select><br><br>

        <label>Ubicación:</label><br>
        <select name="ubicacion">
            <option value="Redfern">Edificio Redfern</option>
            <option value="Mascot">Edificio Mascot</option>
            <option value="Otro">Otro</option>
        </select><br><br>

        <button type="submit" name="tipo" value="entrada">Marcar Entrada</button>
        <button type="submit" name="tipo" value="salida">Marcar Salida</button>
    </form>

    <br>
    <a href="/registros">Ver registros</a><br>
    <a href="/exportar">Descargar Excel</a>
    """

# Registrar entrada o salida
@app.route("/registrar", methods=["POST"])
def registrar():
    codigo = request.form["codigo"]
    ubicacion = request.form["ubicacion"]
    tipo = request.form["tipo"]
    hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    registros.append({
        "codigo": codigo,
        "tipo": tipo,
        "ubicacion": ubicacion,
        "hora": hora
    })

    return f"{tipo.capitalize()} registrada ✔<br><a href='/'>Volver</a>"

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

# Para Render
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)