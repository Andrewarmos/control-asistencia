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
    <html>
    <head>
        <title>ARMOS</title>
        <style>
            body {{
                font-family: Arial;
                background-color: #1c1f26;
                color: white;
                text-align: center;
                padding: 20px;
            }}

            .container {{
                background: #2a2f3a;
                padding: 30px;
                border-radius: 15px;
                max-width: 400px;
                margin: auto;
                box-shadow: 0px 0px 15px rgba(0,0,0,0.5);
            }}

            img {{
                width: 150px;
                margin-bottom: 10px;
            }}

            h1 {{
                margin-bottom: 20px;
            }}

            select {{
                width: 100%;
                padding: 12px;
                margin: 10px 0;
                border-radius: 8px;
                border: none;
                font-size: 14px;
            }}

            button {{
                width: 100%;
                padding: 14px;
                margin-top: 10px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
            }}

            .entrada {{
                background-color: #27ae60;
                color: white;
            }}

            .salida {{
                background-color: #e74c3c;
                color: white;
            }}

            a {{
                display: block;
                margin-top: 15px;
                color: #3498db;
                text-decoration: none;
            }}

            a:hover {{
                text-decoration: underline;
            }}
        </style>
    </head>

    <body>

        <div class="container">

            <img src="/static/logo.png">

            <h1>Bienvenido a ARMOS</h1>

            <form action="/registrar" method="post">

                <label>Empleado</label>
                <select name="codigo">
                    {opciones}
                </select>

                <label>Ubicación</label>
                <select name="ubicacion">
                    <option value="Redfern">Edificio Redfern</option>
                    <option value="Mascot">Edificio Mascot</option>
                    <option value="Otro">Otro</option>
                </select>

                <button class="entrada" type="submit" name="tipo" value="entrada">
                    Marcar Entrada
                </button>

                <button class="salida" type="submit" name="tipo" value="salida">
                    Marcar Salida
                </button>

            </form>

            <a href="/registros">Ver registros</a>
            <a href="/exportar">Descargar Excel</a>

        </div>

    </body>
    </html>
    """

# Registrar
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

# Exportar
@app.route("/exportar")
def exportar():
    df = pd.DataFrame(registros)
    archivo = "registros.xlsx"
    df.to_excel(archivo, index=False)
    return send_file(archivo, as_attachment=True)

# Run
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)