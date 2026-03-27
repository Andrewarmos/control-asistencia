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

# Página principal (DISEÑO MEJORADO)
@app.route("/")
def inicio():
    opciones = ""
    for emp in empleados:
        opciones += f"<option value='{emp['codigo']}'>{emp['codigo']} - {emp['nombre']}</option>"

    return f"""
    <html>
    <head>
        <title>ARMOS</title>
        <style>
            body {{
                font-family: Arial;
                background-color: #f4f6f8;
                text-align: center;
                padding: 20px;
            }}

            .container {{
                background: white;
                padding: 30px;
                border-radius: 10px;
                max-width: 400px;
                margin: auto;
                box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
            }}

            h1 {{
                color: #2c3e50;
            }}

            select {{
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                border-radius: 5px;
                border: 1px solid #ccc;
            }}

            button {{
                width: 48%;
                padding: 12px;
                margin: 5px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
            }}

            .entrada {{
                background-color: #27ae60;
                color: white;
            }}

            .salida {{
                background-color: #c0392b;
                color: white;
            }}

            a {{
                display: block;
                margin-top: 10px;
                color: #2980b9;
                text-decoration: none;
            }}

            a:hover {{
                text-decoration: underline;
            }}

        </style>
    </head>

    <body>

        <div class="container">

            <h1>Bienvenido a ARMOS</h1>

            <!-- Aquí puedes agregar tu logo después -->
            <!-- <img src="URL_DEL_LOGO" width="120"> -->

            <form action="/registrar" method="post">

                <label>Empleado:</label>
                <select name="codigo">
                    {opciones}
                </select>

                <label>Ubicación:</label>
                <select name="ubicacion">
                    <option value="Redfern">Edificio Redfern</option>
                    <option value="Mascot">Edificio Mascot</option>
                    <option value="Otro">Otro</option>
                </select>

                <button class="entrada" type="submit" name="tipo" value="entrada">
                    Entrada
                </button>

                <button class="salida" type="submit" name="tipo" value="salida">
                    Salida
                </button>

            </form>

            <a href="/registros">Ver registros</a>
            <a href="/exportar">Descargar Excel</a>

        </div>

    </body>
    </html>
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