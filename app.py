from flask import Flask, request, jsonify, send_file
from datetime import datetime
import pandas as pd
import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# ===============================
# CONEXIÓN GOOGLE SHEETS (PRO)
# ===============================
sheet = None

try:
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    credenciales_json = os.getenv("GOOGLE_CREDENTIALS")

    if credenciales_json:
        credenciales_dict = json.loads(credenciales_json)
        creds = ServiceAccountCredentials.from_json_keyfile_dict(credenciales_dict, scope)
        client = gspread.authorize(creds)
        sheet = client.open("Control Asistencia ARMOS").sheet1

except Exception as e:
    print("Error Google Sheets:", e)
    sheet = None

# ===============================
# DATOS
# ===============================
registros = []
entradas = {}

empleados = [
    {"codigo": "13434", "nombre": "ANDRIW SOCHA"},
    {"codigo": "22345", "nombre": "JUAN PEREZ"},
    {"codigo": "33456", "nombre": "MARIA LOPEZ"},
    {"codigo": "44567", "nombre": "CARLOS RAMIREZ"}
]

# ===============================
# HOME (MEJORADO)
# ===============================
@app.route("/")
def inicio():
    opciones = ""
    for emp in empleados:
        opciones += f"<option value='{emp['codigo']}'>{emp['codigo']} - {emp['nombre']}</option>"

    return f"""
    <html>
    <head>
        <style>
            body {{
                margin: 0;
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #1c1f26, #2c3e50);
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
            }}

            .container {{
                background: #2b2f38;
                padding: 30px;
                border-radius: 15px;
                box-shadow: 0 0 20px rgba(0,0,0,0.5);
                text-align: center;
                width: 320px;
            }}

            img {{
                width: 120px;
                margin-bottom: 10px;
            }}

            h2 {{
                margin-bottom: 20px;
            }}

            select {{
                width: 100%;
                padding: 10px;
                margin: 8px 0;
                border-radius: 8px;
                border: none;
                font-size: 14px;
            }}

            .buttons {{
                margin-top: 15px;
                display: flex;
                gap: 10px;
            }}

            button {{
                flex: 1;
                padding: 12px;
                border: none;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
                cursor: pointer;
                transition: 0.2s;
            }}

            .entrada {{
                background: #2ecc71;
                color: white;
            }}

            .entrada:hover {{
                background: #27ae60;
            }}

            .salida {{
                background: #e74c3c;
                color: white;
            }}

            .salida:hover {{
                background: #c0392b;
            }}

            a {{
                display: block;
                margin-top: 20px;
                color: #00c3ff;
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
            <h2>Bienvenido a ARMOS</h2>

            <form action="/registrar" method="post">

                <select name="codigo">{opciones}</select>

                <select name="ubicacion">
                    <option value="Redfern">Redfern</option>
                    <option value="Mascot">Mascot</option>
                    <option value="Otro">Otro</option>
                </select>

                <div class="buttons">
                    <button class="entrada" name="tipo" value="entrada">Entrada</button>
                    <button class="salida" name="tipo" value="salida">Salida</button>
                </div>

            </form>

    
        </div>

    </body>
    </html>
    """

# ===============================
# REGISTRAR
# ===============================
@app.route("/registrar", methods=["POST"])
def registrar():
    codigo = request.form["codigo"]
    ubicacion = request.form["ubicacion"]
    tipo = request.form["tipo"]
    ahora = datetime.now()

    horas_trabajadas = ""

    if tipo == "entrada":
        entradas[codigo] = ahora
        mensaje = "Feliz inicio de turno 👋"
        color = "green"

    else:
        if codigo in entradas:
            inicio = entradas[codigo]
            diferencia = ahora - inicio
            horas = round(diferencia.total_seconds() / 3600, 2)
            horas_trabajadas = f"{horas} horas"
            mensaje = f"Gracias por tu ayuda 🙌<br>Trabajaste: {horas} horas"
            del entradas[codigo]
        else:
            mensaje = "No hay entrada registrada ⚠️"
        color = "red"

    registros.append({
        "codigo": codigo,
        "tipo": tipo,
        "ubicacion": ubicacion,
        "hora": ahora.strftime("%Y-%m-%d %H:%M:%S"),
        "horas_trabajadas": horas_trabajadas
    })

    if sheet:
        try:
            sheet.append_row([
                codigo,
                tipo,
                ubicacion,
                ahora.strftime("%Y-%m-%d %H:%M:%S"),
                horas_trabajadas
            ])
        except Exception as e:
            print("Error guardando en Sheets:", e)

    return f"""
    <html>
    <body style="font-family: Arial; background:#1c1f26; color:white; text-align:center; padding:50px;">
        
        <h1 style="color:{color};">{mensaje}</h1>

        <script>
            if (navigator.vibrate) {{
                navigator.vibrate(200);
            }}
        </script>

        <br><br>
        <a href="/" style="color:lightblue;">Volver</a>

    </body>
    </html>
    """



# ===============================
# RUN
# ===============================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)